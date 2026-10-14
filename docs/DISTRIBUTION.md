# Distribution channels

Skills and Agents are independent source repositories with separate installation,
updates, validation and releases. Direct Git/native skill folders and the Python
profile installer are their primary paths. Neither requires the Harness CLI or
the other collection. Roles can use optional skills when available and continue
with feasible native methods when they are absent.

The CLI is an optional downstream consumer. It pins and bundles a Skills snapshot
for reproducible builds; that dependency points from the CLI to Skills. It does
not control either collection's releases, and it does not bundle agent profiles.
Updating any repository does not update copies already installed by another
channel. The CLI validates its pinned integration in its own CI; Agents validates
its own source and native profile registration without checking out either repo.

Installing a Node package in node_modules does not itself register skills, profiles
or commands in an agent host.

| Repository | Current choice | Reason |
| --- | --- | --- |
| ai-skills | Keep root folders and Git-based selection | Preserves source independence and the folder-only contract; existing tools can consume Git skills directly |
| ai-agents | Keep the dependency-free Python installer and portable/OpenCode exports | Already supports selection, updates, preservation and actual host verification; an npm wrapper would still need equivalent behavior |
| agentic-harness-cli | Prepare verified native bundles first | A future npm launcher can be a convenience channel once exact-version platform artifacts and ownership are established |

The external [Skills CLI](https://github.com/vercel-labs/skills) already supports
GitHub sources, listing and partial skill selection. That tool's scope, destination,
updates and provenance differ from `ah skills`; do not silently switch managers or
claim third-party installation behavior was tested by our installer checks.

Do not create 1 npm package per skill/role. A future package should be a thin
versioned distribution of canonical outputs, with an explicit file allowlist,
licenses, no automatic host mutation on install and tarball tests in isolated
targets. Do not publish an empty placeholder or claim an unregistered package works.
For a native CLI launcher, verify platform/architecture, exact release identity and
archive integrity before execution; a portable fallback must preserve honest
unsupported-platform errors. Avoid an unreviewed latest download or credential-bearing
postinstall script.

[npm package metadata](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/)
and [trusted publishing](https://docs.npmjs.com/trusted-publishers/) were reviewed
2026-10-14. Publication needs an actual owned package/scope, authentication or a
configured trusted publisher, versioned artifacts and an explicit publish action.
No npm packages or registry credentials were created or inspected in this work.
