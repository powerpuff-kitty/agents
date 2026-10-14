# Design extraction and taste reports

Design-analyst captures an existing interface's design evidence and produces a
scoped reference report, descriptive taste index/profile and candidate system.
Designer reviews the interpretation; UX-designer owns new journeys. The optional
design-extraction skill supplies the detailed procedure and report template.

Install the profile independently from skills:

```sh
python3 scripts/install.py --agent design-analyst --dry-run
python3 scripts/install.py --agent design-analyst
```

The core pack includes the analyst and the existing UI workflow. Profile-only
selection adds no team command. For coordinated extraction and independent review,
install `--team team-ui` and use:

```text
/team-ui extract a design profile and candidate system from the supplied interface,
write the report to the agreed output directory, and independently review the evidence
```

Supply a URL, accessible app/screens, screenshots, design files or UI source, the
intended use and relevant screen/state/theme/viewport scope. Available host tools
determine capture depth. No capture engine, browser, account, remote API or runtime
scheduler is installed by these profiles. Source-only/offline input is supported;
actual runtime checks remain explicit gaps when unavailable.

## Deliverables

| Artifact | Purpose |
| --- | --- |
| REPORT.md and portable report.html where feasible | Scope, findings, illustrations, interpretation, reuse and actual checks |
| taste.json | Reference metadata/tags and evidence-linked descriptive dimensions |
| candidate DESIGN.md | Foundations, token mappings, component/state/layout rules and unknowns |
| tokens.json / tokens.css where supported | Declared-format token subset and web mapping, with provenance |
| evidence/manifest.json | Sources, revisions, capture context, locators and artifact identities |

A taste profile is not a universal quality score. Screenshot sampling does not
establish exact fonts, hidden behavior, breakpoints or accessibility. Source
declarations do not establish runtime use. Missing exports/checks remain visible.
The generated system is a candidate, not automatic project identity or approval.
Use references with their recorded reuse constraints; examples are labeled
reconstructions and reports do not execute imported source scripts.

The [source profile](../agents/design-analyst/instructions.md),
[role/skill mapping](SKILLS.md) and [evaluation records](../evals/README.md) own
responsibility and verification details. Existing Harness schemas remain canonical;
the local taste handoff is not a replacement schema. A separate reference library
or report-viewer product remains a future option, not part of this implementation.
