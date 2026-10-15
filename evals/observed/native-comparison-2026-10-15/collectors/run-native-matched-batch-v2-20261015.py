import concurrent.futures,os,json,subprocess,time
from pathlib import Path
base=Path('/private/tmp/native-matched-2026-10-15-v3');plan=json.loads((base/'plan.json').read_text());env={**os.environ,'PYTHONPATH':'/Users/tcsntcsn/TCSN/agents/scripts'}
def run(entry):
 root=base/entry['id']
 if (root/'result.json').exists():return json.loads((root/'result.json').read_text())
 with (root/'collector.stdout').open('w') as out,(root/'collector.stderr').open('w') as err:
  p=subprocess.run(['python3',str(base/'runner-startup-fix.py'),'run','--output',str(base),'--id',entry['id'],'--opencode','/Users/tcsntcsn/.opencode/bin/opencode','--model','deepseek/deepseek-v4-pro','--timeout','180','--max-cost','0.15'],env=env,stdout=out,stderr=err,timeout=240)
 row=json.loads((root/'result.json').read_text()) if (root/'result.json').exists() else {'status':'collector_failed','entry':entry,'exit':p.returncode}
 print(json.dumps({'id':entry['id'],'status':row['status'],'usage':row.get('usage'),'exit':p.returncode}),flush=True)
 return row
# First live trial is owned by another foreground collector; never start it twice.
entries=plan['runs'][1:]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 pending={};iterator=iter(entries);stopped=False
 while True:
  while not stopped and len(pending)<2:
   try:entry=next(iterator)
   except StopIteration:break
   pending[pool.submit(run,entry)]=entry
  if not pending:break
  done,_=concurrent.futures.wait(pending,return_when=concurrent.futures.FIRST_COMPLETED)
  for future in done:
   entry=pending.pop(future)
   row=future.result()
   if row['status'] in ['setup_failed','collection_failed','model_mismatch','collector_failed']:stopped=True
  observed=[]
  for entry in plan['runs']:
   p=base/entry['id']/'result.json'
   if p.exists():observed.append(json.loads(p.read_text()))
  total=sum((r.get('usage') or {}).get('reported_cost') or 0 for r in observed)
  if total>=3:stopped=True
  (base/'batch-state.json').write_text(json.dumps({'stopped_on_infrastructure_or_cost':stopped,'reported_cost_observed':total,'completed_records':len(observed)},indent=2)+'\n')
print('Batch collector ended; inspect retained reports for task acceptance.',flush=True)
