# Source and adapter architecture

Each agent has one portable metadata file and one specialist instruction file.
The shared operating contract has one canonical file. A renderer composes those
inputs with host-specific guidance and emits a complete profile. Generated files
are disposable outputs rather than independent sources.

## Portable source contract

`agents/<id>/agent.json` contains `schema_version`, stable `id`, display `title`,
and routing `description`. Version 1 requires a lowercase ID matching its folder.
Descriptions identify the role and nearby exclusions without tool-launch examples.
`instructions.md` owns that role's procedure, evidence requirements, boundaries,
and completion conditions. Shared rules belong in the operating contract.

Canonical sources can refer to project conventions such as AGENTS.md when the
host supports them, but must not require a vendor tool name, API, model, permission
schema, or directory for routine work. The actual project's accepted goals and
instructions remain authoritative over generic role preferences.

## Adapter contract

An adapter directory contains:

- `adapter.json`: version and output target, plus target-specific settings.
- `instructions.md`: additive host guidance without redefining portable role rules.
- `render.py`: a `render(agents, contract, host_instructions, config)` function
  returning relative output paths and their UTF-8 text.

The shared compiler validates canonical metadata, invokes the selected renderer,
and creates a manifest with input and output hashes. Builds have no timestamps or
machine-specific paths. `--check` detects missing, stale, or altered outputs.
Unexpected output files are not silently deleted.

OpenCode maps the neutral description to folded YAML and selects `mode: all` in
its adapter. The generated body includes the specialist instructions, common
contract, and OpenCode host guidance. Its profiles inherit model and permissions.
The portable adapter emits complete plain Markdown without host metadata.

The installer currently knows only the OpenCode destination convention. Adding
a renderer alone does not establish installation support or host compatibility.
For a new tool, add a destination strategy and tests when automatic installation
is appropriate; otherwise document manual loading explicitly.

## Installation boundaries

Installation compiles from current sources, checks all known filename conflicts,
backs up changed existing profiles, and writes individual files atomically.
The local management state records installed hashes so subsequent changes to a
managed profile are recognized as user edits. `--replace` is an explicit request
to back up and overwrite conflicts. Unrelated profiles are preserved and stale
managed profiles are not pruned automatically.

The installation is not a directory-wide transaction: a filesystem failure or
concurrent modification can interrupt it. Backups preserve replaced originals,
and rerunning reconciles successfully installed files. Do not use `--replace`
blindly when local edits should be incorporated into canonical sources instead.

## Verification boundaries

Tests verify deterministic rendering, drift detection, installation preservation,
conflict protection, backups, and idempotence. Optional host validation checks
actual loaded prompts, descriptions, and modes with an explicit executable.
It retries missing IDs briefly during service initialization, while prompt or
metadata mismatches fail immediately.

Behavioral evaluation requires actual retained sessions and outcome evidence.
The scenario files are acceptance specifications and cannot establish compliance
by themselves. The definitions are not a read-only enforcement mechanism; host
permissions and the user's authorized task still govern executable actions.
