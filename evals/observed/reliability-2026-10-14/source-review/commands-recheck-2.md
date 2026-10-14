# Narrow recheck commands

- Python 3 -B stdlib hash snapshot over the same 93 files from the initial manifest. Wrote `source-hashes-recheck-2.json`; printed changed scoped source with line numbers. Bounded truncation followed by focused reads. Exit 0.
- `cat` of scoped test_behavior_eval.py and agent-security report template; `sed -n '99,107p'` of scoped evaluator; Python -B JSON parse/list of fixture memory identities/statements/lineage. Exit 0. No other reviewer outputs read.
- The exact unittest argv, cwd, environment overrides and exit are retained in unit-recheck-2-command.json; stdout/stderr are retained in unit-recheck-2.log. Exit 0, 5 tests. Temp writes constrained under this review directory with TMPDIR, and global/system Git config disabled.
- `python3 -B /private/tmp/reliability-source-review-2026-10-14/probe-recheck-2.py` — exit 0. Exact source retained; synthetic role/root/revision substitution, three scoped copied skills, six case/mode combinations, baseline invariants and deliberate workspace-mutation detection. No git/model/provider execution in this probe.
- Python 3 -B parsed all 12 case specifications, asserted 12 not-run cases each with at least 2 criteria, wrote case-spec-recheck-2.json, and rehashed all 93 files. No source drift during recheck; see source-hashes-recheck-2-end.json. Exit 0.
