# Initial-work protection follow-up

The independent recheck found a remaining pilot-runner gap: an initially untracked owner draft could be deleted by a successful subcommand, leaving clean final Git status. The initial correction and its reports remain unchanged.

run_gates.v2.py adds a clean-source preflight before executing commands. It records the initial identity and refuses a dirty source tree, preserving that draft rather than allowing commands to run. Existing failed-command, tracked-source and final-status checks remain. Root controlled probes returned 0 for a passing command, 1 for a failing command, and 1 before executing a draft-deletion command against initially untracked work; the owner draft remained exact. checks-v2.json and per-probe raw logs retain the identities/results. This is scoped protection for the clean-source gate runner, not an authenticated sandbox or permission boundary. The first corrected script remains as the historical v1 artifact.
