# Installation and task verification

Observed 2026-10-14 with OpenCode v2.0.27. A disposable Git project and private
persistent server registered **51 native skills, 34 agent prompts and 20 team
commands**. Skill paths and Markdown bodies and complete agent prompt bodies
matched their source exports. Team command names were present. No model call,
account change or existing host configuration write occurred.

The first skill inventory can be empty while configuration plugins initialize;
bounded repeat queries on the same server resolve that startup race. Repeatedly
starting a fresh standalone server can repeat the empty snapshot. Native folders
need no skill adapter. Use current [V2 skill documentation](https://opencode.ai/v2/docs/skills/),
which is separate from V1 configuration documentation.

Reproduce from a CLI checkout with its pinned Skills source and an Agents checkout:

```sh
python3 scripts/build.py --adapter opencode
# Run from the CLI checkout; pass the actual export path.
python3 scripts/opencode_skill_probe.py --opencode /absolute/path/to/opencode --agents-export /path/to/agents/dist/opencode
```

Retained [native registry evidence](../evals/observed/native-loading-docs-2026-10-14/result.json)
and [source identities](../evals/observed/native-loading-docs-2026-10-14/sources.json)
identify the tested bytes. This verifies registered content, not model adherence,
team scheduling or all host versions. The native-host CI job fetches the exact integrity-pinned OpenCode 2.0.27 package
and checks current source exports plus a pinned Skills snapshot without model calls.
The workflow pins its shared probe/tooling revision separately.

Individual profile/team selection has deterministic regression coverage for exact
rosters, coordinator inclusion, deduplication and unknown-ID refusal before writes.
The existing installer still protects local edits, backs up replaced managed
content and preserves unrelated outputs. These tests operate in temporary targets.

## Observed content/GEO task

An independent evaluator used the 4 explicit content/GEO skills on 1
[synthetic offline task](../evals/observed/content-geo-review-2026-10-14/input.md).
The [retained result](../evals/observed/content-geo-review-2026-10-14/result.md)
produced a brief, factual edit, newsletter/social adaptations and GEO analysis.
The social draft counted 165/200 characters. Coverage was 4/6, mention and
owned-domain citation rates 2/4, and supporting-citation rate 1/4; missingness,
unsupported certification and noncausal comparisons were distinguished.

[The manifest](../evals/observed/content-geo-review-2026-10-14/manifest.json)
records source/artifact hashes and scope. This is 1 supplied-evidence task,
not live SEO/GEO performance or execution of canonical acceptance cases. The canonical specification objects retain `not_run`;
[observed role smoke cases](../evals/README.md) now cover 3 of 128 cases.
Skill case specifications remain separate from these observed role outcomes. Earlier finance and crypto/forecast
observed tasks remain separate evidence in `evals/observed/`.
