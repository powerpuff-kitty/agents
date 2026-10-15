import sys,json,time
from pathlib import Path
sys.path.insert(0,'/Users/tcsntcsn/TCSN/agents/scripts')
import native_eval as n
old=Path('/private/tmp/native-project-pilot-followup-20261015');root=Path('/private/tmp/native-project-pilot-completion-v2-20261015');root.mkdir()
project=old/'project';prior=json.loads((old/'run.json').read_text());assert prior['status']=='collected'
old_sessions=json.loads((old/'sessions.json').read_text());sid=next(k for k,v in old_sessions.items() if v.get('parentID') is None and v['agent']=='team-lead')
model={'providerID':'deepseek','id':'deepseek-v4-pro'};started=time.monotonic();host=None;sessions={};messages={}
prompt='''Continue the SAME accepted team-feature task in this checkout. Your previous bounded turn stopped with required export gates and final readiness unfinished. Preserve the implemented source and owner work. Do not add optional improvements or widen scope.
Complete all outstanding mandatory AGENTS.md checks on the final source: validate, docs, both export builds, both export --check commands and full unittest suite. Run each command separately with the workdir parameter. The commands are explicitly allowed. A compound-command rejection is not a blanket shell prohibition.
Obtain a read-only independent quality recheck of the final corrected snapshot, retaining its actual report before reconciliation. Do not send writer explanations or desired verdicts. Then obtain the always-required iteration-reviewer final assessment against accepted scope and actual gate/review evidence. Conditional stages may be skipped only with reasons. Delegates must use DeepSeek. Do not reimplement or opportunistically harden unrelated inputs. Only the original 2 source/test files may change if a confirmed requirement defect needs correction; preserve owner note, source scope and staging. No installs, network tools, commit, publication or deployment.
Finish with a concise final delivery: actual commands/results, applicable reviews, preserved files and staging, implementation status and integrated readiness. Do not report readiness with any mandatory evidence missing. Readiness does not authorize publication. This is a continuation, not a replacement of the original retained run.\n'''
(root/'prompt.txt').write_text(prompt)
n.write(root/'before.json',n.snapshot(project));n.write(root/'git-before.json',n.git_state(project))
n.write(root/'source.json',{'prior_result_sha256':n.digest((old/'run.json').read_bytes()),'prior_session_id':sid,'source_commit':prior['source']['source_commit'],'candidate_source_sha256':{p:n.digest((project/p).read_bytes()) for p in prior['source']['allowed_source_changes']},'scope':'Resume prior coordinator conversation with original task and current candidate. Separate bounded user turn; all original records retained.'})
result={'status':'setup_failed','time_limit_seconds':600,'reported_cost_limit_cumulative':.75,'model_requested':model,'acceptance':'needs_independent_review','prior_result_sha256':n.digest((old/'run.json').read_bytes()),'prior_premature_collector_result_sha256':n.digest(Path('/private/tmp/native-project-pilot-completion-20261015/run.json').read_bytes()),'usage_scope':'Cumulative original root and discovered descendants, including prior turn; do not add to prior usage again.'}
try:
 host=n.Host('/Users/tcsntcsn/.opencode/bin/opencode',project,started+600);host.ready()
 query='?'+n.urllib.parse.urlencode({'location[directory]':str(project)})
 location=host.request('/api/location'+query);resolved=host.request('/api/session/'+sid)['data'];n.verify_binding(project,location,resolved,model)
 assert resolved['agent']=='team-lead'
 for _ in range(40):
  try:
   inventory=n.verify_inventory(project,host.request('/api/skill'+query)['data'],host.request('/api/agent'+query)['data']);break
  except ValueError:time.sleep(.2)
 else:raise ValueError('Inventory identity failed')
 n.write(root/'preflight.json',{'location':location,'session':n.clean(resolved),'inventory':inventory})
 n.write(root/'submitted-prompt.json',{'text':prompt})
 baseline_sessions,baseline_messages=n.capture(host,sid,project)
 baseline_ids={row['id'] for row in baseline_messages[sid]}
 n.write(root/'baseline-session.json',baseline_sessions[sid])
 n.write(root/'baseline-message-ids.json',sorted(baseline_ids))
 host.request('/api/session/'+sid+'/prompt',{'text':prompt});result['status']='running'
 while True:
  sessions,messages=n.capture(host,sid,project);n.write(root/'sessions.json',sessions);n.write(root/'messages.json',messages)
  if any(v.get('model',{}).get('id')!=model['id'] or v.get('model',{}).get('providerID')!=model['providerID'] for v in sessions.values()):raise ValueError('Model mismatch')
  cost=n.usage(sessions)
  if not cost['complete_session_fields'] or cost['reported_cost']>=.75:result['status']='usage_bound_reached';break
  new_rows=[row for row in messages[sid] if row['id'] not in baseline_ids]
  completed_turn=any(row.get('type')=='idle' for row in new_rows) and any(row.get('type')=='assistant' and row.get('finish')=='stop' for row in new_rows)
  if completed_turn and all(v.get('outcome') in ['succeeded','failed','interrupted'] for v in sessions.values()):result['status']='collected';break
  time.sleep(1)
except Exception as e:
 result['error']={'type':type(e).__name__,'message':str(e)}
 if isinstance(e,TimeoutError) or (host and host.deadline_expired):result['status']='timed_out'
 elif result['status']=='running':result['status']='collection_failed'
finally:
 if host:host.close()
 result['seconds']=round(time.monotonic()-started,3);result['usage_cumulative']=n.usage(sessions) if sessions else None
 n.write(root/'after.json',n.snapshot(project));n.write(root/'git-after.json',n.git_state(project));n.write(root/'run.json',result)
 print(json.dumps(result),flush=True)
