# Project instructions

This repository owns reusable agent instruction profiles, not project product
truth or an autonomous agent runtime.

- Canonical role metadata and specialist instructions live in `agents/<id>/`.
  The shared operating contract lives in `shared/operating-contract.md`.
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
- Follow [README.md](README.md) for usage, [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
  for source/adapter boundaries, and [evals/README.md](evals/README.md) for evaluation.

Before completing a change, run:

```sh
python3 scripts/validate.py
python3 scripts/build.py --adapter portable
python3 scripts/build.py --adapter opencode
python3 scripts/build.py --adapter portable --check
python3 scripts/build.py --adapter opencode --check
python3 -m unittest discover -s tests -v
```

If installation is part of the task, also verify the actual selected host with
an explicit executable and document any unavailable checks. Preserve user work
and existing project instructions in repositories these agents later inspect.
