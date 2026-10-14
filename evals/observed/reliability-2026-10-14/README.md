# Reliability evaluations — 2026-10-14

The current corpus has 144 canonical case specifications. This batch observes
3 additional distinct cases, bringing combined coverage to **6 observed and 138
unobserved**. Specifications retain `not_run`; observations remain separate.

## What ran

| Work | Sessions and evidence | Scope |
| --- | --- | --- |
| Initial catalog selection | 4 fresh sessions: 2 pagination fixes and 2 pending-diff reviews under discovery-initial/ | Chose relevant procedures from the 59-skill metadata index; source review later found shared-contract routing was not explicit |
| Fixed catalog selection | 4 fresh sessions: the same 2 tasks, each repeated twice under discovery-fixed/ | Metadata index contains 62 skills and 35 roles; task/catalog require the shared contract before optional selection |
| New procedure cases | 3 tasks in 1 fresh session under forward/ | Explicit role/skill loading for reflection, memory and agent-tool security; not 3 independent sessions |
| Independent review | source-review/, output-review/ and discovery-review/ | Non-author source/fixture/output checks with actual local reproductions; historical traces/usage are not authenticated |

All fresh evaluator/reviewer launches requested `fork_turns: none` in the actual
collaboration calls. That is invocation provenance, not proof of a platform sandbox,
statistical independence or exact model identity. Existing test fixtures were
supplied as raw artifacts; intended answers, graders and prior reports were withheld
from the task evaluators. Later correction/recheck assignments were separate.

## Supported results and retained limitations

- Pagination fixes remove the demonstrated equality/break defect and retain the
  owner's pending label edit. Independent checks reran the original 5 tests and
  neighboring generated cases. Fixed pagination-2 also adds 3 legitimate boundary
  tests: its raw `tests_preserved` byte check is false. Existing assertions remain
  intact; the independent review assesses this against the actual task rather than
  silently turning that false check into a pass.
- Both pending-diff reviews identify the percentage/dollar arithmetic regressions,
  including the new checkout caller. Fixtures remain read-only. Fixed review-2
  reports hashing all instruction bytes for preservation, exceeding its literal
  selected-only read boundary. Preserve that scope limitation; no clean routing
  or full trace-completeness claim is inferred.
- Reflection proposes a bounded correction from supplied failed-test evidence;
  there is no executable adapter or successful recheck claim.
- Memory decisions cover the **12 actual records** and reject 3 promotion candidates.
  Original result/actions incorrectly say 13. The [original finding](output-review/original-findings.md)
  and separate [count correction](memory-count-correction/correction.md) remain visible;
  the original observed report is not rewritten.
- Gateway probes reproduce authorization and destination weaknesses in an inert,
  intentionally vulnerable function. No tool dispatch, data export, URL request or
  live-model injection was performed. Missing-destination denial is an explicit
  fail-closed interpretation, not a verified production API schema.

[Initial source review](source-review/review-initial.md),
[separate fix recheck](source-review/review-recheck-2.md),
[7-output review](output-review/review.md) and
[fixed-discovery review](discovery-review/report.md) retain their original conclusions.
Case-specific skill specs have fixture transformations and concrete criteria, but
those 12 skill specifications are not claimed as completed canonical/model runs.

## Reproduce and interpret

From an Agents checkout and the recorded Skills source, prepare a new fixture:

```sh
python3 scripts/behavior_eval.py prepare --case implementation-dirty-worktree --skills-source /path/to/ai-skills --discovery --output /path/to/new/trial
python3 scripts/behavior_eval.py prepare --case reflection-evidence-boundary --skills-source /path/to/ai-skills --output /path/to/new/reflection
```

Give only task/workspace/discovery instructions to a fresh scoped evaluator;
keep initial metadata/grader and other outcomes outside its allowed reads. Retain
its actual response/actions, then run `grade` and independently assess the task.
Deterministic invariants do not automatically grade reasoning or instruction reads.

The [public export record](public-export.json) discloses separate-copy redactions
of unrelated ambient-project notes, omitted unselected instruction trees and Git
internals. Selected complete folders, catalogs, fixture workspaces, baseline files,
diffs, initial hashes and reports are retained. Original private runs remain intact.
Full old instruction grading or reviewer-script replay needs the original/regenerated
snapshot; these trimmed public exports do not pretend every private path exists.
Scripts/check outputs are historical execution evidence, not new model sessions.

[Native host evidence](native-host.json) separately registers 62 skills, 35 profiles
and 20 commands with exact bodies/paths at OpenCode v2.0.27 (commands by name).
No provider/model call or personal configuration write occurred in that check.
Catalog-assisted selection is not automatic native-host triggering. These small
synthetic workloads do not establish broad reliability, token savings or production
security. Model/version, token/cost and complete historical action accounting remain
unknown. No memory backend, npm publication or stable CLI release was performed.
