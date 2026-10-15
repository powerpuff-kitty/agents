# Matched native trial measurements

| Task | Mode | Planned | Status | Acceptance | Input mean (range) | Cost mean |
| --- | --- | ---: | --- | --- | ---: | ---: |
| focused-review-with-skills | named-agent | 2 | {'setup_failed': 1, 'collected': 1} | {'blocked': 1, 'pass': 1} | 22943.0 (22943–22943); 1 missing | 0.035872188 |
| focused-review-with-skills | ordinary | 2 | {'collected': 1, 'timed_out': 1} | {'pass': 1, 'fail': 1} | 10116.5 (9872–10361); 0 missing | 0.026823104 |
| focused-review-with-skills | skill | 2 | {'collected': 2} | {'pass': 2} | 17291.5 (15775–18808); 0 missing | 0.0336578 |
| implementation-dirty-worktree | named-agent | 2 | {'collected': 2} | {'pass': 2} | 13019.0 (9932–16106); 0 missing | 0.020012058 |
| implementation-dirty-worktree | ordinary | 2 | {'collected': 2} | {'pass': 2} | 9338.5 (9064–9613); 0 missing | 0.014867775999999997 |
| implementation-dirty-worktree | skill | 2 | {'collected': 2} | {'pass': 2} | 10725.5 (10166–11285); 0 missing | 0.018859676 |
| implementation-unavailable-check | named-agent | 2 | {'collected': 1, 'timed_out': 1} | {'pass': 1, 'fail': 1} | 24164.0 (16290–32038); 0 missing | 0.039777496 |
| implementation-unavailable-check | ordinary | 2 | {'timed_out': 1, 'collected': 1} | {'fail': 1, 'pass': 1} | 20085.5 (14288–25883); 0 missing | 0.039483862 |
| implementation-unavailable-check | skill | 2 | {'timed_out': 2} | {'fail': 2} | 10015.5 (8823–11208); 0 missing | 0.01744985 |

- Built-in build is explicitly pinned for ordinary/skill controls; named-agent changes that primary.
- Role and skill treatments are different interventions, not a context-only savings experiment.
- Source bytes, instruction events, host-reported tokens/cache and billed costs are distinct.
- Unexposed auxiliary calls/settings remain unknown; sample sizes do not establish statistical reliability.
- No task success is inferred from host outcome, artifact invariants or a lower token count.
