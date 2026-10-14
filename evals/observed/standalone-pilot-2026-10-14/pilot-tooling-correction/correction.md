# Pilot runner correction

Independent review found that the pilot-only run_gates.py retained command exit codes but did not propagate failures to its own process status. Original command logs all record exit 0; their observed results remain unchanged. The original script and reports are preserved. This corrected separate copy exits nonzero for a failed command, changed tracked source or a dirty final source tree.

Root reran its normal 11-command configuration successfully. Controlled disposable variants replaced only the command-list configuration with /usr/bin/true or /usr/bin/false, retaining the corrected aggregation. Both recorded command and process exits matched 0 and 1 respectively. checks.json and raw logs retain the source/probe identities and observations. This is a root-performed correction to pilot tooling, not a claim that the original run failed or a new independently observed canonical case.
