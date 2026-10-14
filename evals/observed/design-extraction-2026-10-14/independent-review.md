# Independent design-extraction and design-analyst review

Original review, retained before feedback. Date: 2026-10-14. Scope: raw current source in the Skills and Agents repositories, with applicable project instructions and relevant callers. The supplied brief is retained separately at `/private/tmp/design-extraction-independent-brief.txt`. This report does not incorporate another review, an author narrative, an intended verdict, or prior retained evaluation outcomes.

## Result

One actionable integration regression: the new core member makes a required existing selection test fail. I found no additional concrete correctness or permission defect in the reviewed extraction procedure, profile, and scoped handoff contract. This is a source review with limited deterministic checks, not observed proof that a model produces complete usable reports or obeys the procedures.

## Finding F1 — P2: update the combined-selection assertion for the expanded core catalog

Location: `/Users/tcsntcsn/TCSN/agents/tests/test_selection.py:28`; trigger introduced by `/Users/tcsntcsn/TCSN/agents/packs/core.json:9`.

Adding `design-analyst` raises the core roster to 16 profiles. The existing test selects `core` plus the separately owned `financial-analyst`, but still asserts that the combined export contains 16 profiles. The current export correctly contains 17. The documented completion suite therefore fails despite valid selection/build behavior. Reproduction:

```sh
cd /Users/tcsntcsn/TCSN/agents
python3 -m unittest discover -s tests -p test_selection.py -v
```

Observed: 5 tests run, 4 pass, `test_combined_selection_deduplicates_and_rejects_unknown` fails with `AssertionError: 17 != 16` at line 28. Update the test to derive the expected unique selected roster or deliberately update its count, while preserving its duplicate-selection and unknown-ID checks. Rerun that test and the repository-required suite. This is a test regression, not evidence of a broken profile export. Its reviewed source hash is recorded below; concurrent changes can supersede it.

## Assessment against the requested use

- Capture coverage is defined before collection. The procedure distinguishes actual runtime observations from source declarations, design metadata, screenshots and inferred behavior. Unknown fonts, roots/device units, hidden states and responsive behavior retain explicit limits.
- Taste is descriptive and evidence-linked rather than a universal quality score. Candidate semantic mappings, internal source-system existence, designer intent and accepted project identity remain distinct.
- Deliverables include a report, taste profile/index, candidate system, supported token exports, evidence manifest and usable examples. Unsupported exports can be omitted with reasons rather than fabricated. The offline HTML rules reject embedded source instructions, imported scripts and unreviewed CSS/URLs.
- Standalone skill links resolve locally, and fallback behavior does not require companion skills or an entire Harness project. The profile also retains a native-method fallback when the extraction skill is absent. Installing profiles does not purport to install skills or change host permissions.
- The new role is owned by core, resolves through explicit selection and the UI team, and renders into portable/OpenCode exports. General team-lead discovery can inspect actual role descriptions. Documentation edits were visibly ongoing, so stale counts or missing role-to-skill prose in those inputs are not raised as findings.
- Scope, consent, private evidence transfer, restricted asset reuse, publication and canonical-identity adoption are bounded by task authority and the shared operating contract. Captured text cannot authorize those actions.
- The DTCG dimension/color syntax example is consistent with the linked 2025.10 format sections I inspected. This is a narrow manual comparison, not a conformance validation of generated tokens. Official source: [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/).

## Actual verification and results

Commands executed against `/Users/tcsntcsn/TCSN/agents` unless noted:

```sh
python3 scripts/validate.py
python3 scripts/build.py --adapter portable --agent design-analyst --output /private/tmp/design-extraction-review-portable
python3 scripts/build.py --adapter portable --agent design-analyst --output /private/tmp/design-extraction-review-portable --check
python3 scripts/build.py --adapter opencode --team team-ui --output /private/tmp/design-extraction-review-opencode
python3 scripts/build.py --adapter opencode --team team-ui --output /private/tmp/design-extraction-review-opencode --check
python3 -m unittest discover -s tests -p test_selection.py -v
```

- Source validation passed: 35 agents, 20 teams, 132 acceptance specifications; host/command loading not checked, model behavior not run.
- Both selected exports built and passed byte freshness checks in private temporary directories. No host installation/configuration was changed. Individual selection contains the named profile; UI-team roster selection resolves the role.
- The selection test command failed as described in F1; four other tests passed. Its tests perform isolated temporary filesystem installs, not a real host install.
- A local Python check parsed both skill JSON files, checked local Markdown targets and verified example profile evidence references. All passed. The check is not JSON Schema, DTCG, fragment/remote-link or rendering validation.
- Git revision/status, raw `cat`/`sed`/`nl` reads and `rg` source/caller searches were used. Early inventory searches enumerated filenames more broadly than the final scope; no prior external audit/evaluation reports or other agents' outputs were opened. Two exploratory reads named nonexistent `tests/test_build.py`, `tests/test_teams.py`, `tests/test_packs.py` and later `tests/test_agents.py`; these returned missing-file errors before actual test filenames were enumerated. Several large raw-source outputs were truncated; the extraction sources were subsequently read separately, and relevant build/team semantics were read in targeted excerpts.
- The official DTCG URL was opened with the web tool and its dimension/color examples located. No package, account, host permission/configuration, secret, commit, push or publication action was performed.

## Limits and residual verification work

No live website/app/Figma traversal, screenshot-only extraction run, HTML rendering, actual generated-report usability trial, native host registry verification, model-routing check, accessibility result or whole-repository suite result is established. The new acceptance specifications correctly remain `not_run`; they do not show behavioral reliability. Full `check_docs.py` was not run because it recursively reads Markdown including retained evaluation material outside this independent review's permitted evidence scope. Only targeted safe tests and temporary exports were used.

The next useful behavioral check is an isolated source-only extraction using the supplied fixture: inspect the resulting evidence/value mappings, theme separation, candidate status, JSON/token shape and an actually rendered offline report. Separate image-only and no-access runs should test the declared uncertainty/fallback behavior. These are residual verification opportunities, not findings of fabricated success.

## Snapshot binding

HEADs alone do not identify the dirty/new source. The SHA-256 table below identifies the raw files used. Capture manifest: `/private/tmp/design-extraction-independent-inputs.json`.

- `/Users/tcsntcsn/TCSN/skills` HEAD `95ff8b5e60997bb34f6ac2262e7e22db899a5ae2`
- `/Users/tcsntcsn/TCSN/agents` HEAD `1c3728db107fab245af9b5523ce3d85bedceea9d`

A post-check comparison detected concurrent changes to `agents/README.md` and `agents/docs/SKILLS.md` after their recorded hashes. Neither carries a finding here. Findings bind to recorded source, not an unreviewed later tree.

| File | SHA-256 |
| --- | --- |
| `/Users/tcsntcsn/TCSN/agents/AGENTS.md` | `e56761619d68df95233a537d245f70d2638c3fde4f7a868123076af3cecead3f` |
| `/Users/tcsntcsn/TCSN/agents/INSTALL.md` | `814d4f2f8a324a4346c743e88abec03b5990ad300291175e3a21f15b4d97929b` |
| `/Users/tcsntcsn/TCSN/agents/README.md` | `98740462f879c8811fc431fba8dbc82c998a4a70d4c314f154beed1596d71270` |
| `/Users/tcsntcsn/TCSN/agents/agents/design-analyst/agent.json` | `b4b91f561b402b1265b57ebfbd23375915b001ce604b470cafc683df17bf1e6e` |
| `/Users/tcsntcsn/TCSN/agents/agents/design-analyst/instructions.md` | `43783822dd88826b7e020f770ab5b09d81a7f6438b8cd167738c7614a602be25` |
| `/Users/tcsntcsn/TCSN/agents/agents/designer/instructions.md` | `897e734e39c0ffe852b12cb2b8e20d15c6e6df145c0e5cfa603059b718b36cd4` |
| `/Users/tcsntcsn/TCSN/agents/agents/evidence-validator/instructions.md` | `fbf301cf159ded606269266db84c6753a77deaa6273ac9741beea7ae1c37b7a1` |
| `/Users/tcsntcsn/TCSN/agents/agents/team-lead/instructions.md` | `55f4b7395679f7e8358e8fdd6743604aed528a31af8dd64ffd80049fed6badb3` |
| `/Users/tcsntcsn/TCSN/agents/docs/ARCHITECTURE.md` | `957897b9e94d93233c7ff2bd145ea0a24b0e15eea78e4a09ac3dbde0780aebd7` |
| `/Users/tcsntcsn/TCSN/agents/docs/SKILLS.md` | `bd519526277ec4df6e71367a9a1c64e182d93b41578e4cc691edd0179a3419cd` |
| `/Users/tcsntcsn/TCSN/agents/evals/behavior-cases.json` | `4b52e34bf8cf898734164a2f02d513a15a8d6a0b62804da235958794330d0708` |
| `/Users/tcsntcsn/TCSN/agents/packs/core.json` | `86bc419d8c8df62470c7a311f9922e3aba9e664a393e4632a77bdb5b215063be` |
| `/Users/tcsntcsn/TCSN/agents/scripts/build.py` | `8c6a077ed7ce44999871c941b0bd2f1039f79c4ed9b730cfe7a57c216328fe83` |
| `/Users/tcsntcsn/TCSN/agents/scripts/check_docs.py` | `9b1992638d0d67e21b4b3d80bec8402faba1180504fd00cea4e06c6117b6584b` |
| `/Users/tcsntcsn/TCSN/agents/scripts/validate.py` | `7418f7426809cac70be98efd22b9df557703c93152a81c05e43ce99b7c6ba798` |
| `/Users/tcsntcsn/TCSN/agents/shared/operating-contract.md` | `25c88a8a48a9f2081348417f0ffed7df4731dc99f34ba84f42104512df397a72` |
| `/Users/tcsntcsn/TCSN/agents/teams/team-ui.json` | `f948b4c6714d7426328414943ad0533e5046f785b3a170e0e35a6ac811e2e76a` |
| `/Users/tcsntcsn/TCSN/agents/teams/team.json` | `93a9d5bfc7ea5d44a42bae624f64a33b7a323d40190388b779f39fa4fe99d135` |
| `/Users/tcsntcsn/TCSN/skills/INSTALL.md` | `c0fa4abdc7830a71870683223366b00e97a854e11e8c71e485120cb9ae93d694` |
| `/Users/tcsntcsn/TCSN/skills/README.md` | `465cbe27fb9d5fa713c9dca5121fe4129ce5265fd4970c9369870452e86d74ab` |
| `/Users/tcsntcsn/TCSN/skills/design-analysis/SKILL.md` | `c51f532e488bd02a0fe51c97dc42e033c07cb50e6d198d371609fb1b75b27847` |
| `/Users/tcsntcsn/TCSN/skills/design-extraction/LICENSE` | `da8e7b98c9f5547396031dd15ffe7a820eb8c2b9e4d1b32c9eb69bbc0d2c5af4` |
| `/Users/tcsntcsn/TCSN/skills/design-extraction/SKILL.md` | `861c7dd239eb5b7805555b46ced205be3745b6d722bb4f3003cfb5cddc53ffd1` |
| `/Users/tcsntcsn/TCSN/skills/design-extraction/assets/report-template.md` | `f1041f0e64e2f2694e1182b738d1e6c99d5e67839a9b2419fa019f8280ec1f70` |
| `/Users/tcsntcsn/TCSN/skills/design-extraction/assets/taste-profile.example.json` | `f190b7eb9db8152052248b46fa71831958e03b5c362a6d12accd7cb70d6b96d7` |
| `/Users/tcsntcsn/TCSN/skills/design-extraction/references/capture-and-report.md` | `4e4c9c6a261e12089b54266b69960f7d7f99a47acd59ea0d85c34c75e3d63e44` |
| `/Users/tcsntcsn/TCSN/skills/design-extraction/tests/cases.json` | `3e823ab33f0f11060a44047debaaad523744f147f915dbb31147255690b0a012` |
| `/Users/tcsntcsn/TCSN/skills/design-extraction/tests/fixtures/reference.css` | `7e81a04148dd881f97f853c448cc7ad553b19232ed59ff3d0f681a29f82b1c6b` |
| `/Users/tcsntcsn/TCSN/skills/design-extraction/tests/fixtures/reference.html` | `6e75166cb6bffaa59196fe7c60c2c7d514c96a91217717c1bf959e6e22285e76` |
| `/Users/tcsntcsn/TCSN/skills/design-intelligence/SKILL.md` | `b7ccd86fed223329f37f38261f9b09a5c7e703859bd1456655c795d70afe581f` |
| `/Users/tcsntcsn/TCSN/agents/tests/test_selection.py` | `b290d224c5ab1e5eb99aced8c6e66871e4a993853e766a74f878f6e96d66e098` |
| `/Users/tcsntcsn/TCSN/agents/tests/test_workflows.py` | `e7e41c6faffaaff92323f5bedc3ccb677b4a0278e61efa92b62f33bb3c85a2bd` |
| `/Users/tcsntcsn/TCSN/agents/tests/test_audit_regressions.py` | `c412d68bff8de2055a8fc004f82bb2977b4b2ef4ca1dbaac0beab8ee3a39dd19` |
| `/Users/tcsntcsn/TCSN/agents/tests/test_behavior_eval.py` | `3c5cf6c3d916c2cef41e23ea3a9135b1272146348af0ba40299e3d676428b375` |
