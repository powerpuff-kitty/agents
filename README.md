# Agents

[![CI](https://github.com/powerpuff-kitty/ai-agents/actions/workflows/validate.yml/badge.svg?branch=main&event=push)](https://github.com/powerpuff-kitty/ai-agents/actions/workflows/validate.yml)
[![Profiles: 35](https://img.shields.io/badge/profiles-35-blue)](docs/CATALOG.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

34 specialists and 1 team lead share a portable operating contract. The catalog
contains **35 profiles, 20 team workflows and 7 optional packs**. OpenCode adapters
produce named profiles and commands; portable exports provide plain Markdown.
Install, build, validate and update this repository independently with Git and
Python 3.10+. No Harness CLI, Harness project or Skills checkout is required.

## Install

Use the [copyable installation prompt](INSTALL.md), or clone the repo and preview
a selection with Python 3.10+; no additional Python packages are required:

```sh
git clone https://github.com/powerpuff-kitty/ai-agents.git
cd ai-agents
python3 scripts/install.py --pack core --dry-run
python3 scripts/install.py --pack core
```

Omit selectors for the full catalog. Repeat/combine `--pack`, `--agent` and
`--team` for partial installs. An explicit team brings its coordinator and declared
members; an individual profile adds no commands. See [selection and dependencies](docs/PACKS.md).

The installer preserves unrelated files and local edits, backs up replaced managed
content and never prunes a previously installed selection. [INSTALL.md](INSTALL.md)
owns destination, update, conflict and verification details.

## Use

```text
/team-feature implement the described feature
/team-ui extract a design profile and candidate system from the supplied reference
/team-geo assess observed AI-answer visibility from the supplied evidence
/team-finance review the supplied financial model
```

[Team workflows](docs/TEAMS.md) define stages, conditional assignments and completion
evidence. [Design extraction](docs/DESIGN-EXTRACTION.md) produces scoped taste/system reports
from existing interfaces. Profiles use the host's available model, tools, context and permissions;
they do not supply a runtime, sandbox or automatic scheduler. Team definitions
request delegation within the actual task scope.

Reusable procedures live in [Skills](https://github.com/powerpuff-kitty/ai-skills).
[Role-to-skill guidance](docs/SKILLS.md) explains optional domains and installation;
installing profiles does not install skills or change their permissions.
[Distribution choices](docs/DISTRIBUTION.md) explains Git/native installation and npm.
[Reflection, memory and agent security](docs/RELIABILITY-METHODS.md) adds focused
methods under existing ownership.
[Product methods](docs/PRODUCT-METHODS.md) covers analytics, experiments, competitor
watching, native apps, participant research and market sizing under existing roles.

## Source layout

```text
agents/<id>/             Canonical role metadata and instructions
shared/                  Shared operating contract
teams/                   Ordered workflow declarations
packs/                   Membership and dependency declarations
adapters/                Portable and OpenCode renderers
docs/                    Usage, architecture and domain guidance
scripts/ and tests/      Build, installation and validation tooling
evals/                   Case specifications and retained observations
dist/                    Generated exports, ignored by Git
```

Edit sources and rebuild exports; [architecture](docs/ARCHITECTURE.md) defines ownership.

## Verify and contribute

```sh
python3 scripts/validate.py
python3 scripts/build.py --adapter portable
python3 scripts/build.py --adapter opencode
python3 scripts/build.py --adapter portable --check
python3 scripts/build.py --adapter opencode --check
python3 -m unittest discover -s tests -v
```

Native registration was checked with OpenCode v2.0.27. [Verification evidence](docs/INSTALLATION-VERIFICATION.md)
separates loaded content from model outcomes; [evaluations](evals/README.md) explain
observed runs and cases that remain unexecuted. [Fresh independent reviews](docs/FRESH-REVIEWS.md)
use separate reviewer sessions without inherited author conversation. Other host versions need their own checks.

Browse the [role catalog](docs/CATALOG.md), [teams](docs/TEAMS.md),
[packs](docs/PACKS.md), [finance](docs/FINANCE.md), [crypto](docs/CRYPTO.md),
[forecasting](docs/FORECASTING.md) and [future domain candidates](docs/DOMAIN-OPPORTUNITIES.md).
[Documentation standards](docs/DOCUMENTATION.md) and [contribution guidance](CONTRIBUTING.md)
cover changes. Authored profiles and tooling use the MIT [license](LICENSE).
