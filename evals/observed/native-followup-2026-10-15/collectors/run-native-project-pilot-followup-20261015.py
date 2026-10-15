import importlib.util,sys,json,time
from pathlib import Path
sys.path.insert(0,'/Users/tcsntcsn/TCSN/agents/scripts')
import native_eval as n
root=Path('/private/tmp/native-project-pilot-followup-20261015');project=root/'project'
assert not (root/'run.json').exists()
started=time.monotonic();deadline=started+900
model={'providerID':'deepseek','id':'deepseek-v4-pro'};host=None;sid=None;sessions={};messages={}
result={'source':json.loads((root/'source.json').read_text()),'model_requested':model,'time_limit_seconds':900,'reported_cost_limit':.75,'team_command':'team-feature','acceptance':'needs_independent_review','status':'setup_failed'}
try:
 assert n.snapshot(project)==json.loads((root/'before.json').read_text())
 assert n.git_state(project)==json.loads((root/'git-before.json').read_text())
 host=n.Host('/Users/tcsntcsn/.opencode/bin/opencode',project,deadline);host.ready()
 query='?'+n.urllib.parse.urlencode({'location[directory]':str(project)})
 location=host.request('/api/location'+query)
 n.verify_binding(project,location,{'location':{'directory':str(project)},'model':model},model)
 for _ in range(40):
  try:
   inventory=n.verify_inventory(project,host.request('/api/skill'+query)['data'],host.request('/api/agent'+query)['data']);break
  except ValueError:time.sleep(.2)
 else:raise ValueError('Inventory identity failed')
 commands=host.request('/api/command'+query)['data'];command=next(v for v in commands if v['name']=='team-feature')
 # Host exposes command template identity. Save only this selected owned command.
 n.write(root/'command-registered.json',command)
 config=json.loads((project/'opencode.json').read_text())
 created=host.request('/api/session',{'title':'AI Agents real-project measurement-validation pilot','model':model,'agent':'team-lead','location':{'directory':str(project)},'permissions':config['permissions']})['data'];sid=created['id'];resolved=host.request('/api/session/'+sid)['data'];n.verify_binding(project,location,resolved,model);assert resolved['agent']=='team-lead'
 n.write(root/'preflight.json',{'location':location,'session':n.clean(resolved),'inventory':inventory})
 prompt={'name':'team-feature','text':(root/'prompt.txt').read_text()};n.write(root/'submitted-command.json',prompt)
 if time.monotonic()>=deadline:raise TimeoutError('Deadline before prompt')
 host.request('/api/session/'+sid+'/command',prompt);result['status']='running'
 while time.monotonic()<deadline:
  sessions,messages=n.capture(host,sid,project);n.write(root/'sessions.json',sessions);n.write(root/'messages.json',messages)
  if any(v.get('model',{}).get('id')!=model['id'] or v.get('model',{}).get('providerID')!=model['providerID'] for v in sessions.values()):raise ValueError('Delegate model mismatch')
  cost=n.usage(sessions)
  if not cost['complete_session_fields'] or cost['reported_cost']>=.75:result['status']='usage_bound_reached';break
  if all(v.get('outcome') in ['succeeded','failed','interrupted'] for v in sessions.values()):result['status']='collected';break
  time.sleep(1)
 else:result['status']='timed_out'
except Exception as error:
 result['error']={'type':type(error).__name__,'message':str(error)}
 if isinstance(error,TimeoutError) or (host and host.deadline_expired):result['status']='timed_out'
 elif result['status']=='running':result['status']='collection_failed'
finally:
 if host:
  try:
   if sid and result['status']!='collected':
    host.deadline=time.monotonic()+10
    for current in set(sessions)|{sid}:host.request('/api/session/'+current+'/interrupt',{})
    sessions,messages=n.capture(host,sid,project);n.write(root/'sessions.json',sessions);n.write(root/'messages.json',messages)
  except Exception as e:result['final_capture_error']=type(e).__name__
  finally:host.close()
 n.write(root/'after.json',n.snapshot(project));n.write(root/'git-after.json',n.git_state(project));result['seconds']=round(time.monotonic()-started,3);result['usage']=n.usage(sessions) if sessions else None
 n.write(root/'run.json',result);print(json.dumps(result),flush=True)
