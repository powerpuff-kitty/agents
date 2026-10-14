"""Native sessions with verified explicit project binding; no personal config writes."""
from pathlib import Path
import base64,hashlib,json,os,secrets,shutil,socket,subprocess,time,urllib.parse,urllib.request
BASE=Path(__file__).resolve().parent;HOST='/Users/tcsntcsn/.opencode/bin/opencode'
MODEL={'providerID':'deepseek','id':'deepseek-v4-pro'}
def clean(value):
 if isinstance(value,dict):
  if value.get('type') in ['reasoning','thinking','redacted_thinking']:return None
  return {k:clean(v) for k,v in value.items() if k not in ['reasoning','thinking','encrypted_content','signature']}
 if isinstance(value,list):return [clean(x) for x in value if not isinstance(x,dict) or x.get('type') not in ['reasoning','thinking','redacted_thinking']]
 return value
def snap(root):
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and '.git' not in p.relative_to(root).parts and '__pycache__' not in p.parts}
summary=[]
for name in ['implementation','review','missing-tool']:
 original=BASE/name;out=BASE/'bound-v2'/name;out.mkdir(parents=True);project=out/'project'
 shutil.copytree(original/'workspace',project,ignore=shutil.ignore_patterns('__pycache__'))
 prompt=(original/'prompt.txt').read_text().strip();(out/'prompt.txt').write_text(prompt+'\n')
 before=snap(project);(out/'before.json').write_text(json.dumps(before,indent=2)+'\n')
 config=json.loads((project/'opencode.json').read_text())
 env={k:v for k,v in os.environ.items() if not k.startswith('OPENCODE_') and k!='INIT_CWD'}
 env['PWD']=str(project);env['OPENCODE_CONFIG_CONTENT']='{"autoupdate":false}'
 env['OPENCODE_USERNAME']='opencode';env['OPENCODE_PASSWORD']=secrets.token_hex(24);env['PYTHONDONTWRITEBYTECODE']='1'
 with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
 server=subprocess.Popen([HOST,'serve','--hostname','127.0.0.1','--port',str(port)],cwd=project,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 auth=base64.b64encode(('opencode:'+env['OPENCODE_PASSWORD']).encode()).decode()
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}));url=f'http://127.0.0.1:{port}'
 session_id=None;started=time.monotonic();result={'scenario':name,'model_requested':MODEL,'wall_clock_limit_seconds':240,'prompt_names_roles_or_skills':False,'trace_scope':'API messages excluding reasoning/thinking; no private config/credentials copied','host_version':subprocess.check_output([HOST,'--version'],text=True).strip()}
 def request(path,body=None):
  data=json.dumps(body).encode() if body is not None else None
  req=urllib.request.Request(url+path,data=data,headers={'Authorization':'Basic '+auth,'Content-Type':'application/json'})
  with opener.open(req,timeout=15) as response:
   raw=response.read(20_000_001)
   if len(raw)>20_000_000:raise ValueError('API response bound exceeded')
   return json.loads(raw) if raw else None
 query='?'+urllib.parse.urlencode({'location[directory]':str(project)})
 try:
  for _ in range(50):
   try:api=request('/openapi.json');break
   except OSError:time.sleep(.1)
  else:raise ValueError('Server readiness failed')
  location=request('/api/location'+query)
  assert location['directory']==str(project) and location['project']['directory']==str(project),'Wrong preflight project'
  for attempt in range(40):
   skills=request('/api/skill'+query) if '/api/skill' in api['paths'] else None
   agents=request('/api/agent'+query) if '/api/agent' in api['paths'] else None
   if skills and agents and len(skills.get('data',[]))>=62:break
   time.sleep(.2)
  if skills is None or agents is None:raise ValueError('Host inventory routes unavailable')
  loaded={x['id']:x for x in skills['data']};profiles={x['id']:x for x in agents['data']}
  owned_skills={};owned_agents={}
  for file in sorted((project/'.agents/skills').glob('*/SKILL.md')):
   skill=file.parent.name;body=file.read_text().split('\n---\n',1)[1].strip();actual=loaded[skill]
   assert actual['path']==str(file) and actual['content'].strip()==body,'Skill identity drift'
   owned_skills[skill]={'path':actual['path'],'body_sha256':hashlib.sha256(body.encode()).hexdigest()}
  for file in sorted((project/'.opencode/agents').glob('*.md')):
   body=file.read_text().split('\n---\n',1)[1].strip();actual=profiles[file.stem]
   assert actual.get('system','').strip()==body and actual.get('steps')==10,'Profile identity/step limit drift'
   owned_agents[file.stem]={'body_sha256':hashlib.sha256(body.encode()).hexdigest(),'mode':actual['mode'],'steps':actual['steps']}
  created=request('/api/session',{'title':'Bound native catalog '+name,'model':MODEL,'location':{'directory':str(project)},'permissions':config['permissions']})['data']
  session_id=created['id'];assert created['location']['directory']==str(project),'Wrong session project'
  resolved=request('/api/session/'+session_id)['data'];assert resolved['location']['directory']==str(project),'Wrong resolved project'
  primary=resolved.get('agent','build');assert profiles[primary]['steps']==10,'Primary step limit not loaded'
  (out/'resolved-before-prompt.json').write_text(json.dumps(clean(resolved),indent=2)+'\n')
  actual_model=resolved.get('model',{})
  assert actual_model.get('providerID')==MODEL['providerID'] and actual_model.get('id')==MODEL['id'],'Model resolution mismatch: '+repr(actual_model)
  preflight={'location':location,'session':clean(resolved),'owned_skills':owned_skills,'owned_agents':owned_agents,'default_agent_steps':profiles[primary]['steps'],'explicit_location_verified_before_prompt':True}
  (out/'preflight.json').write_text(json.dumps(preflight,indent=2)+'\n')
  request('/api/session/'+session_id+'/prompt',{'text':prompt})
  seen_idle=False
  while time.monotonic()-started<240:
   current=request('/api/session/'+session_id)['data']
   assert current['location']['directory']==str(project),'Session location changed'
   # Fetch all message pages; never retain reasoning/thinking parts.
   messages=[];path='/api/session/'+session_id+'/message?limit=100&order=asc'
   while path:
    page=request(path);messages.extend(clean(page['data']))
    cursor=page.get('cursor',{}).get('next');path='/api/session/'+session_id+'/message?'+urllib.parse.urlencode({'limit':100,'cursor':cursor}) if cursor else None
   (out/'messages.json').write_text(json.dumps(messages,indent=2)+'\n')
   (out/'session.json').write_text(json.dumps(clean(current),indent=2)+'\n')
   if current.get('outcome') in ['succeeded','failed','interrupted'] and messages:
    result['status']='finished';result['session_outcome']=current.get('outcome','unknown');seen_idle=True;break
   time.sleep(1)
  if not seen_idle:
   request('/api/session/'+session_id+'/interrupt',{});result['status']='timed_out'
  result['session_id']=session_id
 except Exception as error:
  result['status']='setup_or_run_error';result['error_type']=type(error).__name__;result['error']=str(error)
  if session_id:
   try:request('/api/session/'+session_id+'/interrupt',{})
   except Exception:pass
 finally:
  server.terminate()
  try:server.wait(timeout=5)
  except subprocess.TimeoutExpired:server.kill();server.wait()
  after=snap(project);(out/'after.json').write_text(json.dumps(after,indent=2)+'\n')
  result['changed_files']=sorted(k for k in set(before)|set(after) if before.get(k)!=after.get(k))
  result['elapsed_seconds']=round(time.monotonic()-started,3)
  (out/'run.json').write_text(json.dumps(result,indent=2)+'\n');summary.append(result)
  (BASE/'bound-v2-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(result),flush=True)
 if result['status']=='setup_or_run_error':break
raise SystemExit(0 if len(summary)==3 and all(x['status']=='finished' for x in summary) else 1)
