#!/usr/bin/env python3
"""按清单生成日期+版次命名的生产复现包，内部QA不对外分发。"""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from project_layout import CATEGORIES, RunLayout, registered_data_directories, write_json

ROOT=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date');parser.add_argument('--edition',type=int)
    args=parser.parse_args()
    layout=RunLayout(ROOT,'export_replication','00_setup',args.date,args.edition)
    archive=ROOT/'releases'/f'replication_{layout.version}.zip'
    archive.parent.mkdir(exist_ok=True)
    try:
        if archive.exists():raise FileExistsError(f'禁止覆盖：{archive}')
        config=json.loads((ROOT/'config/replication_export.json').read_text())
        tasks=json.loads((ROOT/'config/tasks.json').read_text())
        public_tasks={}
        for name in config['tasks']:
            task={k:v for k,v in tasks[name].items() if k not in {'qa_entry','qa_expected','qa_artifacts'}}
            if not task.get('enabled'):raise ValueError(f'任务未启用：{name}')
            public_tasks[name]=task
        files=[]
        for file in sorted((ROOT/'code').rglob('*')):
            if file.is_file() and not {'90_qa','__pycache__','.DS_Store'}.intersection(file.relative_to(ROOT/'code').parts):
                files.append((file,file.relative_to(ROOT).as_posix()))
        for rel in ['run.py','project_layout.py','management/DATA_REGISTRY.csv','management/SPECIFICATIONS.csv','management/EXHIBITS.csv','.gitignore']:
            files.append((ROOT/rel,rel))
        files += [(f,'config/'+f.name) for f in (ROOT/'config').glob('machine.*.example.json')]
        for rel in config['raw_files']:files.append((ROOT/'data_raw'/rel,'data_raw/'+rel))
        for rel in config['analysis_files']:files.append((ROOT/'data_analysis'/rel,'data_analysis/'+rel))
        manifest=[]
        with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
            for source,destination in files:
                content=source.read_bytes();z.writestr('economics_workspace/'+destination,content)
                manifest.append({'path':destination,'sha256':hashlib.sha256(content).hexdigest()})
            z.writestr('economics_workspace/config/tasks.json',json.dumps(public_tasks,ensure_ascii=False,indent=2))
            z.writestr('economics_workspace/README.md',(ROOT/'management/PUBLIC_REPLICATION_README.md').read_text())
            z.writestr('economics_workspace/AGENTS.md','# AI复现入口\n\n读README和config/tasks.json，运行登记的生产任务。输出类型优先、文件用日期和版次；数据目录对应code。内部90_qa不在本包，qa_status=NOT_RUN不能冒充内部QA已通过。\n')
            z.writestr('economics_workspace/project.json',json.dumps({'schema_version':4,'package_type':'public_replication','scope':config['scope'],'command':'python3 run.py --task demo','internal_qa_included':False,'analysis_files':config['analysis_files'],'output_layout':'type/module/filename_YYYYMMDD_vNN'},ensure_ascii=False,indent=2))
            z.writestr(f'economics_workspace/EXPORT_MANIFEST_{layout.version}.json',json.dumps({'scope':config['scope'],'version':layout.version,'internal_qa_included':False,'source_files':manifest},ensure_ascii=False,indent=2))
            data_directories={area:set() for area in ('intermediate','analysis')}
            for task in public_tasks.values():
                for area,directories in registered_data_directories(task).items():
                    data_directories[area].update(directories)
            for area,directories in data_directories.items():
                for rel in sorted(directories):
                    z.writestr(f'economics_workspace/data_{area}/{rel.as_posix()}/','')
            for category in CATEGORIES:
                z.writestr(f'economics_workspace/outputs/{category}/','')
        result={'status':'PASS','date':layout.date,'edition':layout.edition,'version':layout.version,'archive':str(archive),'files':len(files),'internal_qa_included':False}
        write_json(layout.record,result);layout.status_file.write_text('PASS\n')
        layout.file('logs','export','.log').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(archive);return 0
    except Exception as error:
        write_json(layout.record,{'status':'FAIL','version':layout.version,'error':str(error)})
        layout.status_file.write_text('FAIL\n');layout.file('logs','export_error','.log').write_text(str(error)+'\n')
        raise


if __name__=='__main__':raise SystemExit(main())
