# Repository-playbook review — 2026-10-14

This review applies the library profile from
[repository-playbook](https://github.com/powerpuff-kitty/repository-playbook), local
auditor version 0.4.0. The offline scan reads source and selected Markdown/config
subsets; it neither executes target code nor proves remote settings, host loading,
model outcomes or complete repository quality. Its five finding states are retained.

## Accepted improvements

- Keep authoritative role inputs in `agents/`, with shared contracts, teams, packs
  and adapters separately owned. Generated `dist/` stays disposable and ignored.
- Add editor conventions, a focused PR template, contribution/triage guidance and
  a least-privilege pinned-checkout CI workflow using existing standard-library checks.
- Apply the owner-selected MIT license to authored profiles and tooling.
- Keep reusable task procedures in the separate root-folder skills source. Existing
  roles select available methods without a new role or hidden installation.
- Provide [INSTALL.md](../INSTALL.md) with a reviewed installation prompt and
  actual-host verification boundary; [SKILLS.md](SKILLS.md) owns integration detail.

The initial scan reported four static failures: editor settings, PR template, CI
configuration and a root license declaration. The updated scan reports no static
failures. File presence is narrow evidence, not proof of branch protection, passing
remote CI, meaningful tests or actual license suitability beyond the owner's choice.
Remote settings and manual/behavioral checks remain unknown or review-required.

## Actual verification and limits

At the initial review, source validation covered 29 profiles, 17 teams, four packs and 100 `not_run`
acceptance specifications. Both portable/OpenCode builds and freshness checks pass;
24 tooling tests pass using synthetic local destinations. These results are separate
from model behavior and personal-host installation. Five new scenarios cover optional
skill selection, review-only scope, CI access blockers and guarded branch cleanup.

An isolated OpenCode v2.0.27 native skill inventory probe returned no skill entries
for the tested discovery paths. No global configuration or installed profiles were
changed. The cause is not established, so live skill loading is not certified and
no speculative compatibility adapter is installed. See [the observed boundary](SKILLS.md#local-verification-boundary).

Run the playbook auditor from its own checkout with the actual local target path:
`node src/cli.mjs PATH --profile library --format json`. Store reports outside the
audited target. The exact profile/build/test commands are in [AGENTS.md](../AGENTS.md).
Do not convert unknown/manual-review findings into passes or use count changes as
a quality score.

## Finance follow-up

The owner subsequently authorized a finance pack with three new roles and one
team, increasing the source catalog to 32 profiles, 18 teams and five packs with
112 unrun acceptance specifications. [FINANCE.md](FINANCE.md) owns current scope,
worked examples and installation guidance. This addition does not change the
reviewed repository structure or establish host/model financial reliability.
