# Source-release readiness: conditional go

The reviewed source supports an experimental **v0.1.0-beta.1 source-only release**, with explicit verification limits. No blocking defect was reproduced in the requested export/installation behaviors. This is not a completed release certification: the exact full test gate and actual OpenCode loading remain unverified here.

Candidate: `73b241f5eb9240034d78f531abd8ace804ed0890`, clean tracked source before and after; macOS 26.7 arm64, Python 3.14.7. No local tags were listed. The version is the requested candidate label, not an existing or published tag. Exact model and usage: **unknown**.

| Gate | Actual evidence | Result |
| --- | --- | --- |
| Source validation | `python3 scripts/validate.py`: 35 agents, 20 teams, 7 packs, 144 scenario specifications | Passed; specifications are not model executions |
| Documentation | `python3 scripts/check_docs.py`: 326 Markdown files, zero path/count errors | Passed within checker limits |
| Exports | Both adapters built and passed `--check`; existing tests compare repeat bytes and reject drift | Passed |
| Repository tests | 24 workflow + 5 selection + 4 regression + 3 native-probe unit + 1 docs + 2 safe behavior-harness tests | 39 passed; 3 not run |
| Installation safety | Existing tests plus `installer_probe.py`: dry run, individual/team selection, no pruning, repeated-install byte/mtime stability, unrelated files, edited-file refusal | Passed in disposable targets |
| Managed updates | Actual installer with an in-memory v2 rendered profile: untouched v1 replaced, profile/state backups exact, mode retained; v2 repeat unchanged | Passed; source version change was simulated |
| Source archive consumer | `archive_probe.py`: repeated `git archive HEAD` bytes match; extracted source validates/builds without `.git`, CLI or Skills checkout; exports match checkout | Passed |
| Archive installation | Explicit disposable destinations, core pack: dry run 26 planned files; install 26 changed; repeat 0 changed / 26 unchanged | Passed |
| Actual host / CI / model behavior | No permitted executable supplied, no network, no model calls; native tests use synthetic/mock evidence | Unverified |
| Publication / recovery | No tag, publication or remote artifact check; backup bytes checked, manual restoration not rehearsed | Not performed |

The exact project command `python3 -m unittest discover -s tests -v` was not run. Three behavior-harness tests prepare synthetic Git commits (`scripts/behavior_eval.py:94`), which conflicts with this pilot's no-commit instruction; the other 39 tests ran without changing project source. Python 3.10, Windows/Linux execution and live host discovery were not tested. No comprehensive security audit is claimed.

Before an unconditional release sign-off, run the complete suite in an authorized disposable environment and retain native-host evidence for the intended revision/version, or explicitly publish the beta with those limitations. Add the untouched-managed-update scenario from this pilot to permanent tests. Consider extending `scripts/opencode_probe.py:49`: its native check covers prompt bodies and command names, but does not compare loaded mode/description/command routing; the stricter optional `validate.py --opencode` path was not exercised here. These are coverage improvements, not reproduced installer failures.

`INSTALL.md` pins `18584173054bb7d16c2448e5892da923cd68370e`. Local Git comparison found only the installation-prompt pin changed between that commit and reviewed HEAD; installer/profile source equivalence is therefore source-confirmed. Do not report that older pin as the reviewed HEAD itself.

Local candidate archive SHA-256: `6f4f6f64d550e33f4c0e44ef2e45026d0c76d8eab002460793319e0aa5110cdf`. This identifies this local tar, not a remote release artifact. Logs, exact commands, selection reasons, installed instruction hashes and reproduction files are indexed in [actions.md](actions.md).

This was one fresh scoped review run, supplied with history inheritance disabled. No additional independent reviewer was invoked. Reading the catalog and installed instructions does not establish automatic host triggering or host registration.
