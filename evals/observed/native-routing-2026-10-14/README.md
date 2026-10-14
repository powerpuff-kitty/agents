# Native OpenCode ordinary-prompt trials

On 2026-10-14, OpenCode v2.0.27 ran 3 ordinary fixture tasks using the
user-selected `deepseek/deepseek-v4-pro` (resolved variant `default`). No prompt
named a specialist or skill, and no agent override or skill attachment was sent.
Each corrected session verified its actual project location, all 62 skill bodies
and paths, all 35 profile bodies and their step limits before the task prompt.
The built-in primary `build` agent had a 10-step limit.

**No corrected run invoked a skill or subagent or selected a custom profile.**
These runs demonstrate native inventory visibility and built-in agent behavior;
they do not demonstrate execution of the installed catalog instructions. Use a
named profile or team command when deliberate specialist selection is needed.

## Corrected outcomes

| Task | Observed result | Limit |
| --- | --- | --- |
| implementation-dirty-worktree | Only pagination.py changed; existing 5 tests pass; owner label/test files preserved | 1 small fixture |
| focused-review-with-skills | Identified staged percentage defect, unstaged dollar-format defect and effect on new checkout caller; no source changes | Runtime Python command denied; unittest discovered 0 tests and exited 5; exact pre-run index bytes were not captured |
| implementation-unavailable-check | Only port.ts changed; required compiler failed to run; final answer disclosed no compile/runtime validation | Claimed no TS runtime despite discovering Node 24 and Bun; available binaries were blocked from runtime execution by policy. Reviewer later ran 46 runtime cases, not the required compiler |

The host marked all 3 sessions `succeeded`. That is a session outcome, not an
acceptance verdict. In particular, the missing-tool trial retained an unmet
compiler check and a false availability explanation. The independent
[corrected report](reviewer/corrected-report.md) and its checks assess the tasks.
These repeat 3 already observed canonical cases: coverage remains **8/144**,
with **136 unobserved**. They do not establish statistical reliability, provider
comparison or successful automatic catalog routing.

[summary.json](summary.json) records actual tools, timing and host-reported usage.
Model/provider IDs and variant were resolved before prompting and recorded in
assistant messages. Backend weight revision, hidden defaults and invoice-level
cost are not established. Usage is the session API's reported totals; unrelated
background operations are not an audited part of those totals.

## Attempts retained separately

- `attempts/default-quota/`: 3 default-model attempts returned provider quota
  HTTP 429 (Google error alias gemini-4-argon, limit 0) before any model response.
  These are provider refusals, not failed fixture reasoning; usage is unknown.
- `attempts/misbound-deepseek-implementation/`: the CLI launcher recorded fixture
  cwd, but the host read an unrelated portfolio checkout and timed out after
  180 seconds. No fixture edits occurred. Full unrelated tool inputs/outputs are
  withheld; the original trace hash, run metadata and derived statistics remain.
  The portfolio was clean after the coordinator stopped its own processes.
  A partly started review had no completed run record; the third CLI task did not
  start. Neither counts as a completed trial.
- `attempts/preflight-v1/`: explicit binding was verified, but an overly strict
  comparison rejected the host-added model variant `default` before prompting.
  The corrected collector compares provider/model ID and retains the variant.

The corrected runner sets cwd and PWD and supplies an explicit native API
location, then checks the created/resolved session and loaded instructions. These
changes were combined; the evidence does not isolate the original binding cause
or prove a host permission defect. Project permission rules are not a sandbox.

## Evidence and reproduction limits

`corrected/<task>/` retains ordinary prompts, API messages, final sessions,
pre-prompt resolution and inventory, before/after file hashes, initial/final small
fixture files and original source identity manifests. Full staged catalogs and
Git internals are omitted to avoid duplicating the collections. Source archives
at AI Agents `942fa2e284d83d13c74a2e56d40e4dd48c741fb7` and AI Skills
`7d5238fe346412bba05623baaacc2c04c0ddfa41` retain those exact sources.
[source-identity-check.json](source-identity-check.json) records comparisons of
296 skill files, 35 exported profiles and 20 commands against those independently
checked release consumers. Initial/final hashes exclude `.git`; review staging
semantics match the original fixture, while byte-identical index preservation
remains unverified without a pre-run index hash.

`collectors/` contains frozen historical ad hoc collectors, including failed
versions. They use local absolute paths and existing host credentials internally;
**do not execute them as general-purpose installers or CI gates**. The original
CLI collectors do not fail their own process when a trial fails. The corrected
collector's exit indicates collection completion, not task acceptance. Recreating
a paid run requires deliberate new output paths, exact source staging, reviewed
permissions, explicit model/budget authorization and a separately checked result.
The installed host's OpenAPI schema supplied the actual API contract; no API
response containing personal provider inventory or credentials is published.

Reasoning/thinking parts are excluded from the retained traces by design. No
credential/configuration files were read or copied by the collectors. The fresh
reviewer was spawned with history inheritance disabled (`fork_turns=none`); the
follow-up reused that independent session. Its original report is retained before
coordinator triage. The report and isolation setting are evidence, not a claim of
an authenticated exhaustive audit log. [manifest.json](manifest.json) hashes the
published artifacts; hashes detect changes, not publisher identity.
