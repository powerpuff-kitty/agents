import sys,json,concurrent.futures
from pathlib import Path
root=Path('/private/tmp/native-corrections-followup-20261015');sys.path.insert(0,str(root/'collectors'));import native_eval as n
plan=json.loads((root/'plan.json').read_text());assert n.digest((root/'plan.json').read_bytes())==(root/'plan.sha256').read_text().strip()
def run(e):
 v=n.execute(root/e['id'],e,'/Users/tcsntcsn/.opencode/bin/opencode',{'providerID':'deepseek','id':'deepseek-v4-pro'},300,.20)
 print(json.dumps({'id':e['id'],'status':v['status'],'seconds':v['seconds'],'invariants':v.get('invariants'),'usage':v.get('usage')}),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,plan['runs']))
n.report(root)
