# Initial independent change review

Verdict: no actionable defect confirmed in the reviewed uncommitted changes. This is bounded source/test evidence, not certification of the repository or later source edits.

## Brief and context

The verbatim initial brief is retained in `/private/tmp/review-agents-changes-brief.txt`. I received a scoped review task, read raw repository instructions/source/diffs, and did not receive an author walkthrough, earlier findings, prior audit reports, or desired verdict. I did not read external audit reports or historical evaluation conclusions. This reviewer session did not author the changes. The precise spawning/history-inheritance invocation is not exposed within my task input; the coordinator must retain that provenance. I cannot independently authenticate isolation or a complete action history.

Repository: `/Users/tcsntcsn/TCSN/agents`.
HEAD: `f374ffbb543595486c8c5145884c123d77e88020`.
The working-tree content, including untracked files, is authoritative for this report. Hashes below were recorded during review and rechecked unchanged after the focused probes.

## Scope and findings

Reviewed all changed source/documents/tests shown in the recorded inventory, plus root AGENTS.md/README.md and the unchanged adapter renderers and relevant team/pack callers. Changes add export/install license retention, explicit UTF-8 I/O, exact generated-byte comparisons, state-file mode preservation, fresh-review instructions and four unexecuted scenario specifications.

No confirmed finding with a demonstrable trigger, impact and changed-source cause was found. Relevant counterevidence:

- Both adapters export LICENSE and include it in source/output hashes. Installation tracks the notice in populated profile/command destinations. A conflicting command notice rejects before creating the profile destination; explicit replacement backs up the original notice.
- Locally edited notice protection applies during subsequent selections. Replacing it preserves a private management-state mode, retains prior roles/commands, and a repeated selection has no changes.
- Exact byte drift, including CRLF output drift, is tested. The locale regression checks passed in the suite.
- Fresh-review guidance distinguishes requested independent review, self-review when isolation is unavailable, snapshot limits, original report retention, and actual invocation provenance. The four new acceptance scenarios remain `not_run`; prose does not claim those model executions occurred.

## Actual checks

All checks ran under Python 3.14.7 on this macOS environment, from the repository, using disposable directories for installation and standalone build output.

1. `python3 -B scripts/validate.py` — exit 0; 34 agents, 20 teams, 128 scenarios; host and command loading `not_checked`, model behavior `not_run`.
2. `python3 -B scripts/check_docs.py` — exit 0; 78 Markdown files, no reported local-link/count errors. This checker expressly excludes external URLs, fragments, rendering and prose-truth verification.
3. `python3 -B -m unittest discover -s tests -v` — exit 0; 36 tests passed in 4.007s, including all four new audit regression tests and behavior-fixture/selection/workflow tests.
4. Each of `python3 -B scripts/build.py --adapter portable --output <disposable>/portable`, its `--check`, the matching opencode build, and its `--check` — exit 0. These used `/var/folders/k9/0mqqtyn90j31qcqvltrlmww00000gn/T/review-agents-builds-e0vzd4c_/` and were removed by the temporary-directory context.
5. A separate Python heredoc invoked `scripts/install.py` in another temporary directory: conflicting command license with `--team team-geo` rejected without creating profiles; `--replace` retained the original notice backup; an edited installed notice rejected a new scientist selection without installing scientist; explicit replacement preserved state mode 0600 and earlier geo profiles/command; repeated scientist selection reported zero changed files. All assertions in the corrected probe passed.
6. The first version of that extra probe stopped with an AssertionError because I incorrectly assumed feature-developer was absent from an explicit team-geo install. Raw team metadata includes it. I corrected the probe to use scientist. This was a probe assumption error, not a product defect; its earlier conflict-preflight assertion passed.
7. Recomputed hashes for every recorded changed input after checks — none changed.

## Limits

No real user configuration was installed or inspected, and no account, secret, package installation, commit or publication operation was performed. No source files were edited. Tests may create ignored Python bytecode through their subprocesses; this does not change the tracked source snapshot. No actual selected-host OpenCode executable/registration check, end-to-end model/team execution, Python 3.10 runtime, Windows runtime, browser, production, complete concurrency/race coverage, external URL check or exhaustive security audit was performed. Disposable host-independent install tests cannot establish actual host loading. The new scenario specifications are not observed behavioral outcomes.

## Reviewed changed input hashes

```json
{
  "head": "f374ffbb543595486c8c5145884c123d77e88020",
  "changed_working_tree_sha256": {
    "INSTALL.md": "bc3845168e833d898c4d6220cad642cfdb5edabc93a370444f0bc42b083c6d0f",
    "agents/quality-engineer/instructions.md": "fa60df70cd2b4613c1221d49af2e3ccf2f8c2d9f312c176ae1da1bcf752c3419",
    "agents/team-lead/instructions.md": "55f4b7395679f7e8358e8fdd6743604aed528a31af8dd64ffd80049fed6badb3",
    "docs/ARCHITECTURE.md": "957897b9e94d93233c7ff2bd145ea0a24b0e15eea78e4a09ac3dbde0780aebd7",
    "docs/FRESH-REVIEWS.md": "115d4eb3eca975ec7ad2f7d2e0516408ed92fd15b2e45731ed38e3fd8a1d0795",
    "docs/INSTALLATION-VERIFICATION.md": "14c9a8eed5a543ae2046786ee6394335a3ff40eb7b7fa866d79dff4563cf6fec",
    "docs/PACKS.md": "0f2e18248a713629a8334c367c9fc7f8664463664522778ab39f86c56a1da38e",
    "docs/TEAMS.md": "0b6ca5ef3e87bfd2a432f4b170dcec09e9b2144a574b31a9a64cfc2455c8e5e4",
    "evals/README.md": "1d5c21c7d6118033ee78d3c082119d29efc23da35a7e35941297a1ab519fecc2",
    "evals/behavior-cases.json": "28c36714b75699ba191b5fe40904687730eaacc19d1d16c978e14d4a5a1cdfcd",
    "scripts/behavior_eval.py": "9c78053353ed177bd7da67b816e91ef7e13107737d7a1e37203d13b1309bd07e",
    "scripts/build.py": "8c6a077ed7ce44999871c941b0bd2f1039f79c4ed9b730cfe7a57c216328fe83",
    "scripts/check_docs.py": "9b1992638d0d67e21b4b3d80bec8402faba1180504fd00cea4e06c6117b6584b",
    "scripts/install.py": "1fc062c74d60ece3be91b926082576021cba03fa9d7c723945b58bc43613f627",
    "scripts/validate.py": "7418f7426809cac70be98efd22b9df557703c93152a81c05e43ce99b7c6ba798",
    "shared/operating-contract.md": "25c88a8a48a9f2081348417f0ffed7df4731dc99f34ba84f42104512df397a72",
    "tests/test_audit_regressions.py": "c412d68bff8de2055a8fc004f82bb2977b4b2ef4ca1dbaac0beab8ee3a39dd19",
    "tests/test_workflows.py": "37e54f275cce90d214ed07abed359fcbda581f7f1d0939b5f060167d87dbe6d9"
  }
}
```
