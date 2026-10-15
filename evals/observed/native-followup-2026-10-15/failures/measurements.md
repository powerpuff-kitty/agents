# Matched native trial measurements

| Task | Mode | Planned | Status | Acceptance | Input mean (range) | Cost mean |
| --- | --- | ---: | --- | --- | ---: | ---: |
| focused-review-with-skills | ordinary | 1 | {'collected': 1} | {'pass': 1} | 9961.0 (9961–9961); 0 missing | 0.024899996 |
| implementation-unavailable-check | named-agent | 1 | {'collected': 1} | {'fail': 1} | 17137.0 (17137–17137); 0 missing | 0.026927208000000005 |
| implementation-unavailable-check | ordinary | 1 | {'collected': 1} | {'pass': 1} | 9600.0 (9600–9600); 0 missing | 0.01928718 |
| implementation-unavailable-check | skill | 2 | {'collected': 2} | {'pass': 2} | 11854.5 (10144–13565); 0 missing | 0.022475089999999996 |

- Built-in build is explicitly pinned for ordinary/skill controls; named-agent changes that primary.
- Role and skill treatments are different interventions, not a context-only savings experiment.
- Source bytes, instruction events, host-reported tokens/cache and billed costs are distinct.
- Unexposed auxiliary calls/settings remain unknown; sample sizes do not establish statistical reliability.
- No task success is inferred from host outcome, artifact invariants or a lower token count.
