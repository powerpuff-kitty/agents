# Design extraction verification — 2026-10-14

2 fresh sessions used explicit design-analyst/design-extraction instructions on
synthetic offline source. Separate fresh reviewers checked each output against raw
evidence without the author conversation or desired answers. Actual invocation
provenance, input identity and limits are in the [manifest](manifest.json).

- [Source-only report](source-only/REPORT.md), [HTML companion](source-only/report.html),
  [taste profile](source-only/taste.json) and [candidate system](source-only/DESIGN.md):
  13 evidence records and 27 local-format token candidates; independent review
  found no material static mapping/link/HTML defect. See the [original output review](report-evidence-review.md).
- [DTCG export](dtcg/result.md): 15 candidates per theme, original units and separate
  default/dark files. [Independent subset review](dtcg-evidence-review.md) checked
  values, mappings and shape. The [provenance addendum](dtcg-provenance-addendum.md)
  reconstructs 2 historical instruction identities; it does not certify later edits.
- [Integration review](independent-review.md) found a stale test count; it was fixed
  and the [targeted recheck](targeted-recheck.md) passed. The full current Agents
  suite passes 36 tests; both adapters build and byte-check.
- [Native loading](native-host.json) registered 52 skills, 35 prompts and 20 commands
  in isolated OpenCode 2.0.27. This verifies entrypoint/prompt content and command
  names, not model behavior or actual team scheduling.

The exercise exposed an ambient-project adoption note in a reference-only report.
Current instructions now separate the explicit analysis target from the working
directory. New target-scope cases remain unexecuted. Historical reports/captured
instructions remain identified by their original hashes; an old run does not prove
that a changed instruction works. Public examples are explicitly separate exports:
[source-only export notes](source-only/EXPORT.md), [token export notes](dtcg/EXPORT.md).
Unrelated project instruction contents are withheld, and scoped report redactions
are disclosed. The original complete local runs were not rewritten.

The 2 exercises are separate from canonical behavior cases. No browser, live website,
native-app interaction, accessibility, official DTCG conformance or repeated model
reliability was established. There is no new browser/crawler runtime in these repos.
