# Native evaluations

`scripts/native_eval.py` reuses the existing behavior fixtures to compare ordinary
prompts, explicit skill attachments and named profiles in OpenCode 2.0.27. It is an
optional evaluation tool: normal build, validation, installation and CI need no
AI Skills checkout, host credentials or paid inference. Use Python 3.10+ and a
POSIX host supporting process groups for live trials.

## Prepare without inference

Build exports, then explicitly select skill source and model:

```sh
python3 scripts/build.py --adapter opencode
python3 scripts/native_eval.py prepare --output /absolute/new/trials --skills-source /absolute/ai-skills --agents-export dist/opencode --repeats 2 --model deepseek/deepseek-v4-pro
```

Preparation creates a seeded, frozen 18-run roster: 3 fixtures × 3 modes × 2
repetitions. Starting file hashes match within each case. The skill treatment adds
an explicit request and native skill attachment. Ordinary and skill controls pin
the built-in `build` primary; named-agent trials select the corresponding profile.
This controls the primary agent, rather than testing an arbitrary ambient default.
No skill folder is adapted and no host account/configuration is changed.

The default remains these 18 runs. Select `--case` and `--mode` explicitly for
smaller or broader exercises; each option can be repeated. Additional fixtures
cover the existing canonical `shared-project-context`, `security-isolated-repro`,
`security-secret-evidence`, `architecture-proposed-decision` and
`coordination-missing-delegation` cases. They are read-only. The final case denies
the subagent capability rather than merely describing delegation as unavailable.
Fixture preparation and invariant checks never establish behavioral coverage.

The missing-compiler fixture now supplies `port.contract.check.mjs`, permitted as
`node --experimental-strip-types port.contract.check.mjs` when the existing Node
supports TypeScript. The check is protected from edits and covers 34 accepted and
rejected inputs. No runtime is installed; this check does not replace the absent
required compiler. Such changed-input follow-ups remain separate from historical
matched trials.

Tasks, instruction hashes, source revisions and working-tree inputs are recorded.
Participant workspaces receive native catalogs; expected answers/grader metadata
remain outside them. Inspect all inputs and the generated permissions before running.
These project permissions are not an OS sandbox. The host internally uses the
existing account, while the runner never reads or copies credential files.

## Run a deliberately selected trial

Use an ID from plan.json. Live execution requires an explicit executable, matching
model, time limit and host-reported cost threshold:

```sh
python3 scripts/native_eval.py run --output /absolute/new/trials --id PLANNED_ID --opencode /absolute/path/to/opencode --model deepseek/deepseek-v4-pro --timeout 180 --max-cost 0.15
```

There is no provider fallback, automatic retry or hidden batch inference. Each run
owns a new private localhost server/process group. Preflight checks actual project,
resolved primary/model and registered instruction identities before prompting.
Existing partial attempts refuse overwrite. The collector records API messages
without reasoning/thinking, descendant sessions, before/after files and Git staging
entries/index bytes, and source/test invariants. The host disables optional Git
index refresh; focused read-only reviews check index bytes separately from semantic
staging entries. It terminates its owned process
group on completion or interruption. A deadline watchdog also terminates that
owned server group if API polling/response transfer stalls; responses returned
past the deadline are rejected. Shutdown grace and invariant checks have separate
bounded overhead. Detached processes outside that group are not an OS sandbox.
A reported-cost threshold can overshoot due to in-flight work; it is not a hard
billing cap.

Implementation scope checks permit new root test/check files alongside the named
implementation file. They still protect existing supplied tests, owner files and
installed instructions. Review the content and necessity of added tests separately;
a permitted filename is not proof of test quality.

Exit 1 means collection or invariant failure. Exit 2 means collection completed but
task acceptance still needs independent review. Neither exit nor a host `succeeded`
outcome grades review reasoning, a missing compiler, tool-policy compliance or all
side effects. Recorded instruction bodies also do not expose the entire provider
prompt or rule out additional host/global contributions. Treat preflight identity
claims within that scope.

## Review and measure offline

```sh
python3 scripts/native_eval.py report --output /absolute/new/trials
python3 scripts/native_eval_report.py --output /absolute/new/trials
python3 scripts/native_eval_report.py --output /absolute/new/trials --review /absolute/review.json
```

The fixed roster retains failures and unexecuted runs. The optional review file has
`runs` entries with `id`, `result_sha256`, `acceptance` (`pass`, `fail`, `blocked` or
`unverified`) and optional `notes`. It is rejected if the result hash changed.
This binds the supplied assessment to bytes; it does not authenticate the reviewer
or independently validate their judgment. Use the [fresh-review method](FRESH-REVIEWS.md).

## Required offline evidence gate

```sh
python3 scripts/check_evidence.py
```

CI runs this command without a native executable, account, model call or AI Skills
checkout. [The evidence index](../evals/evidence-checks.json) explicitly registers
bundles and their result-bound reviews. The gate verifies each bundle's complete
artifact set and SHA-256 manifest, rejects linked/unsafe paths and malformed JSON,
then regenerates the JSON and Markdown measurements in memory. Changed artifacts,
stale review bindings, omitted failure/missing rows or stale reports fail the gate.
It never rewrites retained evidence. Older formats remain historical rather than
being silently interpreted as current native trials. Manifest consistency does
not authenticate an author or establish the correctness of an acceptance judgment.

Live inference remains an explicitly invoked optional command with model, executable,
time and cost bounds. It is not part of this CI gate.

## Measurement scope

The measurement report keeps per-run values and group mean/range/sample counts,
unknown usage, actual primary agents, resolved skill-body attachments, skill calls
and instruction-file reads. Skill attachments may carry full bodies without a
skill tool invocation; a requested ID alone does not establish loading. Count source
bytes separately from host tokens/cache and cost. Do not sum a parent session's
reported fields again from individual assistant messages; independently compare
those message sums where the host exposes them. Descendant totals and unexposed
auxiliary billing need distinct treatment.

Only finite nonnegative numeric metric samples contribute to statistics. Booleans,
negative/nonfinite/nonnumeric observations and non-dict usage containers count as
missing. Nonfinite values in returned rows become JSON null; failed/missing planned
rows and exact raw-result review bindings remain intact.

These modes change procedures/roles, not just context disclosure. Lower input or
cost does not prove a context-efficiency improvement. Such a claim needs matched
accepted outcomes and a separate context-only intervention with comparable settings,
retained failures and complete accounting. Source trimming without those results
is a source-size change. Repeated native runs also do not increase unique canonical
case coverage when they repeat already observed cases.
