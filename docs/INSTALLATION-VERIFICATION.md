# Installation and task verification

Observed 2026-10-14 with OpenCode v2.0.27. A disposable Git project and private
persistent server registered **62 native skills, 35 agent prompts and 20 team
commands**. Skill paths and Markdown bodies and complete agent prompt bodies
matched their source exports. Team command names were present. No model call,
account change or existing host configuration write occurred.

The first skill inventory can be empty while configuration plugins initialize;
bounded repeat queries on the same server resolve that startup race. Repeatedly
starting a fresh standalone server can repeat the empty snapshot. Native folders
need no skill adapter. Use current [V2 skill documentation](https://opencode.ai/v2/docs/skills/),
which is separate from V1 configuration documentation.

Check profiles independently from this AI Agents checkout with an explicit host:

```sh
python3 scripts/build.py --adapter opencode
python3 scripts/opencode_probe.py --opencode /absolute/path/to/opencode --expected-version 2.0.27 --agents-export dist/opencode
```

The probe uses a disposable project, home/configuration directories and a private
persistent server. It checks complete profile bodies and command names without an
AI Skills or CLI checkout, installing skills, or invoking a model. The earlier combined
AI Skills/AI Agents observations above remain evidence for their recorded revisions.
A separate 2026-10-14 run of this profile-only probe registered all 35 prompts
and 20 command names on OpenCode v2.0.27 without installing any skills.

The latest [native registry evidence](../evals/observed/reliability-2026-10-14/native-host.json)
and [source identities](../evals/observed/reliability-2026-10-14/source-inputs.json)
identify the reliability-method run. Earlier [design-extraction evidence](../evals/observed/design-extraction-2026-10-14/native-host.json)
remains historical. This verifies registered content, not model adherence,
team scheduling or all host versions. The native-host CI job fetches the exact integrity-pinned OpenCode 2.0.27 package
and checks current source exports without model calls. The host package lock,
fetcher and profile probe live in this repository. No cross-repository checkout or
coordinated release is needed. The Linux fetcher verifies the locked archive
integrity before extracting its single executable; on other platforms pass an
existing supported executable explicitly.

Separate [ordinary-prompt native trials](../evals/observed/native-routing-2026-10-14/README.md)
used DeepSeek with verified fixture locations and all 62 skills/35 profiles visible
before prompting. All 3 used built-in `build`; none invoked a skill or subagent or
selected a custom profile. Use a named profile or team command for deliberate
specialist selection. Installation visibility does not guarantee implicit use.
The retained attempts include quota refusal, wrong-project activity and a corrected
rerun; host session success is assessed separately from task acceptance.

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
[observed role smoke cases](../evals/README.md) now cover 8 of 144 cases.
Skill case specifications remain separate from these observed role outcomes. Earlier finance and crypto/forecast
observed tasks remain separate evidence in `evals/observed/`.
