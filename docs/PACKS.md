# Installable packs

Pack declarations in `packs/*.json` select canonical profiles and teams without
forking their instructions. Builds, installation, and optional host validation
default to the full catalog: 28 profiles and 16 teams.

| Pack | Owned profiles | Owned teams | Dependencies | Total with dependencies |
| --- | --- | --- | --- | --- |
| core | 14 | 7 | None | 14 profiles, 7 teams |
| science-data | 3 | 2 | core | 17 profiles, 9 teams |
| product-growth | 8 | 5 | core, science-data | 25 profiles, 14 teams |
| game-3d | 3 | 2 | core, science-data | 20 profiles, 11 teams |

Core includes ux-designer, usability-auditor, accessibility-specialist, and `/team-ux`.
The core UX workflow remains usable without product-growth: optional user-researcher,
data-analyst, and copywriter candidates are omitted when unavailable. Installing
science-data adds analytics support; product-growth adds user research and copy.

Science/data supports quantitative growth evaluation and game balance. Combining
product-growth and game-3d includes the full catalog. Dependency closure is
automatic; repeated pack selections do not duplicate files. See the [catalog](CATALOG.md)
for role ownership and [team workflows](TEAMS.md) for presets.

```sh
# All profiles and commands
python3 scripts/install.py --tool opencode

# Minimal core or selected domains
python3 scripts/install.py --pack core --dry-run
python3 scripts/install.py --pack core
python3 scripts/install.py --pack science-data
python3 scripts/install.py --pack product-growth --pack game-3d

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
the full catalog and all 91 behavior specifications even with `--pack`; reported
profile/team counts and optional host checks concern the selected closure. Host
checks allow unrelated additional profiles/commands and do not execute model workflows.
