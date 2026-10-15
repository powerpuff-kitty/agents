import concurrent.futures,importlib.util,json,sys,time,shutil
from pathlib import Path
roots=[Path('/private/tmp/native-failures-followup-20261015'),Path('/private/tmp/native-coverage-followup-20261015')]
for root in roots:
 shutil.copyfile('/Users/tcsntcsn/TCSN/agents/scripts/opencode_probe.py',root/'collectors/opencode_probe.py')
sys.path.insert(0,str(roots[0]/'collectors'))
import native_eval as n
jobs=[]
for root in roots:
 plan=json.loads((root/'plan.json').read_text());assert n.digest((root/'plan.json').read_bytes())==(root/'plan.sha256').read_text().strip()
 for entry in plan['runs']:jobs.append((root,entry))
model={'providerID':'deepseek','id':'deepseek-v4-pro'}
def run(job):
 root,entry=job
 print(json.dumps({'started':entry['id'],'group':root.name}),flush=True)
 value=n.execute(root/entry['id'],entry,'/Users/tcsntcsn/.opencode/bin/opencode',model,300 if 'failures' in root.name else 240,.20)
 print(json.dumps({'finished':entry['id'],'group':root.name,'status':value['status'],'seconds':value['seconds'],'invariants':value.get('invariants'),'usage':value.get('usage')}),flush=True)
 return value
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 results=list(pool.map(run,jobs))
for root in roots:n.report(root)
print(json.dumps({'executed':len(results),'automatic_retries':0}),flush=True)
