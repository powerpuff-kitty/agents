"""Bounded native OpenCode runs; retain public task events, never reasoning parts."""
from pathlib import Path
import hashlib,json,os,subprocess,time
BASE=Path(__file__).resolve().parent
HOST='/Users/tcsntcsn/.opencode/bin/opencode'
def clean(value):
 if isinstance(value,dict):
  if value.get('type') in ['reasoning','thinking','redacted_thinking']:return None
  return {k:clean(v) for k,v in value.items() if k not in ['reasoning','thinking','encrypted_content','signature']}
 if isinstance(value,list):return [clean(x) for x in value if not isinstance(x,dict) or x.get('type') not in ['reasoning','thinking','redacted_thinking']]
 return value
summary=[]
for name in ['implementation','review','missing-tool']:
 root=BASE/name;project=root/'workspace';prompt=(root/'prompt.txt').read_text().strip()
 env=dict(os.environ);env['OPENCODE_CONFIG_CONTENT']='{"autoupdate":false}';env['PYTHONDONTWRITEBYTECODE']='1'
 argv=[HOST,'run','--standalone','--format','json','--auto','--title','Native catalog '+name,prompt]
 started=time.monotonic();p=subprocess.Popen(argv,cwd=project,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 timeout=False
 try:stdout,stderr=p.communicate(timeout=180)
 except subprocess.TimeoutExpired:
  timeout=True;p.terminate()
  try:stdout,stderr=p.communicate(timeout=10)
  except subprocess.TimeoutExpired:p.kill();stdout,stderr=p.communicate()
 events=[];discarded=0;non_json=[]
 for line in stdout.splitlines():
  if not line.strip():continue
  try:event=json.loads(line)
  except ValueError:non_json.append(line);continue
  if event.get('type') in ['reasoning','thinking','redacted_thinking']:discarded+=1;continue
  events.append(clean(event))
 (root/'events.json').write_text(json.dumps(events,indent=2)+'\n')
 (root/'stderr.txt').write_text(stderr)
 (root/'non-json-output.txt').write_text('\n'.join(non_json)+'\n')
 record={'scenario':name,'argv':argv,'cwd':str(project),'exit':p.returncode,'timed_out':timeout,'elapsed_seconds':round(time.monotonic()-started,3),'host_version':subprocess.check_output([HOST,'--version'],text=True).strip(),'event_count':len(events),'reasoning_events_not_retained':discarded,'trace_scope':'CLI JSON events excluding reasoning/thinking; no credential/config files inspected or copied','configured_model':'default, not overridden','configured_agent':'default, not overridden','tool_permissions':'disposable project rules; --auto never overrides configured deny; not a sandbox'}
 (root/'run.json').write_text(json.dumps(record,indent=2)+'\n');summary.append(record)
 (BASE/'run-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps({'scenario':name,'exit':p.returncode,'timed_out':timeout,'events':len(events),'elapsed':record['elapsed_seconds']}),flush=True)
