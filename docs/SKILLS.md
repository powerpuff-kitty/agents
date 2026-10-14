# Roles and reusable skills

An agent profile owns a responsibility and its handoff/completion expectations.
A skill supplies a focused task procedure. Profiles remain usable without a
particular skill collection, Harness layout, model or hosted provider. Installing
these profiles does not install, grant access to or prove loading of any skill.

The independent [skills repository](https://github.com/powerpuff-kitty/skills)
contains one self-contained folder per skill directly at its root, plus a single
[README.md](https://github.com/powerpuff-kitty/skills#readme) overview and
[INSTALL.md](https://github.com/powerpuff-kitty/skills/blob/main/INSTALL.md) entrypoint. Each skill includes
`SKILL.md`, its license and required local resources. Select only a relevant skill
actually exposed in the current host. Do not fetch or install missing skills
without installation scope; use feasible native methods and state the gap.

| Procedure | Starting role | Responsibility boundary |
| --- | --- | --- |
| [systematic-debugging](https://github.com/powerpuff-kitty/skills/tree/main/systematic-debugging) | feature-developer | Reproduce and fix the owning defect when authorized; quality-engineer can independently verify it. |
| [test-engineering](https://github.com/powerpuff-kitty/skills/tree/main/test-engineering) | quality-engineer; feature-developer for implementation tests | Select meaningful behavior checks, preserve failure evidence and verify the requested change. |
| [change-review](https://github.com/powerpuff-kitty/skills/tree/main/change-review) | quality-engineer | Review the specified diff and accepted behavior; source edits and merge actions need task scope. |
| [ci-triage](https://github.com/powerpuff-kitty/skills/tree/main/ci-triage) | release-engineer | Diagnose exact pipeline/source evidence; route application fixes to the serialized developer. |
| [repository-maintenance](https://github.com/powerpuff-kitty/skills/tree/main/repository-maintenance) | project-auditor | Reconcile acceptance and collaboration state; external changes require existing explicit authorization. |

These procedures do not justify five duplicate specialist profiles. Team-lead
selects the smallest capable existing role set and preserves independent review
when it is requested and feasible. Reviewers do not certify their own authored
change by adopting another role name. A focused defect or CI failure does not
require a full team or every specialty audit.

## OpenCode

OpenCode natively discovers Agent Skills; no skill renderer is required. Its
[skill documentation](https://opencode.ai/docs/skills/) lists project-local
`.agents/skills/<name>/SKILL.md` and `.opencode/skills/<name>/SKILL.md`, and global
`~/.agents/skills/<name>/SKILL.md` and `~/.config/opencode/skills/<name>/SKILL.md`.
The source repo's root folders must be installed into a supported discovery path.
Use real folders with their local resources, preserve existing custom copies and
avoid duplicate names across discovery locations. The required frontmatter is
`name` plus `description`; preserve normal automatic selection unless the user
explicitly requests otherwise. Review date: 2026-10-14.

The existing `adapters/opencode/` renders role profiles and team commands. It does
not transform skill files or widen skill permissions. Check the installed host's
actual skill inventory and load the chosen skill before claiming delivery. The
current source changes were validated as profiles/specifications; they are not
new live-host or model-adherence results. Other hosts use their own verified
skill discovery workflow, with the same portable skill contents where supported.

## Local verification boundary

On 2026-10-14, an isolated OpenCode v2.0.27 `skill.list` API probe returned an empty
inventory for a valid root-source skill copied into documented project discovery
paths. No global host configuration was changed and no model call ran. The skill
source and generated role exports pass their structural checks; native skill
loading remains unverified in this local environment. The empty response alone
does not establish a required adapter or a particular loader/configuration defect.
