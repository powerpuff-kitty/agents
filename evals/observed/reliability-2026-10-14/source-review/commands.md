# Commands and inspection log

Initial read-only commands (all exited 0 except the noted first ls):

- ls -la on the three scoped skill directories and output directory: exit 1 because output directory did not yet exist; scoped directories present.
- rg --files over the three scoped skills and canonical agent-work/project-memory directories: exit 0.
- git diff in agents scoped to scripts/behavior_eval.py, tests/test_behavior_eval.py, shared/operating-contract.md and initially security-auditor/instructions.md: exit 0; final path corrected to agents/security-auditor/instructions.md and diff read separately.
- Python -B and cat source reads of all non-LICENSE files in the three skills, named evaluator/test/contract/security role; bounded tool-output truncation was followed by focused re-reads.
- git status --short -- structured-reflection project-memory agent-security-review (skills repo): all three untracked.
- Canonical reflection.v1.schema.json, project-memory/README.md and memory.v1.schema.json read.
- Snapshot command: Python 3 -B standard-library SHA-256 over scoped sources and the two allowed canonical contract trees.

Subsequent exact probe commands are retained as .py artifacts, with JSON/text outputs. No command in this review intentionally writes to a repository.

## Executed scoped tests and probes

1. `mkdir -p /private/tmp/reliability-source-review-2026-10-14/unit-tmp` — exit 0.
2. From `/Users/tcsntcsn/TCSN/agents`: `TMPDIR=/private/tmp/reliability-source-review-2026-10-14/unit-tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 python3 -B -m unittest discover -s tests -p test_behavior_eval.py -v` — exit 0, 4 tests passed in 1.077s. Passed: boundary fixture fail/fix/owner-edit detection; readonly source-mutation detection; output no-overwrite; discovery staging and instruction-mutation detection. This ran the source current at that point; no claim for later edits.
3. `python3 -B /private/tmp/reliability-source-review-2026-10-14/probe.py` — exit 0. Exact probe source retained. Compiles a reconstructed earlier evaluator and a captured current evaluator; substitutes a synthetic root/roles and revision string, copies only three allowed skill sources, performs no git/model/provider/network action. Twelve staging/grade combinations (three cases x two modes x two source versions). Results: prior discovery omitted catalog for all three; captured current discovery included it for all three. Shared contract staged but not referenced by task/catalog in all six discovery outputs. All baseline workspace/instruction checks true; all twelve deliberately mutated workspace fixtures detected. See probe-results.json. Explicit-mode role.md appends the shared contract; absence of a standalone shared-contract path in explicit mode is expected.
4. Python 3 -B import of the scoped `gateway.py` and four pure `authorize` calls — exit 0. Supplied forged approval accepted (True), benign allowed read accepted (True), unapproved disallowed tool denied (False), allowed tool with an unlisted destination accepted (True). Intentionally vulnerable fixture only, no model/action boundary integration executed. See gateway-probes.json.
5. Python 3 -B hash recheck — exit 0. See source-hashes-recheck.json for drift after initial capture.
