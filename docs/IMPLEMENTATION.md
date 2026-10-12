# Initial agent suite implementation

The repository contains nine portable agent definitions, a shared operating
contract, an OpenCode renderer/installer, a plain Markdown export, and 21 behavioral
acceptance specifications. This is the implemented structure, not a claim that
every model follows the profiles or every tool natively supports named agents.

## Instruction improvements

The existing implementation, progress, quality, security, architecture, and
designer profiles were revised from a local instruction audit. The changes make
project-context discovery, preservation of user edits, review-only scope,
existing authorization, evidence confidence, and completion explicit.

Quality review no longer requires remediation or unrelated benchmarks. Progress
review no longer includes automatic external tracker changes. Architecture scores
are normalized correctly; quality and architecture ratings disclose unverified
coverage and use continuous grade intervals. Security validation uses isolated
fixtures and redacted evidence. Designer maintains representative coverage and
uses existing local visual tools when interactive browser access is unavailable.

Release, performance, and evidence specialists add artifact/consumer verification,
comparable profiling and measurement, and provenance/reproducibility/claim checks.
Narrow procedures remain skills instead of separate overlapping role copies.

## Verification on 12 October 2026

- Source validation passed for all nine roles and 21 scenario specifications.
- Portable and OpenCode output builds were deterministic, and drift checks passed.
- Nine workflow regression tests passed: deterministic builds/drift detection,
  dry-run preservation, unrelated-file preservation and idempotence, conflict
  refusal/backups/local-edit protection, profile symlink protection, neutral
  portable export, output-directory symlink protection, management-state
  validation, and exact routing-description preservation.
- The generated OpenCode profiles were installed with backups and no model or
  permission overrides. OpenCode 2.0.27 loaded all nine complete prompts,
  descriptions, and modes. Loading was checked from the suite repository and
  two existing project directories.
- A YAML folding issue that split a hyphenated role name was found through
  actual host metadata comparison, corrected, and covered by a regression test.
- Two local OpenCode installations were observed: version 1.4.1 on one PATH and
  2.0.27 under the user's OpenCode installation. Host validation therefore requires
  an explicit executable. Version 1.4.1 compatibility was not established.

Commands are documented in [the README](../README.md). Installation backups and
machine-specific validation records remain local, outside version control.

## Remaining evidence limits

The 21 behavioral scenarios have not been executed in actual evaluated model
sessions. File, rendering, installer, and host-loading checks do not establish
instruction adherence, reliability, token savings, or domain accuracy.

Native browser access remained denied in the checked service. The designer's
fallback uses available local browser tests or artifacts and keeps unavailable
interaction checks unverified. This migration did not enable browser integrations
or silently change host permissions.

Only the portable and OpenCode adapters are implemented. Other hosts can manually
consume portable bundles, but automatic named-agent integration requires a new
adapter and host-loading evidence. Existing project instructions and authorized
scope govern each subsequent task.
