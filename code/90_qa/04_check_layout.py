#!/usr/bin/env python3
"""内部验收：可读版次、代码镜像、分类输出、迁移与无QA公开包；只处理合成示例。"""
import csv
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from project_layout import RunLayout, write_json


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def check(layout):
    work=layout.provenance/'workspaces';work.mkdir()
    checks=[]
    def command(workspace,args,success=True):
        result=subprocess.run([sys.executable,str(workspace/args[0]),*args[1:]],cwd='/tmp',capture_output=True,text=True)
        with layout.file('logs','driver','.log').open('a') as f:f.write(result.stdout+result.stderr)
        if success and result.returncode!=0:raise RuntimeError(result.stdout+result.stderr)
        return result
    def last(workspace,task):
        paths=list((workspace/'outputs/runs'/task).glob('run_*.json'))
        file=max(paths,key=lambda p:p.stat().st_mtime_ns)
        return file,json.loads(file.read_text())
    def run(workspace):
        command(workspace,['run.py','--task','demo','--profile','config/machine.mac.example.json'])
        file,record=last(workspace,'demo');assert record['status']=='PASS'
        return file,record
    def mirror(workspace):
        wanted={p.relative_to(workspace/'code').as_posix() for p in (workspace/'code').rglob('*') if p.is_dir() and '__pycache__' not in p.parts and not p.name.startswith('.')}
        for layer in ['data_intermediate','data_analysis']:
            actual={p.relative_to(workspace/layer).as_posix() for p in (workspace/layer).rglob('*') if p.is_dir()}
            assert actual==wanted,(layer,actual^wanted)
    _,base=last(ROOT,'demo');assert base['qa_status']=='PASS'
    originals={name:digest(Path(path)) for name,path in base['artifacts'].items()}
    _,again=run(ROOT);assert again['edition']>base['edition'] and again['date']==base['date']
    assert originals=={name:digest(Path(path)) for name,path in base['artifacts'].items()}
    result=command(ROOT,['run.py','--task','demo','--profile','config/machine.mac.example.json','--date',base['date'],'--edition',str(base['edition'])],False)
    assert result.returncode!=0 and originals=={name:digest(Path(path)) for name,path in base['artifacts'].items()}
    checks.append({'check':'repeat_increments_readable_edition_and_refuses_overwrite','status':'PASS','first':base['version'],'second':again['version']})
    mirror(ROOT)
    for category in ['tables','figures','logs','estimates','samples','qa','runs']:
        for file in (ROOT/'outputs'/category).rglob('*'):
            if file.is_file():assert re.search(r'_\d{8}_v\d+\.',file.name),str(file)
    for folder in (ROOT/'outputs').rglob('*'):
        if folder.is_dir():assert not re.search(r'\d{8}_\d{6}_[a-f0-9]{8}$',folder.name),str(folder)
    figure=Path(base['artifacts']['MAIN_FIGURE']);table=Path(base['artifacts']['MAIN_TABLE'])
    assert figure.suffix=='.png' and figure.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
    assert table.suffix=='.doc' and table.read_bytes().lstrip().startswith(b'{\\rtf')
    assert not table.with_suffix('.txt').exists()
    assert not any(figure.with_suffix(ext).exists() for ext in ['.pdf','.gph','.svg','.jpg'])
    for area,kind,suffix in [('figures','figure','.pdf'),('tables','regression_table','.txt')]:
        try:layout.artifact({'area':area,'kind':kind,'module':'02_main_regressions','stem':'invalid_format','suffix':suffix},{})
        except ValueError:pass
        else:raise AssertionError('未拒绝不符合规则的图表格式')
    checks.append({'check':'png_images_doc_regression_tables_and_no_txt_sidecars','status':'PASS'})
    checks.append({'check':'mirrored_data_directories_and_type_first_dated_artifacts','status':'PASS'})
    moved=work/'内部迁移副本'
    shutil.copytree(ROOT,moved,ignore=shutil.ignore_patterns('outputs','releases','data_intermediate','data_analysis','__pycache__','.git'))
    _,moved_record=run(moved);assert moved_record['qa_status']=='PASS';mirror(moved)
    subprocess.run(['git','init','-q',str(moved)],check=True)
    for rel,wanted in [('data_raw/private_input.csv',0),(str(Path(moved_record['artifacts']['PANEL_FILE']).relative_to(moved)),0),(str(Path(moved_record['artifacts']['ANALYSIS_FILE']).relative_to(moved)),1)]:
        assert subprocess.run(['git','-C',str(moved),'check-ignore','--quiet',rel]).returncode==wanted
    checks.append({'check':'relocation_and_git_policy','status':'PASS','record':str(last(moved,'demo')[0])})
    command(ROOT,['export_replication.py']);_,export=last(ROOT,'export_replication');archive=Path(export['archive'])
    public=work/'公开生产包';public.mkdir()
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();assert len(names)==len(set(names)) and not any('/90_qa/' in n for n in names)
        tasks=json.loads(z.read('economics_workspace/config/tasks.json'));assert all('qa_entry' not in t and 'qa_artifacts' not in t for t in tasks.values())
        z.extractall(public)
    public=public/'economics_workspace';_,public_record=run(public)
    reserved={re.search(r'(\d{8}_v\d+)\.',p).group(1) for p in json.loads((ROOT/'config/replication_export.json').read_text())['analysis_files']}
    assert public_record['qa_status']=='NOT_RUN' and public_record['version'] not in reserved
    assert not (public/'code/90_qa').exists();mirror(public)
    checks.append({'check':'public_package_runs_without_qa_and_preserves_included_analysis_edition','status':'PASS','archive':str(archive),'record':str(last(public,'demo')[0])})
    command(ROOT,['server_sync.py','plan']);_,plan=last(ROOT,'server_sync_plan')
    assert plan['status']=='NOT_APPLICABLE' and not plan['remote_connection_made'] and re.fullmatch(r'\d{8}_v\d+',plan['version'])
    checks.append({'check':'server_plan_uses_readable_type_first_paths_without_connection','status':'PASS'})
    # 在Stata重新载入历史、当前、迁移及公开数据并逐项比较；完整b/V也比较。
    reference=ROOT/'data_analysis/01_data_preparation/02_build/firm_year_analysis_reference_20261027_v01.dta'
    statements=['version 18.0','set more off']
    for ref in [reference,Path(base['artifacts']['ANALYSIS_FILE'])]:
        statements += [f'use "{ref}", clear']
        for record in [again,moved_record,public_record]:statements += [f'cf _all using "{record["artifacts"]["ANALYSIS_FILE"]}", all']
    statements += [f'use "{base["artifacts"]["MAIN_SAMPLE"]}", clear']
    for record in [again,moved_record,public_record]:statements += [f'cf _all using "{record["artifacts"]["MAIN_SAMPLE"]}", all']
    statements += [f'estimates use "{base["artifacts"]["MAIN_ESTIMATE"]}"','matrix b0 = e(b)','matrix V0 = e(V)']
    for record in [again,moved_record,public_record]:
        statements += [f'estimates use "{record["artifacts"]["MAIN_ESTIMATE"]}"',
          'mata: st_numscalar("bdiff", max(abs(st_matrix("b0") :- st_matrix("e(b)"))))',
          'mata: st_numscalar("vdiff", max(abs(st_matrix("V0") :- st_matrix("e(V)"))))',
          'assert scalar(bdiff) <= 1e-10','assert scalar(vdiff) <= 1e-10']
    marker=layout.file('qa','compare_pass','.txt')
    statements += [f'file open result using "{marker}", write text','file write result "PASS" _n','file close result','exit, clear']
    script=layout.file('logs','compare','.do');script.write_text('\n'.join(statements)+'\n')
    stata=json.loads((ROOT/'config/machine.mac.example.json').read_text())['stata_bin']
    with layout.file('logs','compare_console','.log').open('w') as f:subprocess.run([stata,'-e','do',f'"{script}"'],cwd=layout.logs,stdout=f,stderr=subprocess.STDOUT,check=True)
    assert marker.read_text().strip()=='PASS'
    checks.append({'check':'historical_current_relocated_and_public_data_samples_full_b_V_match','status':'PASS','tolerance':1e-10})
    report={'status':'PASS','layout_version':4,'version':layout.version,'checks':checks,'scope':'synthetic on macOS; NUSTP read-only reference; no server connection','artifacts':again['artifacts']}
    write_json(layout.record,report);layout.status_file.write_text('PASS\n');write_json(layout.file('qa','layout_report','.json'),report)
    print(json.dumps({'status':'PASS','report':str(layout.record),'checks':len(checks)},ensure_ascii=False))


if __name__=='__main__':
    layout=RunLayout(ROOT,'layout_checks','90_qa')
    try:check(layout)
    except Exception as error:
        write_json(layout.record,{'status':'FAIL','version':layout.version,'error':str(error)})
        layout.status_file.write_text('FAIL\n');layout.file('logs','layout_error','.log').write_text(str(error)+'\n')
        raise
