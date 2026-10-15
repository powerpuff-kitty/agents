# Native comparison, context measurement and project pilot

This record retains 18 planned DeepSeek trials: 3 existing fixtures × 3 usage
modes × 2 repetitions. It also retains a separate startup retry, 2 shorter-context
trials and a real AI Agents source-change pilot. These repeat already observed
canonical cases; unique coverage remains **8/144**, with **136 unobserved**.

## What was measured

OpenCode v2.0.27 used `deepseek/deepseek-v4-pro`, resolved variant `default`.
Ordinary and explicit-skill controls pinned the built-in `build` primary; named
trials selected feature-developer or quality-engineer. This controls primary
selection rather than testing an arbitrary ambient default. All 62 skill bodies
and 35 profile bodies were checked against their staged files before inference;
created/resolved session locations and models were checked separately.

The [frozen plan](matched/plan.json) records seed 17, starting source fingerprints,
source revisions, prompt identities and repetitions. Starting files match within
each case. Source snapshots were AI Agents
`cbf7c53fe3f83b438a7d47945760fa38d6f3499c` and AI Skills
`aed7e19f426c315b142111ef846f84d7680f3df3`; working input hashes identify staged
exports/configuration. The later corrections in this release were not inputs to
these runs. Complete provider prompts, backend weight revisions, sampling defaults
and additional host/global instruction contributions were not exposed.

## Outcomes and routing

The original roster has **12 collected sessions, 5 timeouts and 1 startup failure**.
Those are collection outcomes; the independent
[task report](runner-review/final-trial-review.md.txt) and
[result-bound decisions](runner-review/final-decisions.json) assess actual acceptance:
**12 scoped passes, 5 failed deliveries and 1 block**.
[Measurements](matched/measurements.md) retain every planned slot and per-group
sample counts/ranges, including failed or unavailable observations.

- All 6 ordinary controls used `build`, with no observed skill load.
- All 6 explicit-skill trials contain host-resolved attachments with the requested
  skill body. These are actual attachment records, not merely submitted skill IDs.
- The 5 named-profile sessions that started used the requested profile. The
  quality-engineer review also loaded change-review through a native skill call.
- Original run 07 failed during host readiness before a session or model response.
  Its [single bounded retry](startup-retry/plan.json) is reported separately with
  its own source/result hashes and [review](runner-review/retry-review.md.txt).
  It does not replace the startup failure or add an independent planned repetition.

The fixed 180-second/0.15 reported-cost thresholds remain in each trial record.
Timeouts retain partial source, usage and absent final reports. Numeric host usage
fields reconcile with exposed assistant totals where available; interrupted final
requests and unexposed auxiliary operations prevent invoice-complete accounting.
Reported cost thresholds can overshoot while work is in flight. Execution overlap,
cache state and 2 repetitions per cell limit comparisons; no model ranking,
statistical reliability or causal procedure/cost improvement is claimed.

## Context reduction

The [context comparison](context/comparison.json) changes only the debugging
entrypoint content in otherwise matching starting files. Its trigger/frontmatter,
license, guide and supporting fixtures remain intact. Unique temporary paths and
host attachment wrappers differ. Exact source entrypoint bytes changed from
**3,137 to 2,668**, removing **469 bytes (15.0%)**; Markdown body bytes changed from
2,779 to 2,310. Both baseline and both candidate executions passed the original
5 pagination tests, preserved the owner edit and semantic staging, and received
[independent review](runner-review/context-review.md.txt).

Mean host input was 10,725.5 before and 10,651.5 after; mean cache-read tokens rose
from 123,968 to 136,384. Reported cost varied between runs. These small, overlapping
samples support the source/attachment size reduction and scoped observed behavior,
not a causal token/billing saving or general quality-equivalence claim. The reviewed
shorter entrypoint was adopted; unrelated skills were not mechanically shortened.

## Real project pilot and completed correction

The [project task](project-pilot/prompt.txt) requested a staging-identity improvement
in the actual AI Agents source archive through `team-feature`. The native run
selected team-lead, then 1 feature-developer delegate. It timed out after 600 seconds
before regression tests and independent workflow review were completed. Its partial
fix detected staged-entry changes, but legacy missing evidence returned a truthy
`"unverified"` string. Shell-unavailability claims also exceeded the observed
compound-command denials. The [initial independent report](pilot-review/initial-report.md.txt)
retains these findings and the incomplete native result.

The coordinator completed the correction separately: semantic staging uses a hash
of NUL-delimited modes/blobs/stages/paths; unchanged porcelain output cannot hide
changed staged content. Stat-cache refreshes stay distinct. Missing legacy evidence
is a falsey null check; deleted fixture Git metadata fails preservation safely.
Regression and compatibility tests were added. The
[remediation review](pilot-review/remediation-review.md.txt) independently accepted
that focused change, with 10 focused tests and all required checks in its isolated
source copy. Those later checks are not native-run verification. Native-final and
coordinator-final source files remain separate.

## Collector findings and retained attempts

[Original runner review](runner-review/initial-report.md.txt),
[recheck](runner-review/recheck-report.md.txt) and
[final source review](runner-review/final-runner-review.md.txt) keep findings separate
from corrections. Regression tests cover pre-prompt project/model/content checks,
expired admission, partial-attempt preservation, Git deletion/drift, process-group
cleanup, missing usage, cursor handling, startup readiness and report hash binding.

The first 2 live collector attempts failed before any assistant response. Their
recovered session APIs report 0 tokens/cost, not audited billing. The cursor bug
combined `order` with a continuation cursor; the corrected adapter preserves
filters while letting the cursor supply ordering. The original roster then used
that frozen collector until a transient readiness `503`; bounded startup handling
was corrected for the remaining runs. Both versions are retained, with per-result
runner digests. Model inputs and limits stayed fixed. Earlier unused roster slots
remain in their plans; they are not presented as executed trials.

An overly narrow invariant in original run 03 flagged its added verification file.
The reviewer found that adding the test was authorized; its failing harness and
unfinished report remain actual task findings. The corrected collector permits
new root verification files while protecting existing inputs.
[Scope corrections](matched/scope-corrections.json) do not alter original checks,
results or task verdicts. A completed tool wrapper can contain a nonzero exit or
metadata error; the report preserves those failures separately from host status.

The later [guard recheck](runner-review/guard-recheck.md.txt) assesses an owned-server
deadline watchdog, post-deadline response refusal, disabled optional Git refresh and
separate literal-index checks for read-only reviews. An actual OpenCode server
[deadline smoke check](guards/native-guard-smoke.json) submitted no prompt/model
call. These changes do not rewrite older timeout or index-preservation observations;
the startup retry's strict index-preservation verdict remains unverified.

Current OpenCode adapter guidance also distinguishes denied compound commands from
missing executables and failed inner checks from wrapper completion. Source tests
and registry checks of that later guidance do not prove model adherence to it.

## Evidence boundaries

Public copies retain prompts, messages, sessions, preflight records, file/staging
identities, final small fixtures and reviewer decisions. Full staged catalogs, Git
internals and the duplicated project checkout are omitted. Initial small fixture
files were regenerated offline and checked against retained before hashes; they
are not substituted for final outcomes. Source commits plus hashes identify the
remaining resources. Original reviewer Markdown is retained verbatim with a `.txt`
suffix so original local references are not represented as working published links.
The export provenance records original paths and byte identities.

The coordinator spawned both independent reviewers with `fork_turns=none`; follow-up
reviews reused those sessions. Settings and retained records do not authenticate an
exhaustive action history. Reasoning/thinking parts, credentials and private
provider inventories are not published. Project permission rules are not a sandbox.
Historical collectors in this folder use local paths and existing accounts; they
are evidence, not automatic CI jobs or general-purpose installation recipes.
Use the [maintained runner guide](../../../docs/NATIVE-EVALUATIONS.md) for new work.

[manifest.json](manifest.json) hashes published artifacts, excluding itself.
Checksums detect changed bytes, not publisher identity. Outstanding broader routing,
architecture/protected-truth coverage and complete usage-accounting requirements in
[issue 26](https://github.com/powerpuff-kitty/ai-skills/issues/26) remain open.
