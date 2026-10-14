# Targeted follow-up verification — design extraction integration

Date: 2026-10-14. This is follow-up verification with the original finding history, not a fresh blind audit. The original report and brief are retained unchanged at `/private/tmp/design-extraction-independent-review.md` and `/private/tmp/design-extraction-independent-brief.txt`.

## Result

Original finding F1 is resolved in the recorded current source: `tests/test_selection.py:28` now expects 17 profiles for `core` plus the separately owned `financial-analyst`; all 5 selection tests pass. All 24 workflow tests also pass. No additional concrete integration defect was found in this targeted recheck.

The current core roster has 16 unique profiles including exactly one `design-analyst`. Both portable and OpenCode core exports include the role and its assignments in the general and UI team briefs. `teams/team.json` includes exactly one conditional design-analyst candidate for an explicit extraction/profile/report task. `teams/team-ui.json` retains the scoped artifact writer and sequences its report before independent checks. These are instruction and export results, not actual model routing or scheduler guarantees.

## Commands and actual results

Run from `/Users/tcsntcsn/TCSN/agents`:

```sh
git rev-parse HEAD
git status --short
python3 -m unittest discover -s tests -p test_selection.py -v
python3 -m unittest discover -s tests -p test_workflows.py -v
python3 scripts/validate.py --pack core
```

- Selection suite: 5 tests, all passed.
- Workflow suite: 24 tests, all passed, including general catalog routing, conditional adaptive mutation rules, pack selection/dependency filtering, deterministic exports, installation isolation and preservation, and mock command-loading/location checks.
- Core source validation: passed; 16 profiles, 8 teams, 132 catalog acceptance specifications. Actual host loading and command loading remained `not_checked`; model behavior remained `not_run`.
- Additional direct Python checks used `build.compile_profiles` for both adapters with `packs=['core']`: passed unique roster count, exactly one design-analyst profile, and presence of `Agent: design-analyst` in both general/UI team outputs. They also checked that the general-team design-analyst condition is not `always` and that the UI report stage precedes independent checks. No persistent exports were written by this check.
- Raw targeted `cat`, `sed` and `rg` reads inspected the requested test/team/core sources; broad search output was occasionally truncated, while the relevant assertions, assignment and ordering were subsequently checked directly from parsed source.
- Source hashes were captured before test execution and compared afterwards: none of the recorded files changed during these checks.

The tests create disposable files and isolated temporary installation targets. No installed host, account, package, permission configuration, secret, tracked source, commit or publication was changed. No earlier external review/evaluation output or another agent's output was used.

## Limits

This recheck does not establish a full repository test-suite result, native host registration, model adherence, fresh-review behavior, actual extraction report quality, HTML rendering, or accessibility. Mock host tests are not live host verification. Other prior review limits remain applicable.

## Current snapshot

Agents HEAD: `1c3728db107fab245af9b5523ce3d85bedceea9d`. Dirty/new sources are identified by these hashes rather than HEAD alone.

| File | SHA-256 |
| --- | --- |
| `tests/test_selection.py` | `189fbf776babeaef4d3253cf1f0e6e261d6fc727989ff686996a6e92f22aef4e` |
| `tests/test_workflows.py` | `e7e41c6faffaaff92323f5bedc3ccb677b4a0278e61efa92b62f33bb3c85a2bd` |
| `teams/team.json` | `e79815ed35b29ac5a65546682613fcbbc6020fe8d6fcc4d1258d1a3dab436ac1` |
| `teams/team-ui.json` | `f948b4c6714d7426328414943ad0533e5046f785b3a170e0e35a6ac811e2e76a` |
| `packs/core.json` | `86bc419d8c8df62470c7a311f9922e3aba9e664a393e4632a77bdb5b215063be` |
| `scripts/build.py` | `8c6a077ed7ce44999871c941b0bd2f1039f79c4ed9b730cfe7a57c216328fe83` |
| `scripts/validate.py` | `7418f7426809cac70be98efd22b9df557703c93152a81c05e43ce99b7c6ba798` |
| `agents/design-analyst/agent.json` | `b4b91f561b402b1265b57ebfbd23375915b001ce604b470cafc683df17bf1e6e` |
| `agents/design-analyst/instructions.md` | `43783822dd88826b7e020f770ab5b09d81a7f6438b8cd167738c7614a602be25` |
