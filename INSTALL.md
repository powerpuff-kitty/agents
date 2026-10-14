# Install agent profiles

This source owns reusable roles and team workflows. Its adapters render portable
Markdown or OpenCode profiles; they do not install skills or provide a model runtime.
See [role-to-skill guidance](docs/SKILLS.md) for the independent procedure source.

## Copyable installation prompt

Give this prompt to an agent with local filesystem, Git and Python access:

```text
Install the agents from https://github.com/powerpuff-kitty/agents for
OpenCode on this machine, using the effective global agent and command locations.

Inspect a temporary checkout, its AGENTS.md and INSTALL.md, and record the exact
source revision. Verify Python 3.10+ and the installed OpenCode executable. Review
canonical roles, teams, selected packs and the local installer before running it.
Install all packs unless I named a smaller selection. Use the repository's existing
OpenCode installer with --dry-run first, inspect the exact destinations/conflicts,
then apply the already authorized installation when preflight succeeds.

Preserve unrelated profiles, commands, permissions and customized files. Do not
use --replace automatically, delete old profiles or switch scope to bypass a
conflict. Report conflicts for a concrete decision; an identical installation
should be a no-op. Retain source licensing and installation provenance.

Use the installed OpenCode executable to reload and verify actual profile and
team-command discovery against this source. Report source/host versions, selected
packs, effective locations, installed/unchanged/conflicted files and actual checks.
Keep unavailable host loading and model behavior unverified. This authorizes the
profile installation, not skill installation, model calls, account changes,
publication or deployment.
```

For a project installation, name the project and explicit profile and command
destinations instead of the global scope. The installer supports only its
documented OpenCode destination strategy; portable exports are manually loaded
instructions in other hosts, not automatic named-agent integration.

## Existing installer

From a reviewed checkout:

```sh
python3 scripts/validate.py
python3 scripts/install.py --tool opencode --dry-run
python3 scripts/install.py --tool opencode
```

Add the same `--pack core` or other explicit pack selection to both installer
commands when selecting a subset. For a project, supply explicit `--target` and
`--commands-target` locations to both invocations. Preserve their separate scopes.
The effective default uses `$XDG_CONFIG_HOME/opencode/agents` or
`~/.config/opencode/agents`, with commands in the sibling `commands` directory.
A profile conflict is refused before either destination is written. The optional
`--replace` operation requires an intentional replacement decision and backs up
replaced content; installation never prunes unrelated or previously installed packs.

After authorized installation, use the actual executable path:

```sh
/path/to/opencode reload
python3 scripts/validate.py --opencode /path/to/opencode
```

The optional host validation checks loaded profile text/metadata and team-command
registration in the intended project. It does not run those team workflows or
establish model reliability. Unsupported host versions or unavailable inspection
remain explicit gaps. Review [architecture and installation boundaries](docs/ARCHITECTURE.md)
when upgrading; source renders and local tests are separate from live loading.

Authored source is MIT-licensed under [LICENSE](LICENSE). Retain notices with
substantial copies and preserve third-party terms. Skills require their own
separately authorized installation; OpenCode reads SKILL.md natively, with no
skill renderer in this repository.
