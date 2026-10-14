# Independent source audit: Agents

Snapshot: `/private/tmp/independent-audit-agents` at **f374ffbb543595486c8c5145884c123d77e88020** (detached worktree), audited 2026-10-14. Runtime: Python 3.14.7. Tracked worktree and index were clean before and after checks. No tracked source was edited, packages installed, personal host configuration changed, model invoked, publication performed, or external account accessed.

This audit used the repository's root `AGENTS.md`, README/INSTALL and architectural documentation, the codebase-audit procedure, raw canonical/profile/team/pack sources, adapters, scripts, tests and CI configuration. The inherited TCSN `.agentic` routing did not describe this distinct repository; `.agentic/README.md` and `.agentic/manifest.yaml` are absent here. Historical retained evaluation/review conclusions, other conversations and other agents' findings were not used.

The deterministic checks pass in the normal local environment. Four narrower defects were reproduced independently. None establishes a high-severity exploit or a failed model workflow. Priorities below are relative maintenance priorities, not a fabricated readiness score.

## Confirmed findings, ranked

### 1. P2 — Source decoding depends on the machine's locale

**Location:** `scripts/build.py:24` and `scripts/build.py:36`; the same implicit text encoding pattern occurs in other source reads. `README.md:15` and `AGENTS.md:24` specify Python 3.10+ without a UTF-8 locale prerequisite.

**Trigger:** Run the documented tooling where Python's default text encoding is not UTF-8. The checked-in instructions contain UTF-8 punctuation. `Path.read_text()` without `encoding=` uses the process default, so the compiler cannot reliably read its own canonical sources. Installation and validation also call this compiler.

**Observed reproduction:**

```sh
env LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 python3 scripts/build.py --adapter portable --output /private/tmp/fresh-agents-build-c-locale
```

Exit **1**:

```text
Build failed: 'ascii' codec can't decode byte 0xe2 in position 2407: ordinal not in range(128)
```

A preceding locale query returned `US-ASCII`. The isolated reproduction script repeats this failure in a temporary destination.

**Impact:** A valid Python installation with a non-UTF-8 locale cannot build or install the catalog. Other default encodings can decode bytes incorrectly rather than fail, altering prompt text. The observed failure is confirmed; other operating systems/default encodings were not executed.

**Remediation:** Read checked-in text explicitly as UTF-8 throughout the tooling, and write exports with a specified encoding. Add a small subprocess regression check with UTF-8 mode/coercion disabled or otherwise verify the explicit encoding path.

**Confidence:** High for the reproduced locale failure; no native Windows claim is made.

### 2. P2 — Standalone exports and installed profiles omit the source license notice

**Locations:** `scripts/build.py:257-275`, `adapters/portable/render.py:4-17`, `adapters/opencode/render.py:5-33`, and `scripts/install.py:105-108`. Relevant source contract: `LICENSE:3-13`, `INSTALL.md:26` and `INSTALL.md:84-85`.

**Trigger:** Build either adapter's export, or install even a single profile using the documented installer. Renderers compose the role/shared/host instructions but no copyright or permission notice. The compiler adds only its build manifest; the installer accepts only the generated profile/command Markdown and adds its management state.

**Observed reproduction:** Both temporary full exports have no `LICENSE`. With a `financial-analyst`-only installation, the entire installed inventory was:

```text
agents/.agents-managed.json
agents/financial-analyst.md
```

The isolated reproduction scanned all compiled output text for the root permission notice: **false** for both adapters. The installed profile also lacks it.

**Impact:** A portable export or installed collection taken independently from the checkout does not carry the notice that the repository itself says to retain with substantial copies. This is a concrete packaging/documentation-contract mismatch; this audit does not give a legal compliance opinion. A user retaining the entire source checkout separately still has its root LICENSE.

**Remediation:** Include the root notice in generated distributions and preserve an appropriate notice artifact in installations, without making the host discover a license document as an agent/command. Cover standalone and selected-profile paths. Updating only the installation prompt would not fix direct documented CLI usage.

**Confidence:** High.

### 3. P3 — `build --check` can pass while exported bytes contradict the manifest hash

**Locations:** `scripts/build.py:271-272` hashes UTF-8 output bytes, but `scripts/build.py:292-294` checks output using newline-normalizing text reads. `scripts/build.py:306` also writes text using platform-default newline handling.

**Trigger:** Change one generated file from LF line endings to CRLF, without changing its text. This can happen through editor or cross-platform checkout/copy behavior.

**Observed reproduction:** Build a temporary portable export for `financial-analyst`, replace its output bytes with `bytes.replace(b'\n', b'\r\n')`, compare its SHA-256 with `build-manifest.json`, then call `build(..., check=True)` for the same selection:

```text
manifest_hash_matches_actual_file False
check_passed True
```

This was reproduced on the current machine without a Windows host or renderer mutation. The retained reproduction script contains the exact steps.

**Impact:** The advertised deterministic/drift check does not verify the byte identity promised by its own `output_sha256`. A consumer verifying exported hashes rejects an artifact that this check labels verified. The reproduced difference is line endings; this is not evidence that arbitrary changed instructions evade checking.

**Remediation:** Define export bytes as UTF-8/LF, write those bytes, and compare bytes or verify actual output digests in check mode. A regression should assert that hash mismatch cannot coexist with a passing check.

**Confidence:** High; modest practical severity because the reproduced prompt text is semantically unchanged.

### 4. P3 — Updating management state widens a pre-existing restricted file mode

**Locations:** `scripts/install.py:90-92` calls `atomic_write` without preserving the state file's existing mode; `scripts/install.py:20-25` defaults to `0644`. Profile replacement already preserves its previous mode at `scripts/install.py:86-87`. Relevant preservation contract: `AGENTS.md:26-27`, `INSTALL.md:23`.

**Trigger:** Set an existing `.agents-managed.json` to `0600`, then add another selected profile or otherwise change the managed hash mapping.

**Observed reproduction:** In a temporary installation, install `financial-analyst`, chmod only its management file to `0600`, then install `quant-researcher` into the same target:

```text
state_before_update 0o600
state_after_update 0o644
```

**Impact:** An installer update silently removes an administrator/user's restriction on group/other reading. The current state contains profile names, hashes and repository metadata, not credentials, so no secret disclosure is claimed. This is primarily a permission-preservation defect.

**Remediation:** Preserve the existing state file's mode when atomically replacing it, as is already done for managed profiles. Consider respecting the process umask for newly created metadata rather than unconditionally chmodding it to `0644`.

**Confidence:** High.

## Executed checks and results

All commands ran from the audited snapshot unless an absolute temporary script path is shown.

| Command/check | Actual result |
| --- | --- |
| `git status --short`; `git rev-parse HEAD` | Clean; revision recorded above |
| `cat AGENTS.md .agentic/README.md .agentic/manifest.yaml` | Root instructions read; missing `.agentic` paths reported; command exit 1 for those absent paths |
| `python3 scripts/validate.py` | Exit 0; 34 agents, 20 teams, 7 packs, 124 scenario specifications; host/command loading not checked, model behavior not run |
| `python3 scripts/check_docs.py` | Exit 0; 77 Markdown files checked, no supported-local-path/count errors; checker explicitly excludes URL/fragment/render/prose-truth verification |
| `python3 -m unittest discover -s tests -v` | Exit 0; all 32 tests passed |
| `python3 scripts/build.py --adapter portable --output /private/tmp/fresh-agents-build-portable` | Exit 0 |
| `python3 scripts/build.py --adapter opencode --output /private/tmp/fresh-agents-build-opencode` | Exit 0 |
| Same portable build command with `--check` | Exit 0 |
| Same OpenCode build command with `--check` | Exit 0 |
| C-locale build command above | Exit 1 with UTF-8 source decoding failure |
| `python3 /private/tmp/fresh-agents-audit-repros.py` | Exit 0; independently reproduces all four findings in temporary directories |
| `git status --porcelain=v1`; `git diff --exit-code`; `git diff --cached --exit-code` | No output; all exit 0 after checks |
| `python3 --version` | Python 3.14.7 |

Additional read-only inspection used `rg --files`, `cat`, `sed`, `nl`, `wc`, and short Python snippets over canonical sources and temporary outputs. Builds/checks used temporary destinations instead of the worktree's default `dist/`.

## Architecture and instruction assessment

Source ownership is explicit: canonical role metadata/instructions, one shared contract, neutral team JSON, pack ownership/dependencies, and tool-specific renderers. Source validation exercises catalog closure, IDs, assignment/writer constraints, pack coverage and case coverage. Tests cover selection isolation, team dependencies, deterministic export drift, installer preservation/conflicts/backups/idempotence and several workflow ordering rules. The passing suite supports those deterministic claims only.

The shared and sampled role/coordinator instructions preserve user authorization, unrelated working changes, scoped remediation, evidence limits, independent review, serialized writers and completion semantics. Team source explicitly distinguishes stage instructions from an enforced scheduler. No additional actionable profile instruction defect was confirmed in this sampling. All catalog JSON was loaded by validation; manual procedural reading focused on the shared/team-lead, implementation/review/readiness and finance/crypto/forecast boundaries rather than claiming a behavioral evaluation of every role.

## Preferences and optional improvements (not defects)

- Installed management state records output hashes and repository identity but no retained build manifest/source revision. Persisting a source/build identity beside the installation could simplify provenance after deleting a temporary checkout. Current architecture documentation promises installed hash tracking, so this is not reported as a separate contract violation.
- Optional native command validation intentionally checks registration names/descriptions rather than command body/coordinator flags. Broader command-content validation would provide stronger evidence if the host API exposes it. Current documentation describes this limit, so the audit does not call it a false model-behavior claim.
- No numerical repository/agent readiness score is assigned; a meaningful behavior/reliability score would need actual task executions and a declared rubric.

## Unverified areas and limits

- No actual OpenCode executable, running host registry, installed personal profile, permissions configuration, reload, or named-team workflow was inspected or modified. Host compatibility and model adherence are unverified here.
- No actual behavioral/model session was run; the 124 cases are specifications. Prior retained results were not opened or independently authenticated.
- CI YAML and pinned external-tool references were inspected, but GitHub Actions and the external native-host/skill probe were not executed or fetched.
- Python 3.10 itself, other Python versions, Windows and other filesystem/locale combinations were not run. The C-locale failure and LF/CRLF check discrepancy are local reproductions under Python 3.14.7.
- No dependency installation, package scanner, performance benchmark, intrusive test or production test occurred. The tooling uses the Python standard library; adapter code executes trusted repository renderer source by design.
- Installer failure/concurrency handling is not a directory-wide transaction; documentation explicitly discloses this. No atomic multi-destination guarantee is inferred.
- External links, current provider APIs, accounting/financial/legal standards and real market/chain data were not validated. Synthetic documentation arithmetic was inspected, not treated as financial advice or proof of specialist reliability.

Retained artifacts: this report and `/private/tmp/fresh-agents-audit-repros.py`. No repository remediation was applied.
