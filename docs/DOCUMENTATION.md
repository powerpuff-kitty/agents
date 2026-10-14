# Documentation standards

Keep current usage in the README/INSTALL entrypoints, architecture in ARCHITECTURE,
roles in the catalog, workflows in TEAMS and membership/dependencies in PACKS.
Canonical role instructions and skill entrypoints own their procedures; guides
explain examples and boundaries without repeating the entire procedure.

Use numerals for quantities. Update catalog counts from validated source, and link
CI badges to a named workflow/branch/event. A file-presence check is not behavioral
evidence. Label planned, source-validated, host-loaded and model-observed outcomes.

## Depth by task

| Artifact | Required documentation | Add depth when useful |
| --- | --- | --- |
| Skill | Precise trigger, inputs, procedure and completion | Focused references, worked example, output template or tested helper for ambiguity/repeated mechanics |
| Agent | Responsibility, boundaries, method/handoff and completion | Domain examples when evidence or scope is easy to misinterpret |
| Team | Ordered stages, members, conditions, ownership and completion evidence | A worked handoff when coordination is nontrivial |
| Tooling | Supported invocation, inputs/outputs, failure and preservation behavior | Reproducible checks for mutation, compatibility and recovery |

Do not add a handbook or duplicate role merely to fill a template. Preserve local
resources required by independently installed skills. Read referenced resources
only when relevant; source independence can justify local copies across skills.

## Evidence

Store scenario specifications separately from observed runs. Retain input/source
identities, actual output/checks, host/model identity when exposed, reviewer verdict
and limitations. Preserve failed/unverified outcomes and original raw artifacts.
Never rewrite an observed transcript to match current wording or counts.

[Evaluations](../evals/README.md) and [installation verification](INSTALLATION-VERIFICATION.md)
own retained evidence. Refresh affected checks after changing source; historical
records apply to their recorded bytes. Git history retains obsolete implementation
diaries; current docs do not accumulate milestone appendices.
