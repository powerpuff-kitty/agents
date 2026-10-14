# Independent repository audits — 2026-10-14

2 reviewers started with `fork_turns: "none"` against clean detached source
snapshots. They received the [Skills brief](skills/original-brief.txt) and
[Agents brief](agents/original-brief.txt), project rules and raw source, without
the author conversation or prior findings. The invocation setting comes from the
coordinator's tool calls; it is not an authenticated record of every reviewer read.

The original [Skills report](skills/original-report.md) and [Agents report](agents/original-report.md)
are retained unchanged. All 8 findings were confirmed and fixed; the
[manifest](manifest.json) records dispositions, source revisions and limits.
Original Skills repro inputs/logs and the Agents reproduction script remain
historical evidence; their absolute paths refer to the original local environment.
Regression tests in current source exercise the repaired behavior. A second pair
of fresh-session reviewers found no actionable regression in the hashed changes:
[Skills recheck](skills/change-review.md), [Agents recheck](agents/change-review.md).
Their exact briefs and input hashes are retained alongside each report. Later
report/index/installation-pin edits are outside those recorded input hashes.

The [isolated installation check](installed-host.json) loaded 51 skills,
34 profiles and 20 commands in OpenCode 2.0.27, with license notices retained.
No model was invoked by that check. These 2 audits are observations, not runs of
the new canonical role-case specifications or proof of exhaustive coverage.
