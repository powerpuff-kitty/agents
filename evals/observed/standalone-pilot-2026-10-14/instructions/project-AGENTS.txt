# Project instructions

This repository owns reusable agent instruction profiles, not project product
truth or an autonomous agent runtime.

- Canonical role metadata and specialist instructions live in `agents/<id>/`.
  The shared operating contract lives in `shared/operating-contract.md`.
- Portable team assignments and stage/completion policies live in `teams/*.json`.
  Keep host macros, command syntax, and coordinator mode mappings in adapters.
  Preserve sequential dependencies, 1 source writer, conditional review reasons,
  and the distinction between workflow instructions and an enforced scheduler.
- Pack membership and dependencies live in `packs/*.json`. Keep 1 owner per
  role/team, cover the full catalog, and validate dependency closure. Adaptive
  team candidates may be omitted from a pack export when their role is unavailable;
  fixed workflows must resolve all members. Individual --agent selection adds only
  the named profile; explicit --team includes its coordinator and declared roster.
  Selectors combine without duplicates. Selection never silently removes
  previously installed files.
- Put tool-specific formatting, host guidance, and capability mapping in
  `adapters/<tool>/`. Keep neutral sources free of vendor tool APIs and permission
  configuration. Preserve task authorization, evidence, and completion semantics.
- `dist/` is generated and ignored. Edit sources/adapters, then rebuild; do not
  maintain independent handwritten copies of the same role for each tool.
- Use Python 3.10+ standard-library tooling. Do not add dependencies without a
  concrete need. Document actual implemented support, not hypothetical adapters.
- Installation must preserve unrelated profiles, back up replaced content,
  protect local edits, and remain idempotent. Do not silently widen permissions.
- Evaluation scenarios are specifications. Only actual retained model executions
  can establish behavioral outcomes; deterministic validators must not claim them.
- Authored profiles and tooling use the root MIT [LICENSE](LICENSE).
  [INSTALL.md](INSTALL.md) owns the copyable installation prompt; installing
  profiles and installing skills are separate scopes. Installation, default
  validation and native-host CI must work without a CLI or Skills checkout;
  keep optional cross-catalog checks explicit and downstream integration pins
  owned by their consumer.
- Follow [README.md](README.md) for usage, [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
  for source/adapter boundaries, [docs/FINANCE.md](docs/FINANCE.md) for finance
  scope and worked examples, [docs/CRYPTO.md](docs/CRYPTO.md) and
  [docs/FORECASTING.md](docs/FORECASTING.md) for the related packs, and [evals/README.md](evals/README.md) for evaluation.

Before completing a change, run:

```sh
python3 scripts/validate.py
python3 scripts/check_docs.py
python3 scripts/build.py --adapter portable
python3 scripts/build.py --adapter opencode
python3 scripts/build.py --adapter portable --check
python3 scripts/build.py --adapter opencode --check
python3 -m unittest discover -s tests -v
```

If installation is part of the task, also verify loaded profiles and team command
registration in the actual selected host with
an explicit executable and document any unavailable checks. Preserve user work
and existing project instructions in repositories these agents later inspect.
