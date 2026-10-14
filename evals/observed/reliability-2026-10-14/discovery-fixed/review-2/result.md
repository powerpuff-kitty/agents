# Pending change review

Two confirmed high-priority defects require correction. Review only; no source, index, tracker or configuration edits were made.

1. **P1 — Percentage discount is treated as a dollar subtraction.** `workspace/pricing.py:2` replaces percentage multiplication with `quantity * unit_price - discount_percent`, violating `workspace/CONTRACT.md:1`. With `quote(3, 50, 10)`, the pending code returns **140**, expected **135**; `quote(3, 50, 100)` returns **50**, expected **0**. The unchanged public signature at line 1 still advertises percentage points. HEAD returns 135.0 for the first case. Restore percentage arithmetic using the subtotal, then verify zero, partial and full discounts on subtotals other than $100. Confidence: source-confirmed and reproduced.

2. **P1 — Dollar formatter reduces amounts by a factor of 100.** `workspace/display.py:2` divides an input already expressed in dollars by 100, violating `workspace/CONTRACT.md:1`. `dollars(90)` now returns **'$0.90'**, expected **'$90.00'**; HEAD produces the expected result. The relevant untracked caller `workspace/checkout.py:1-4` imports both changed functions and exposes this defect: `checkout()` returns **'$0.90'** instead of **'$90.00'**. Remove the cents conversion and recheck the formatter plus checkout integration. Confidence: source-confirmed and reproduced.

The checkout example has a $100 subtotal, where subtracting 10 dollars accidentally equals a 10% discount. It therefore does not expose finding 1; the separate $150-subtotal check does. No additional defect is established in the new caller itself.

## Scope and selected instructions

Compared HEAD `7b8215b3357290c7a045dd63e60accdefe8e554b` with the complete pending work: staged `pricing.py`, unstaged `display.py`, and untracked `checkout.py`. Read all four workspace source/contract files and searched all callers. The index and worktree diffs were inspected separately and the combined HEAD diff was checked. No pending source was excluded.

Read `instructions/operating-contract.md` before selecting `quality-engineer` (responsibility for correctness and verification) and `change-review` (focused pending-diff procedure), including its review method. Selected `structured-reflection` after concrete contract failures, including its method and report template, to retain observed evidence and bounded correction proposals. No broad audit, security, performance, release, implementation or team procedure was needed. These are fixture catalog instructions, not ambient project rules.

## Actual verification

- Python 3.14.7, invoked with `python3 -B`: five focused comparisons, **1 passed / 4 failed**, process exit 1. Zero discount passed. Partial discount, full discount, dollar formatting and checkout failed with the values above.
- Executed original HEAD pricing/display functions in memory using `git show`; the partial-discount, formatter and composed checkout-argument baseline checks returned 135.0, '$90.00', '$90.00' respectively. No checkout file exists in the tracked baseline.
- Parsed every Python source with `ast.parse`: all three passed. No bytecode cache was created.
- `git diff --check` and `git diff --cached --check`: both passed (exit 0). These establish whitespace checks only.
- No repository test suite or test configuration exists among the four fixture files. These are direct reproductions, not a claim of comprehensive test, browser, build, production or release verification.

## Reflection record

- Attempt/snapshot: this pending review against the pinned HEAD and unchanged source hashes in actions.md.
- Trigger/status: findings 1 and 2, actual failed comparisons; reflection completed.
- Observed facts: percentage arithmetic is wrong away from a $100 subtotal; formatter scales dollar inputs incorrectly. A checkout-only pass for pricing would be an unsupported assumption.
- Cause: the changed expressions directly contradict the explicit unit contracts; no unknown business requirement is needed to explain the failures.
- Bounded correction: restore percentage arithmetic and dollar formatting, then rerun the failing cases and neighboring valid inputs. Review-only authority permits recommendations; corrections were not performed. Stop when these failures are resolved without changing the contracts, or report conflicting new requirements.
- Actual recheck: source syntax, whitespace and preservation checks ran; no corrected-source recheck exists because source was not edited.
- Candidate memory: none; remaining gap is validation of a future correction.

## Preservation and limitations

Workspace and instruction tree fingerprints were unchanged before/after the executable checks, including the Git metadata files captured by the workspace hash. Source hashes, HEAD, staged blob identities and status also remained unchanged. See actions.md for evidence and methodological limits. Only the three requested output artifacts were written outside those read-only trees.

No network, package installation, accounts, personal configuration, commits, publication or delegation was used. No initial.json, grader source, other trials or author/reviewer notes were read. A mechanical preservation fingerprint did read bytes across all instruction files (rather than only selected instruction contents); unrelated instructions were not semantically inspected. This exceeded the narrow selected-instruction reading intent and is disclosed rather than omitted. The broad file-name inventory also listed catalog asset paths. Host identity, model and usage are unknown. This standalone review did not author the source; no separate independent reviewer was spawned and no comprehensive isolation certification is claimed.
