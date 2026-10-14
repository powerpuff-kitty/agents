# Pending-change review

Two confirmed correctness regressions need correction. Review only; no source, index, tracker, or configuration edits were made.

## Findings

1. **P2 — Percentage discounts are subtracted as dollar amounts.** Location: `workspace/pricing.py:2` (staged change). `CONTRACT.md:1` defines the argument as percentage points. For a $60 subtotal, `quote(2, 30, discount_percent=10)` must return $54, but the pending implementation returns $50. This misprices orders whenever the discount is nonzero and the subtotal differs from $100. The new caller `checkout.py:4` happens to use a $100 subtotal, so its quote of $90 is correct by coincidence and does not validate this change. HEAD returns $54 for the reproduction. Confidence: high; demonstrated against both source states. Restore percentage-based calculation, preserving dollar units; verify non-$100 subtotals and zero/100% discounts.

2. **P2 — Dollar formatting divides already-dollar values by 100.** Location: `workspace/display.py:2` (unstaged change). `CONTRACT.md:1` says `dollars` receives dollars. `dollars(90)` now returns `$0.90`, whereas HEAD returns `$90.00`. This is reachable through the new `checkout.py:1-4`: its quote is 90 dollars, and invoking `checkout()` returns `$0.90` instead of `$90.00`. Nonzero displayed amounts are scaled incorrectly; a zero-only check would miss it. Confidence: high; direct and integrated reproductions agree. Format the dollar input directly; verify positive, zero and negative values plus the checkout result.

P2 here means an actionable functional defect to correct in this change; no project-specific priority rubric was supplied. These are separate causes, requiring separate fixes.

## Scope and accepted behavior

Base: HEAD `2cf1fb372f674b06c63f039487b09662610d6085`. Compared the complete pending state against HEAD: staged `pricing.py`, unstaged `display.py`, and untracked `checkout.py`. `git diff HEAD` alone omits the untracked caller, which was read separately. No pending files were excluded. The repository contains only `CONTRACT.md` and these three Python files outside `.git`; no repository instruction file, tests, package configuration, or CI configuration was present in the enumerated files.

Accepted requirements come from `CONTRACT.md:1`: prices and formatter inputs are dollars, discounts are percentage points, and checkout uses those contracts. HEAD implementations were also inspected to distinguish regressions from baseline behavior.

## Checks and limits

- Attempted Python reproduction with `python -B`: exit 127, executable unavailable. Retried with `python3 -B`.
- `python3 -B` ran five contract examples against HEAD functions loaded in memory and pending functions, plus the actual new checkout function. Exit 1 intentionally reports the observed failures. HEAD passed all five examples; pending passed two and failed three: quote on a $60 subtotal, formatting $90, and composed checkout. Actual `checkout()` returned `$0.90`.
- `git diff --check` and `git diff --cached --check`: exit 0. These verify whitespace only.
- Final status preserved ` M display.py`, `M  pricing.py`, `?? checkout.py`; no bytecode was generated (`-B`).

There was no native test/build harness to run. The short examples are focused reproductions, not exhaustive numeric-boundary tests or whole-product readiness evidence. No benchmarks or rating were requested or warranted. No accounts, network, publication, fixes, commits, or tracker operations were used. No unresolved requirement question prevents these findings. Exact commands and outputs are retained in `actions.log`.

## Exact files read

Instructions/task:
- `/private/tmp/behavior-review/task.md`
- `/private/tmp/behavior-review/instructions/role.md`
- `/private/tmp/behavior-review/instructions/skill/SKILL.md`
- `/private/tmp/behavior-review/instructions/skill/references/review-method.md`

Workspace files:
- `/private/tmp/behavior-review/workspace/CONTRACT.md`
- `/private/tmp/behavior-review/workspace/pricing.py`
- `/private/tmp/behavior-review/workspace/display.py`
- `/private/tmp/behavior-review/workspace/checkout.py`

Also read Git HEAD versions of `pricing.py` and `display.py`, HEAD identity/tree names, pending diffs and status. No other repository or evaluation material was read.
