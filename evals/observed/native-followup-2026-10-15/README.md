# Native reliability follow-ups — 2026-10-15

These are separate bounded DeepSeek/OpenCode executions after the
[previous comparison](../native-comparison-2026-10-15/README.md). Original failures
remain unchanged. Native host completion, artifact preservation and independently
accepted task delivery are distinct.

## Trial outcomes

| Exercise | Planned | Independent pass | Independent fail |
| --- | ---: | ---: | ---: |
| Earlier failed-delivery follow-ups | 5 | 4 | 1 |
| Previously unobserved canonical cases | 5 | 4 | 1 |
| Separate corrective runs | 2 | 1 | 1 |

The initial named port implementation passed the supplied 30-case check but failed
a review probe: formatting a rejected object invoked its conversion hook and could
throw Error instead of the required TypeError. The strengthened 34-case check
reproduces that defect against the original source. The separate implementation
correction passed those checks and independent supplemental probes. The required
TypeScript compiler remains unavailable; runtime evidence is not compilation.

The architecture case and its correction both fail acceptance. They recommend a
relevant in-process boundary and preserve accepted ADR history, but overstate file
inspection and the guarantee established by a documented, unimplemented storage
primitive. The shared inspection guidance was clarified; these observations do
**not** establish that the guidance fixed the behavior. No further retry is hidden.

The [coverage index](index.json) records **13 observed and 131 unobserved cases**
out of 144 canonical specifications. The 5 new executions cover current project
context, isolated tenant authorization, sanitized logging evidence, proposed
architecture and unavailable delegation. Failed acceptance still counts as an
observed execution, never as success. Repetition, installation checks and the project
pilot add no unique canonical coverage.

The secret-evidence trial has no literal synthetic canary in its retained outputs.
A reviewer later displayed the synthetic constant while reading collector source;
that separate incident is disclosed in the correction report. The coordination case
has an actual host/session subagent-deny rule and no children. It truthfully reports
serial self-checks and a failing test; an attempted rejected delegation was not
observed, so exercised enforcement remains unverified.

## Project pilot

The real-project pilot uses a public AI Agents checkout and its updated coordinator
instructions to harden malformed measurement handling. It preserves owner work and
staging and separates a writer from a native quality reviewer. Initial and continued
runs, final source snapshots, actual gate results and external acceptance are
retained under `project-pilot/` and `pilot-review/`.

The first 847-second turn produces the source and initial independent review but
hits its coordinator step bound before 4 mandatory export gates. Its corrected
source has 77 tests. A first continuation collector returns after 1.467 seconds
while the resumed session still has its previous succeeded state; only the new
user prompt is retained, so this is **not** a completed model turn. The separate
v2 collector requires a new assistant completion and idle event before accepting
terminal state. Both original collector versions and records remain visible.

V2 completes in 405.387 seconds with all 7 actual gates passing, a new independent
quality recheck and a final iteration-reviewer assessment. External fresh review
accepts the exact source, owner/index preservation and final delivery evidence.
Only generated exports change during continuation; they match independent builds.
The metric correction is integrated into the repository separately from these
retained source snapshots.

**Full team-feature preset compliance remains incomplete:** no initial framing
review or conditional-stage skip reasons were recorded. The native iteration
reviewer's blanket shell-denial claim is unsupported by its 2 rejected compound
commands; other actors successfully ran separate permitted commands. The final
delivery has a minor count typo: actual report tests are 11, with 6 added, rather
than its stated 10 with 7 added. These qualifications do not erase the actual
passing gates or independently accepted source, and no complete preset-reliability
claim is made.

The external review's first 77-test run also retains a PermissionError during
unchanged process-group cleanup. The isolated cleanup test and subsequent full
suite pass; the cause remains unverified and this change does not claim to fix it.

## Installation exercise

The disposable installer exercise checks scoped dry runs, conflict protection,
authorized replacement backups, modes, repeat idempotence and preservation across
partial selections. It touches no real user installation. The original different-
selection assertion was tautological; the separate recheck corrects it, and the
independent replay verifies the target behavior from actual bytes/modes/state.

The dry-run no-write claim applies to installation destinations. Ordinary Python
can create source bytecode caches; the independent cold `python3 -B` replay also
preserves the full bounded source/target tree. No universal absence of transient
or outside-tree writes, concurrency safety or crash-recovery guarantee is inferred.

## Identity, review and reproduction

The [native guide](../../../docs/NATIVE-EVALUATIONS.md) describes optional execution
and required offline verification. Each trial has a frozen plan/prompt, source and
instruction hashes, actual location/model preflight, API trace, final files and
Git identities. Explicit `deepseek/deepseek-v4-pro` and OpenCode 2.0.27 are used;
ordinary controls select built-in build, while named cases select their recorded
profile. Skills are registered natively; registration is not automatic use.

Fresh external reviews use explicit `fork_turns: none`; their original reports,
source identities and commands remain separate from coordinator dispositions.
Native child session IDs and messages are retained, but a role name or parent ID
alone does not prove history isolation. Decision wrappers preserve the reviewer's
entries and identify original decision bytes; binding authenticates consistency,
not reviewer identity or judgment.

`export-provenance.json` distinguishes copied artifacts and reconstructed initial
port input verified against original before hashes. Full native catalogs, duplicate
instruction trees, `.git`, generated exports and the duplicate full project checkout
are omitted. Source revisions and actual file/body hashes identify those inputs.
Reviewer Markdown reports retain verbatim bytes as `.md.txt` because their private
local links are historical context, not published link targets. `manifest.json`
seals published artifacts; run `python3 scripts/check_evidence.py` from the repository
for offline integrity, binding and report regeneration without inference.

Usage is exposed host accounting, not an invoice. Continuation session totals
include earlier turns and must not be added to the original totals again. Hidden
auxiliary calls, provider weights/settings and complete prompts remain unknown.
No causal cost saving, statistical reliability, exhaustive action trace or complete
catalog qualification is claimed. See [finding dispositions](disposition.md).
