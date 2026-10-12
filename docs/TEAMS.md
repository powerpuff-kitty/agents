# Team workflows

A team preset supplies ordered assignments to team-lead. OpenCode commands load
the preset as a user prompt and select that coordinator in the current session.
The coordinator delegates to specialists using the host's available capabilities.
These are reusable workflow instructions, not a new runtime or a multi-select UI.

| Command | Default intent | Workflow |
| --- | --- | --- |
| `/team-audit <scope>` | Review only | Project-auditor scopes accepted work, then all eight other specialists review bounded domains; team-lead consolidates all nine results |
| `/team-feature <feature>` | Implement the described feature | Applicable architecture/design framing, one feature-developer source writer, then independent quality and relevant conditional reviews |
| `/team-ui <screens or journey>` | Review only | Designer establishes representative coverage, followed by quality/evidence checks and performance review when relevant |
| `/team-release <target>` | Readiness review | Release-engineer establishes gates, specialists assess applicable evidence, and release-engineer reconciles the readiness matrix |

The audit preset is the explicit all-specialists entry point. Every assignment
must produce an actual result or an explicit failed/blocked state. Other presets
explain conditional inclusions and skips instead of invoking every role for every
small task. If scope is empty, a clear current task can supply it; otherwise the
coordinator asks only for the missing critical input.

## Coordination rules

The coordinator provides isolated children with scope, accepted requirements,
relevant paths, source identity, permitted actions, and evidence expectations.
It owns a stage/member status record and the final result. Specialists do not
recursively launch other coordinators or additional unassigned workers.

Independent reviews of a stable snapshot may run concurrently, with a requested
maximum of three active assignments and any lower host/user limit respected.
Writers complete before dependent reviews. Corrections return to the implementation
owner, then affected checks run against the changed snapshot. Review assignments
do not mutate source or shared trackers merely because a fix was identified.

Findings are deduplicated by root cause, disagreements are reconciled against
source/reproduction, and stale findings are rechecked or labeled stale. Failed
children and unverified checks remain explicit. An average of incompatible
specialist ratings is not a team readiness score.

Review presets do not authorize tags, pushes, publication, deployment, rollback,
intrusive tests, or new large benchmark programs. Existing explicit authorization
persists, and an explicit remediation request can add a serialized fix/verify
stage without redundant permission questions.

## Installation and host mapping

```sh
python3 scripts/install.py --tool opencode
~/.opencode/bin/opencode reload
python3 scripts/validate.py --opencode ~/.opencode/bin/opencode
```

The installer writes ten profiles and four commands by default. Team-lead is a
primary profile, while specialists retain both primary and child eligibility.
Command frontmatter selects team-lead and uses `subagent: false`, keeping the
coordinator in the parent session so specialists can be its children. No selected
model or global permission setting is changed.

For another destination, use `--target <agents-directory>` and optionally
`--commands-target <commands-directory>`. Omitting the latter uses the sibling
`commands/` directory. `--agents-only` installs profiles without commands.
Profile and command directories must not overlap; nesting commands inside an
agent directory could make the host discover command templates as agent profiles.
Conflict protection, backups, and idempotence apply to both destinations.

Portable exports include complete coordinator/specialist bundles in
`dist/portable/agents/` and neutral briefs in `dist/portable/teams/`. Supply the
applicable bundles to another host; the brief does not provision a team by itself.
If named delegation is unavailable, the coordinator can apply feasible role checks
serially and must label them coordinator-performed rather than independent runs.

## Evidence limits

The command registry verifies that the host discovers the slash commands; source
and rendering tests verify their coordinator, scope placeholder, and parent-session
mapping. No actual end-to-end model team run is established by these checks.
The 31 behavioral scenarios remain unrun until evaluated sessions and artifacts
are retained. Parallel limits and review-only rules are prompt contracts rather
than runtime-enforced semaphores or read-only permissions.
