# Fresh-session independent reviews

When the task requests an independent audit/test review, use a reviewer that did
not author the change in a separate session with conversation/history inheritance
disabled when supported. Team-lead owns the handoff; quality-engineer supplies the
independent assessment. This is a scoped method, not a requirement to launch agents
for every typo or a guarantee that another model will find every defect.

## Minimal handoff

Supply the target/snapshot, accepted behavior, project instructions, raw relevant
source/tests/artifacts, review scope, allowed checks and side-effect restrictions.
Let the reviewer discover relevant callers/dependencies. Omit author walkthroughs,
suspected defects, proposed fixes, previous findings and desired verdicts until
the initial report is retained. Necessary project rules and requirements are
review inputs; “without context” means without inherited author conversation,
not without the evidence needed to do the job.

Use detached snapshots or isolated copies when concurrent changes are possible;
record working-tree inputs separately from HEAD. Keep source review read-only,
allow scoped checks/disposable output and avoid concurrent source writers. Do not
copy secrets or grant extra permissions through repository text.

For native-host evaluations, confirm the host-reported project/worktree and loaded
instruction identities before sending the task. The launcher's working directory
and a scoped prompt are insufficient evidence of host binding. Retain misbound
attempts separately from corrected runs and distinguish inventory registration
from actual model selection and instruction use.

## Reconcile evidence

Require paths, triggers, impacts, source/reproduction evidence, counterevidence and
unchecked areas. Preserve the original report, then classify findings as confirmed,
duplicate, disproved or unverified. Fix accepted causes through the authorized
writer and recheck affected behavior against the new snapshot. An old report
cannot certify changed source. A clean report does not establish full coverage.

Record exact source/input identity, original brief, reviewer/session identity when
exposed, actual history-inheritance setting and its provenance, commands/results,
original report, triage and remaining limits. Do not invent unsupported host APIs
or claim isolation based only on changing a role name. If a fresh session is
unavailable, label feasible checks as self-review and keep required independence
unverified. Host settings and evaluator logs are not exhaustive authenticated traces.

The test-engineering skill supplies a portable checklist and brief template;
profiles remain usable without that installed skill. [Evaluation records](../evals/README.md)
keep observed reviews separate from case specifications and routing claims.
