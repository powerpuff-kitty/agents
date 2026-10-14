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

## Financial procedures

The optional [finance pack](FINANCE.md) adds:

| Skill | Primary role use |
| --- | --- |
| market-data-validation | All finance roles; data-analyst checks input provenance/availability. |
| financial-model-review | financial-analyst checks statements/forecasts/valuation; portfolio-risk-analyst checks exposure/stress models. |
| backtest-validation | quant-researcher checks causal timelines, fills/costs, ledgers and selection evidence. |

Each skill includes a focused reference, worked synthetic examples, a report
template and six unrun acceptance cases. Profiles still work with bounded direct
methods if a skill is unavailable. No account or model call is needed to install
these sources; actual native loading remains a separate check.

## Crypto and forecast procedures

| Skill | Primary role use |
| --- | --- |
| onchain-data-analysis | onchain-analyst checks chain identity, finality, units and metric evidence. |
| smart-contract-review | Existing security-auditor checks scoped EVM/Solidity source/control paths and deployment match. |
| defi-risk-analysis | onchain-analyst and portfolio-risk-analyst assess mechanism-specific protocol/position scenarios. |
| odds-analysis | probability-analyst checks formats, complete-market margin and conditional fees/payoffs. |
| forecast-calibration | probability-analyst evaluates recorded probabilities, proper scores, calibration and uncertainty. |
| settlement-rule-review | probability-analyst checks contract definitions, sources, deadlines and resolution/finality status. |

[Crypto](CRYPTO.md) and [forecasting](FORECASTING.md) own role/team examples.
Each skill has a focused guide, report template and six unrun acceptance cases.
Profiles do not install skills or provision wallet/account access.

## OpenCode

OpenCode natively discovers Agent Skills; no skill renderer is required. Its
[skill documentation](https://opencode.ai/v2/docs/skills/) lists project-local
`.agents/skills/<name>/SKILL.md` and `.opencode/skills/<name>/SKILL.md`, and global
`~/.agents/skills/<name>/SKILL.md` and `~/.config/opencode/skills/<name>/SKILL.md`.
The source repo's root folders must be installed into a supported discovery path.
Use real folders with their local resources, preserve existing custom copies and
avoid duplicate names across discovery locations. The portable collection contract requires
`name` plus `description`; V2 uses the directory-derived ID and treats `name` as a display label; preserve normal automatic selection unless the user
explicitly requests otherwise. Review date: 2026-10-14.

The existing `adapters/opencode/` renders role profiles and team commands. It does
not transform skill files or widen skill permissions. Check the installed host's
actual skill inventory and load the chosen skill before claiming delivery. The [retained verification](INSTALLATION-VERIFICATION.md) checks current registered
content. It does not establish model adherence. Other hosts use their own verified
skill discovery workflow, with the same portable skill contents where supported.

## Local verification boundary

On 2026-10-14, an initial fresh-server `skill.list` API query was empty. A
persistent-server check then registered all 51 skills, 34 agent prompts and 20
team command names with expected skill paths/bodies and agent prompt bodies.
Configuration plugins initialize asynchronously; bounded polling must reuse the
same server. No global host configuration changed and no model call ran. See
[actual evidence and reproduction](INSTALLATION-VERIFICATION.md). Native folders
need no skill adapter; other hosts/versions need their own checks.

## Content/GEO and managed selection

Existing copywriter/marketing/GEO roles can use content-brief, copy-editing,
content-repurposing and geo-measurement. [Domain recommendations](SKILL-RECOMMENDATIONS.md)
map optional procedures to agent packs. The CLI's `skills` lifecycle offers
individual/domain selection, revision/hash inventory, safe managed updates and
rollback; it remains separate from installing agent profiles.
