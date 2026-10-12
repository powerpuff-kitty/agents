# Team implementation verification

On 12 October 2026 the suite gained a portable team-lead profile and four canonical
team presets: project audit, feature delivery, UI review, and release readiness.
There are now ten profiles, four team briefs/slash commands, and 31 behavioral
acceptance specifications.

## Implemented behavior

Team definitions live in `teams/*.json` and specify coordinator, intent, mode,
parallel assignment limit, ordered stages, contextual applicability conditions,
and completion evidence. The audit preset covers all nine specialists. Other
presets select relevant assignments, with conditional reviews where appropriate.
Feature delivery has one exclusive source writer followed by independent review.

OpenCode renders the coordinator as primary and keeps specialists eligible for
both primary and child use. Four generated commands select team-lead, force the
current session, and pass the requested scope as a prompt argument. The portable
adapter emits neutral briefs alongside complete profile bundles.

Installation checks profile and command destinations for conflicts before either
is changed, protects local edits, preserves unrelated files, and records separate
backup paths when replacements occur. An agents-only option remains available.
Only team-lead and the four commands were added to the local installation; the
existing nine specialist files, selected model, and global permissions were unchanged.

## Checks performed

- Source validation passed for ten profiles, four teams, and 31 case specifications.
- Both adapters built successfully and generated-output drift checks passed.
- Fifteen regression tests passed, including parent coordinator mapping, one
  argument placeholder per command, absence of pre-executed shell blocks,
  command conflict preflight, command edit/backup protection, agents-only install,
  unknown team members, invalid review writers, multiple source writers, and
  host-neutral portable briefs, non-overlapping install destinations, and the
  existing build/installer checks.
- OpenCode 2.0.27 loaded every full profile prompt, description, and intended mode.
- The actual command registry exposed all four team command names/descriptions.
  This registry check did not execute a command or call a model.
- Configuration reload completed successfully. An initial reload encountered a
  stale location from an earlier temporary-clone verification; invalidation removed
  that failed context, and the next reload succeeded without a service restart.

## Limits

No end-to-end model team session was evaluated. The 31 specifications remain
`not_run`; child dispatch, conditional selections, concurrency adherence, writer
serialization, and consolidated outcomes require retained model-run evidence.
The preset's parallel limit and review boundaries are instructions, not an enforced
scheduler or sandbox. Host tools, permissions, budgets, and project instructions
continue to govern execution.

The command registry exposes names/descriptions, not its complete resolved template.
Template/coordinator/parent mapping is checked in generated files against the
published host schema; registration proves discovery rather than full execution.
Use [team usage](TEAMS.md) for invocation and expected workflow behavior.
