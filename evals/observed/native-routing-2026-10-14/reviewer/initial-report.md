# Independent initial native OpenCode trial review

Scope: frozen collectors, permitted three prompts/native-initial manifests/workspaces, three completed default attempts and completed DeepSeek implementation attempt. DeepSeek review and missing-tool did not have run.json when this report was prepared and are not assessed as completed. No desired verdict was supplied. This report is also retained as initial-report.md for follow-up comparison.

## Assessment

The evidence does not establish successful native catalog routing or any completed fixture task. All three default attempts fail before tool execution with a provider quota refusal. The DeepSeek implementation attempt executes tools but operates on the real TCSN checkout rather than its fixture, then times out. These are distinct outcomes: provider refusal, wrong-project activity, and timeout; there is no observed tool permission rejection in that completed implementation trace.

### F1 — High: fixture isolation did not hold in the completed DeepSeek implementation attempt

`implementation/attempt-deepseek/run.json` records cwd `/private/tmp/native-routing-2026-10-14/implementation/workspace`. Nevertheless, zero-based events 1–3 in its events.json read the real TCSN manifest, README, and tcsn-change skill under `/Users/tcsntcsn/TCSN/tcsn.io`. Event 6 invokes `skill` with id `tcsn-change`; events 7/10–13 search real TCSN code, and event 18 executes a shell command explicitly changing to that real checkout. Subsequent shell calls (22,25,37,45,48,62,66,69,88) continue there; event 25 also searches `/Users/tcsntcsn/TCSN` for labels.txt. All 42 tool uses are recorded completed (15 read,13 grep,10 shell,3 glob,1 skill). No fixture source edit or fixture test invocation is visible.

Counterevidence/limits: the launcher really records the fixture cwd and the installed fixture config says external_directory deny, scoped shell allow rules and 10 steps per configured agent. The trace still has 25 step_start/24 step_finish. This makes applicability of that config and the recorded working directory uncertain; it does not identify the cause or prove an OpenCode permissions defect. Inherited host/session context, configuration loading and host behavior were not investigated. No outside-repository source was independently inspected as part of this review; the relevant evidence is the retained trace.

Effect: this attempt cannot validate ordinary fixture-driven catalog selection. The actual visible skill invocation is tcsn-change from outside the fixture. No subagent/delegation call or installed-role choice is observed. The default agent identity is not exposed. There is no independent proof that the fixture catalog was discovered by the host merely because it exists on disk.

### F2 — Default attempts are blocked by provider quota, not failed fixture reasoning

Each root events.json contains exactly one step_start and one error, no tools, no assistant outcome, no step_finish usage. All exit 1 without timeout: implementation 1.108s, review 1.022s, missing-tool 1.186s. The error is `provider.quota`, HTTP429, Google free-tier quota limit0, identifying the provider-reported model alias `gemini-4-argon`. That alias is error evidence, not a verified complete configured model identifier or successful served model. Quota refusal is not an authentication audit or evidence that all credentials/providers are healthy or unhealthy. Exact usage and billing are unknown, not zero.

### F3 — Completed DeepSeek implementation did not fix pagination

The command explicitly requested `deepseek/deepseek-v4-pro`; no --agent override was supplied. Host version is recorded `opencode v2.0.27`. The attempt exits130 after180.161s, timed_out true. Last event91 is a transport socket error; without a control trace its causal relation to collector termination is uncertain. No final text event or completed task claim exists.

The original 359 source/catalog files match native-initial.json; labels.txt still reads `Continue to next page — owner edit`. A copied-workspace `python3 -B -m unittest -v` runs5 tests and fails2 (`test_exact_first`, `test_exact_last`), with3 passing. pagination.py:6–7 still drops the final exact-size page. This independent check establishes the unresolved fixture bug, not an agent-executed test result.

Observed step_finish usage across24 completed steps sums input73233, output3600, cache-read1084416, cache-write0, reported cost0.098600172. These are trace-reported partial sums; the terminal step lacks step_finish, and no billing currency or invoice verification is supplied. The requested model string is known; successful backend model identity, sampling/reasoning settings and overall usage remain unknown.

## Setup evidence and preserved fixture state

The two frozen collectors match both script-sha256.json and their original collector copies: run_trials.py `9d359109612df34323a926391dab130203f70e92fa4613f8823030493913ff23`; run_deepseek_trials.py `6698b95d4ecc07456ef3048c94fae75e07366e49c79b5de2dcbc90c161ce7b8a`. Both call opencode run --standalone --format json --auto with fixture cwd, command-local autoupdate:false, timeout180s, terminate then kill if needed. DeepSeek adds only the explicit model flag. Ordinary prompts do not assign profile/skill names. Each fixture has35 profile Markdown files and62 SKILL.md files, and the manifests record agents revision942fa2e284d83d13c74a2e56d40e4dd48c741fb7 and skills revision7d5238fe346412bba05623baaacc2c04c0ddfa41. Those revisions are recorded provenance, not independently validated commits.

The collectors exclude reasoning/thinking parts from JSON retention. Trace excludes those by design; discarded-event count0 is not evidence that no internal reasoning occurred. Collectors inherit the environment and do not record resolved runtime directory/config/agent/settings. They do not provide sandbox isolation. The review did not execute either collector.

Original manifest comparisons match359 implementation,360 review,359 missing-tool files with no additions. Original review index hash at review entry is `e6543ddab9763656ce754fabad3835bcee0d268842405e25fd2c608d3934c3a7` and remains unchanged during reviewer actions. There is no pre-attempt index hash in native-initial.json, so this review cannot independently prove its pre-run byte identity.

Reviewer copy checks confirm the review fixture contains staged pricing.py and unstaged display.py plus new checkout.py. Concrete defects for the later review outcome comparison: pricing.py:2 subtracts percentage points as dollars (`quote(3,50,10)` returns140, expected135); display.py:2 divides dollars by100 (`dollars(90)` returns$0.90, expected$90.00); new checkout.py:4 exposes that display defect. Its 2×50,10 example coincidentally gives the correct numeric discount result90 and alone does not expose the pricing defect. These are reviewer findings, not findings produced by an unavailable native final answer.

The missing-tool fixture's port.ts:2 remains `return Number(value)`, incompatible with CONTRACT.md's boolean/blank/fractional/string-format/range rejection requirements. A disposable-copy `command -v standalone-pilot-tsc` exits1 without output. No compiler, runtime substitute or full TypeScript validation was run, and no missing-tool native recovery is yet assessed.

## Boundaries and next review step

No model/network/provider call, installation, commit, publication, original source/index/result edit, personal configuration/auth read, model-preflight.json read or unrelated temp/repository inspection was performed. All executable fixture checks ran in reviewer/copy-* directories. Exact argv, stdout, stderr and exits are in checks.json; manifest/artifact hashes and observed trace statistics are in evidence.json; after-check preservation is in preservation.json.

Read-only repository entrypoint files required by the enclosing user instructions were also read: .agentic/README.md, .agentic/manifest.yaml and .agents/skills/tcsn-change/SKILL.md. This does not apply that implementation workflow to the fixture review. Initial commentary incorrectly referred to denied shell calls; it was corrected after exact trace parsing. No permission failure is claimed in this report.

Await completed run.json for later DeepSeek attempts. Before any further model rerun, independently verify effective fixture directory/config and catalog discovery using bounded non-provider checks, then retain those results; otherwise wrong-project activity confounds any routing verdict. No rerun is performed or authorized by this review itself.
