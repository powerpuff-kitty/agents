# Independent releases

Git tags are the version authority for this source collection. AI Agents has its own
release cadence and starts at `v0.1.0-beta.1`; AI Skills and the Harness CLI may use
different versions. No npm manifest, shared version service or coordinated release
is required. The version applies to profiles, shared instructions, teams, adapters
and installer source at the tagged commit.

A prerelease makes a checked snapshot available with explicit limits. Deterministic
tests and native registration do not establish model reliability or execution of
all behavioral specifications. Release notes distinguish observed results from
unexecuted cases and identify installation/adapter compatibility changes.

Before 1.0, use a new minor version for incompatible source, selection, adapter or
installation changes, and a patch version for compatible corrections. Use a
`-beta.N` suffix while the supported surface remains a prerelease. Keep existing
tags immutable; withdraw or supersede a faulty release with notes and a new version.

## Prepare and publish

1. Select a clean, reviewed commit and the version. Run all [repository gates](../AGENTS.md).
2. Require successful source and native-host CI for that exact commit. The jobs
   use this repository alone; they do not require AI Skills or CLI checkouts.
3. Verify partial/repeated installation, updates and local-edit protection in
   disposable targets. Keep unavailable platforms and behavioral checks explicit.
4. Build a source archive from the exact commit with `git archive`, retaining
   licenses, installer, adapters and required local resources. Record repository,
   version, commit and archive SHA-256 in release metadata; retain a checksum file.
5. Inspect the archive's member paths, contents and file hashes against the target
   commit, and run source/build/install checks from the extracted archive.
6. Create a new tag at the checked commit and publish a GitHub prerelease with
   the source archive, checksum, metadata and accurate notes. Verify the remote
   tag target, downloaded asset hashes and notes. Do not bypass repository protections.

For example, archive a reviewed commit without including working-tree files:

```sh
git archive --format=tar.gz --prefix=ai-agents-0.1.0-beta.1/ FULL_COMMIT_SHA > ai-agents-0.1.0-beta.1.tar.gz
```

Generate release files outside this checkout, or leave them untracked and never
commit them into the source catalog. The source archive is sufficient: users run
its Python installer or build portable/OpenCode exports locally. An npm package
or preinstalled CLI is unnecessary. SHA-256 checksums detect changed bytes; they
are not authenticated publisher signatures.

## Update and rollback

Users can pin a tag and record its resolved full commit as described in
[INSTALL.md](../INSTALL.md#versioned-installs). Updating the source alone does not
change installed profiles. Review release notes, preview the original selection
and destinations, then apply; preserve local changes and unrelated files.

To revert an installation, select a previous reviewed commit and rerun the same
selection after inspecting its dry run. Normal local-edit conflict protection
still applies. A smaller selection does not delete profiles introduced later.
Preserve installation backups and review any explicit replacement deliberately.
