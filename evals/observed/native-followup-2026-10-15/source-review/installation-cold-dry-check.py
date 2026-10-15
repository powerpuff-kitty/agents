import hashlib,json,os,shutil,stat,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
work=root/'installation-cold-dry-reproduction';source=work/'source'
shutil.copytree(Path('/private/tmp/installation-followup-recheck-20261015/source'),source)
for p in list(source.rglob('__pycache__')):shutil.rmtree(p)
def snap():
 out={}
 for p in [work,*sorted(work.rglob('*'))]:
  st=p.lstat();out[str(p.relative_to(work))]={'mode':stat.S_IMODE(st.st_mode),'mtime_ns':st.st_mtime_ns,'ctime_ns':st.st_ctime_ns,'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None}
 return out
before=snap();argv=[sys.executable,'-B','scripts/install.py','--agent','designer','--target',str(work/'nonexistent/agents'),'--dry-run']
p=subprocess.run(argv,cwd=source,capture_output=True,text=True,timeout=30)
result={'argv':argv,'cwd':str(source),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'all_bounded_nodes_content_modes_mtimes_unchanged':snap()==before}
assert p.returncode==0 and result['all_bounded_nodes_content_modes_mtimes_unchanged']
(root/'installation-cold-dry-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
