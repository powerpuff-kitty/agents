# Reusable agents

Twenty-seven specialist profiles and a team lead share one operating contract. Portable role
instructions are the source of truth; adapters produce tool-specific versions.
The repository currently supports plain Markdown bundles and OpenCode profiles.

The [agent catalog](docs/CATALOG.md) lists all 28 roles. Sixteen [team workflows](docs/TEAMS.md)
cover general tasks, engineering, research, science/data, product/growth, and game/3D
work. Four [installable packs](docs/PACKS.md) share the same canonical sources.

These are instruction profiles. They use the host's selected model, available
tools, project context, and permissions. They do not independently provide tools,
enforce a sandbox, or establish expertise through a profile name alone.

## Layout

```text
agents/<id>/agent.json          Portable identity and routing description
agents/<id>/instructions.md     Specialist instructions
shared/operating-contract.md    Shared scope, evidence, and completion rules
teams/<preset>.json             Portable assignments, stages, and completion
packs/<id>.json                 Membership and dependency declarations
adapters/portable/              Plain Markdown export
adapters/opencode/              OpenCode renderer and host-specific guidance
dist/<adapter>/agents/          Generated profiles, ignored by Git
dist/opencode/commands/         Generated team slash commands
dist/portable/teams/            Neutral team briefs
scripts/                       Build, install, and validation commands
tests/                         Build and installation regression tests
evals/                         Behavioral acceptance specifications
```

## Build and install

Python 3.10+ is required; no additional packages are needed.

```sh
git clone https://github.com/powerpuff-kitty/agents.git
cd agents
python3 scripts/build.py --adapter portable
python3 scripts/build.py --adapter opencode
python3 scripts/install.py --tool opencode --dry-run
python3 scripts/install.py --tool opencode
```

OpenCode profiles install under `$XDG_CONFIG_HOME/opencode/agents`, or
`~/.config/opencode/agents` when that variable is unset. Team commands install in
the sibling `commands/` directory. Use `--target` for a
project-local `.opencode/agents` directory or another explicit destination.
Use `--commands-target` for a separate command destination, or `--agents-only`
to install profiles without commands. Both destinations are checked for conflicts
before either is written. Unrelated profiles and commands are preserved.
Locally edited or unmanaged conflicting outputs are refused unless `--replace`
is supplied; replacements are backed up
under the target's parent `backups/` directory. Reinstallation without changes
does not rewrite the profiles. Obsolete files are not silently deleted.

Without `--pack`, builds and installation include all 28 profiles and 16 commands.
For a smaller installation, select packs; dependencies are included automatically:

```sh
python3 scripts/install.py --pack core --dry-run
python3 scripts/install.py --pack core
python3 scripts/install.py --pack science-data
python3 scripts/install.py --pack product-growth --pack game-3d
```

Selecting fewer packs later preserves previously installed outputs; it does not
uninstall them. Pack-specific builds use separate default output directories.
See [pack selection](docs/PACKS.md) for dependency counts and matching validation.

After installing, use the intended OpenCode binary to reload and verify:

```sh
~/.opencode/bin/opencode reload
python3 scripts/validate.py --opencode ~/.opencode/bin/opencode
```

Use your actual executable path if different. OpenCode 2.0.27 loading was verified
for this adapter. The minimal frontmatter intentionally avoids model/permission
overrides. The team lead uses `mode: primary`; specialists retain `mode: all`.
Other OpenCode versions require their own loading checks; do not infer
compatibility from the file extension. Existing projects can override global
profiles, so inspect the host result in the intended project directory.

Select a profile or ask OpenCode to use it for a concrete task, for example:
`Use designer to audit this project's design system and UI.`

## Use a team

Type these custom slash commands in OpenCode with the requested scope:

```text
/team research alternatives for our current storage layer
/team fix the settings keyboard navigation and verify it
/team-research compare these libraries against our project constraints
/team-audit review this project's readiness
/team-feature add the described feature
/team-ui review the dashboard and settings flow
/team-ux review navigation, task continuity, and recovery
/team-ux fix the scoped onboarding flow and verify it
/team-release assess version 1.2.0 readiness
/team-data analyze the supplied cohort dataset
/team-science design an experiment protocol without running it
/team-launch plan the launch from our approved product facts
/team-seo audit this site
/team-geo assess the supplied AI-answer visibility samples
/team-game design the progression economy
/team-3d specify this asset for our runtime
```

Commands select team-lead in the current session. `/team` selects the smallest
useful set of available specialists based on the actual task, including relevant
project-specific roles. `/team-research` gathers sources, then independently checks
claims and relevant domain implications. The audit preset includes nine core
specialists plus research when needed; other presets use conditional assignments.
The UX team adds focused journey design, independent task walkthroughs, and deep
accessibility checks, with optional research/data/copy roles when installed.
They specify ordered stages, a requested maximum of three independent active
assignments, serialized source writers, and consolidated evidence.

These are instruction-based workflows using the host's delegation tools, not a
separate deterministic scheduler. Review commands do not implicitly authorize
source fixes, tracker changes, publication, or deployment. Feature delivery
authorizes the described implementation. The general team derives action scope
from the request and existing authorization; selecting it alone permits no source
or external mutations. See [team behavior](docs/TEAMS.md).

## Use outside OpenCode

Build `portable` and provide the relevant complete bundle from
`dist/portable/agents/` to a host as instructions. This is manual instruction use,
not a claim of automatic named-agent integration in every tool. The bundles
contain specialist guidance and the shared contract without OpenCode metadata.
Portable team briefs are in `dist/portable/teams/`; supply the coordinator and
applicable complete role bundles to the host. A brief does not create an agent
runtime by itself.

For a maintained integration with another host, add `adapters/<tool>/`, its
renderer, capability/metadata mappings, documentation, and loading tests. Reuse
the same canonical roles; do not fork their full instructions. Hosts differ in
named-agent support, skill discovery, model selection, permissions, and delegation.
Only adapters and explicitly reviewed role changes should account for differences.
See [architecture](docs/ARCHITECTURE.md).

## Validate and evaluate

```sh
python3 scripts/validate.py
python3 scripts/build.py --adapter portable --check
python3 scripts/build.py --adapter opencode --check
python3 -m unittest discover -s tests -v
```

Source validation, deterministic rendering, installer tests, and actual host
profile/command loading are distinct from model behavior. The 91 scenarios in
[evals](evals/README.md) remain `not_run` until an actual evaluated session is
retained. Do not report passing instruction-file checks as agent reliability.

The [implementation record](docs/IMPLEMENTATION.md) documents the initial source
migration and verification. It is an evidence record, not another instruction
source; [team verification](docs/TEAM-IMPLEMENTATION.md) records the later addition.
Deployment credentials, private project data, local backups, and model
transcripts do not belong in this repository.
