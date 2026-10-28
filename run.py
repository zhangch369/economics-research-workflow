#!/usr/bin/env python3
"""Stata生产任务入口：代码镜像数据目录，类型优先输出，日期和版次命名。"""
import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
from pathlib import Path
from project_layout import RunLayout, mirror_data_directories, now, resolve, write_json

ROOT = Path(__file__).resolve().parent


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def stata_path(path):
    value = path.as_posix()
    if any(c in value for c in ['"', '`', '$', '\n', '\r']):
        raise ValueError('Stata路径不能包含引号、反引号、美元符号或换行。')
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task', default='demo')
    parser.add_argument('--profile', default='config/machine.local.json')
    parser.add_argument('--date', help='输出日期YYYYMMDD，默认北京时间当天')
    parser.add_argument('--edition', type=int, help='指定版次；已存在则拒绝覆盖。默认自动递增。')
    args = parser.parse_args()
    tasks = json.loads((ROOT/'config/tasks.json').read_text())
    if args.task not in tasks:
        parser.error('任务未登记。')
    task = tasks[args.task]
    profile = json.loads(resolve(ROOT,args.profile).read_text())
    roots = {k:resolve(ROOT,profile.get(field,default)) for k,field,default in [
        ('raw','data_raw_root','data_raw'), ('intermediate','data_intermediate_root','data_intermeidate'),
        ('analysis','data_analysis_root','data_analysis')]}
    reserved=set()
    for spec in task.get('artifacts',{}).values():
        directory=(roots[spec['area']] if spec['area'] in roots else ROOT/'outputs'/spec['area'])/spec['module']
        pattern=re.compile(re.escape(f"{spec['stem']}_{args.task}_")+r'(\d{8}_v\d+)'+re.escape(spec['suffix'])+r'$')
        if directory.is_dir():
            for path in directory.iterdir():
                match=pattern.fullmatch(path.name)
                if match:reserved.add(match.group(1))
    layout = RunLayout(ROOT, args.task, task.get('output_module', '00_setup'), args.date, args.edition, reserved)
    record = {'status':'RUNNING', 'task':args.task, 'run_id':layout.run_id,
              'date':layout.date, 'edition':layout.edition, 'version':layout.version,
              'started_at':now(), 'project_root':str(ROOT), 'host':platform.node(),
              'os':platform.platform(), 'python':sys.version, 'python_executable':sys.executable,
              'qa_status':'NOT_RUN', 'entry':task['entry'], 'scope':task['scope']}
    proc = None

    def update(status, error=None):
        record['status'] = status
        if status != 'RUNNING': record['ended_at'] = now()
        if error: record['error'] = error
        write_json(layout.record, record)
        layout.status_file.write_text(status+'\n')

    def interrupted(signum, frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, interrupted)
    update('RUNNING')
    print(f'运行记录：{layout.record}', flush=True)
    try:
        if not task.get('enabled'):
            raise RuntimeError('正式任务尚未接入，不能标记完成。')
        stata = resolve(ROOT,profile['stata_bin'])
        if not stata.is_file(): raise FileNotFoundError(f'请填写Stata实际路径：{stata}')
        if len(set(roots.values())) != 3: raise ValueError('三层数据须使用不同目录。')
        mirror_data_directories(ROOT,roots)
        specs = dict(task['artifacts'])
        if task.get('qa_entry'): specs.update(task.get('qa_artifacts',{}))
        artifacts = {name:layout.artifact(spec,roots) for name,spec in specs.items()}
        for path in artifacts.values():
            if path.exists(): raise FileExistsError(f'已有同名产物，禁止覆盖：{path}')
        record.update({'data_roots':{k:str(v) for k,v in roots.items()}, 'data_version':layout.version,
                       'artifacts':{k:str(v) for k,v in artifacts.items()}, 'seed':20261027, 'processors':1})
        inputs=[]
        for item in task['inputs']:
            path=roots[item['area']]/item['path']
            inputs.append({**item,'bytes':path.stat().st_size,'sha256':sha256(path)})
        provenance=layout.provenance
        write_json(provenance/f'inputs_{layout.version}.json',inputs)
        shutil.copytree(ROOT/'code',provenance/'code',ignore=shutil.ignore_patterns('__pycache__','.DS_Store'))
        for rel in ['run.py','project_layout.py','AGENTS.md','project.json','management/STATUS.md',
                    'management/DATA_REGISTRY.csv','management/SPECIFICATIONS.csv','management/EXHIBITS.csv']:
            source=ROOT/rel
            if source.is_file():
                target=provenance/'context'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
        write_json(provenance/f'task_{layout.version}.json',task)
        write_json(provenance/f'machine_{layout.version}.json',{k:profile[k] for k in (
            'stata_bin','data_raw_root','data_intermediate_root','data_analysis_root','batch_flag') if k in profile})
        snapshot=provenance/'code'
        write_json(provenance/f'code_manifest_{layout.version}.json',[
            {'path':p.relative_to(snapshot).as_posix(),'sha256':sha256(p)} for p in sorted(snapshot.rglob('*')) if p.is_file()])
        log=layout.file('logs','analysis','.log')
        wrapper=layout.file('logs','entry','.do')
        rcfile=layout.record.parent/f'stata_rc_{layout.version}.txt'
        qastate=layout.file('qa','qa_status','.txt',module='90_qa')
        values={'PROJECT':ROOT,'CODE':snapshot,'RAW':roots['raw'],'INTERMEDIATE':roots['intermediate'],
                'ANALYSIS':roots['analysis'],'OUT':ROOT/'outputs','LOG_FILE':log,'STATA_RC_FILE':rcfile,
                'QA_STATUS_FILE':qastate,**artifacts}
        lines=['version 18.0','clear all','set more off','set varabbrev off','set seed 20261027',
               'set sortseed 20261027','if c(MP) == 1 set processors 1']
        lines += [f'global {name} "{stata_path(path)}"' for name,path in values.items()]
        lines += [f'global VERSION "{layout.version}"','capture log close _all',
                  'log using "$LOG_FILE", text name(runlog)',
                  f'capture noisily do "{stata_path(snapshot/task["entry"])}"','local stata_rc = _rc']
        if task.get('qa_entry'):
            lines += ['if `stata_rc\' == 0 {',f'    capture noisily do "{stata_path(snapshot/task["qa_entry"])}"',
                      '    local stata_rc = _rc','    file open qastate using "$QA_STATUS_FILE", write text',
                      '    if `stata_rc\' == 0 file write qastate "PASS" _n',
                      '    else file write qastate "FAIL" _n','    file close qastate','}']
        lines += ['file open rcfile using "$STATA_RC_FILE", write text',
                  'file write rcfile "`stata_rc\'" _n','file close rcfile','log close runlog','exit `stata_rc\', clear']
        wrapper.write_text('\n'.join(lines)+'\n')
        flag=profile.get('batch_flag','/e' if os.name=='nt' else ('-e' if sys.platform=='darwin' else '-b'))
        command=[str(stata),flag,'do',f'"{stata_path(wrapper)}"']
        record.update({'command':command,'log_directory':str(layout.logs),'provenance':str(provenance)})
        update('RUNNING')
        with layout.file('logs','console','.log').open('w') as handle:
            proc=subprocess.Popen(command,cwd=layout.logs,stdout=handle,stderr=subprocess.STDOUT)
            record['process_returncode']=proc.wait()
        record['stata_returncode']=int(rcfile.read_text().strip()) if rcfile.exists() else None
        if qastate.exists(): record['qa_status']=qastate.read_text().strip()
        if record['process_returncode']!=0 or record['stata_returncode']!=0:
            raise RuntimeError(f'Stata未完成；查看{log}及启动日志。')
        expected=list(task['expected'])+(task.get('qa_expected',[]) if task.get('qa_entry') else [])
        manifest=[]
        for name in expected:
            path=artifacts[name]
            if not path.is_file() or path.stat().st_size==0: raise RuntimeError(f'缺必需产物：{path}')
            manifest.append({'artifact':name,'path':str(path),'bytes':path.stat().st_size,'sha256':sha256(path)})
        if task.get('qa_entry') and (record['qa_status']!='PASS' or artifacts['QA_PASS'].read_text().strip()!='PASS'):
            raise RuntimeError('内部QA未通过。')
        write_json(provenance/f'outputs_{layout.version}.json',manifest)
        update('PASS')
        print(f'PASS：{layout.version}；内部QA：{record["qa_status"]}',flush=True)
        return 0
    except KeyboardInterrupt:
        if proc is not None and proc.poll() is None:
            proc.terminate()
            try: proc.wait(timeout=10)
            except subprocess.TimeoutExpired: proc.kill();proc.wait()
        update('INTERRUPTED','运行被中断；保留日志和部分产物。')
        return 130
    except Exception as error:
        update('FAIL',str(error));layout.file('logs','launcher_error','.log').write_text(str(error)+'\n')
        print(f'FAIL：{error}',file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
