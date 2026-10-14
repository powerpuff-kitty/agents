# Installable packs

Pack declarations in `packs/*.json` select canonical profiles and teams without
forking their instructions. Builds, installation, and optional host validation
default to the full catalog: 34 profiles and 20 teams.

| Pack | Owned profiles | Owned teams | Dependencies | Total with dependencies |
| --- | --- | --- | --- | --- |
| core | 15 | 8 | None | 15 profiles, 8 teams |
| science-data | 3 | 2 | core | 18 profiles, 10 teams |
| product-growth | 8 | 5 | core, science-data | 26 profiles, 15 teams |
| game-3d | 3 | 2 | core, science-data | 21 profiles, 12 teams |
| finance | 3 | 1 | science-data (and its core dependency) | 21 profiles, 11 teams |
| crypto | 1 | 1 | finance (and its dependencies) | 22 profiles, 12 teams |
| forecasting | 1 | 1 | science-data (and core) | 19 profiles, 11 teams |

Core includes ux-designer, usability-auditor, accessibility-specialist, and `/team-ux`.
The core UX workflow remains usable without product-growth: optional user-researcher,
data-analyst, and copywriter candidates are omitted when unavailable. Installing
science-data adds analytics support; product-growth adds user research and copy.

The [finance pack](FINANCE.md) provides financial reporting/model analysis,
quantitative strategy research and portfolio-risk review. It does not connect
financial accounts or install the independent validation skills.

Core also owns iteration-reviewer and `/team-iteration`; feature/general workflows
use it to assess integrated product increments against accepted gates. See
[iteration readiness](ITERATION-READINESS.md) for evidence and trigger boundaries.

Science/data supports quantitative growth evaluation and game balance. Combining
product-growth, game-3d, crypto and forecasting includes the full catalog. Dependency closure is
automatic; repeated pack selections do not duplicate files. See the [catalog](CATALOG.md)
for role ownership and [team workflows](TEAMS.md) for presets.

```sh
# All profiles and commands
python3 scripts/install.py --tool opencode

# Minimal core or selected domains
python3 scripts/install.py --pack core --dry-run
python3 scripts/install.py --pack core
python3 scripts/install.py --pack science-data
python3 scripts/install.py --pack product-growth --pack game-3d --pack crypto --pack forecasting

# Matching portable/OpenCode exports and validation
python3 scripts/build.py --adapter portable --pack core
python3 scripts/build.py --adapter opencode --pack core
python3 scripts/build.py --adapter portable --pack core --check
python3 scripts/build.py --adapter opencode --pack core --check
python3 scripts/validate.py --pack core --opencode ~/.opencode/bin/opencode
```

The default full export remains `dist/<adapter>/`. A selected build uses
`dist/<adapter>-<requested-pack-ids>/`, with sorted unique requested IDs; its manifest
records the resolved dependency closure. Use `--output` for an explicit destination.
Adaptive team briefs omit unavailable candidates and empty stages from that export.
The coordinator's routing reference still describes the catalog and instructs it
to discover actual installed roles rather than assuming every listed role exists.

Selecting a smaller pack later updates its managed outputs but preserves previously
installed profiles and commands. It is not an uninstall operation; a previously
installed specialist may still be discovered by the host. Unrelated files, local
edits, backups, conflict preflight, and idempotence retain the normal installer rules.
Use separate project-local targets for a clean subset when needed:

```sh
python3 scripts/install.py --pack core --target /path/to/project/.opencode/agents
```

The sibling `.opencode/commands` is selected automatically. Source validation checks
the full catalog and all 124 behavior specifications even with `--pack`; reported
profile/team counts and optional host checks concern the selected closure. Host
checks allow unrelated additional profiles/commands and do not execute model workflows.

[Crypto](CRYPTO.md) adds onchain evidence and a conditional contract/economic
review team. [Forecasting](FORECASTING.md) adds odds, proper-score/calibration
and settlement analysis. Neither pack adds account or transaction capabilities.
Combining crypto and forecasting resolves 23 profiles and 13 workflows; shared
dependencies are deduplicated. Source profiles still require actual host loading
checks after a requested installation.

## Fine selection

Build, install and validation also accept repeatable `--agent ID` and `--team ID`.
With any granular selection and no `--pack`, no whole pack is selected. A team
adds its coordinator and every declared member, including adaptive candidates;
this makes the selected command self-contained. An individual profile adds only
itself. Combine selectors with packs to extend their closure, with no duplicates.
Unknown IDs fail before installation writes. Granular exports use a deterministic
`<adapter>-selection-<hash>` default directory; use `--output` for a chosen path.
All-source validation/evaluation specification checks still run before selecting.

```sh
python3 scripts/install.py --agent financial-analyst --dry-run
python3 scripts/install.py --team team-geo --agent financial-analyst --dry-run
python3 scripts/build.py --adapter opencode --team team-geo
python3 scripts/build.py --adapter opencode --team team-geo --check
```

Build the matching selection before its `--check`. Fewer selections preserve prior
installed outputs. Pack-to-skill recommendations are documented in
[SKILLS.md](SKILLS.md); no skill installation is implicit.
