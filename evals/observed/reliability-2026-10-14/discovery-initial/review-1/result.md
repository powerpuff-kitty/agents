# Pending-change review

1. **P1 — Apply the discount as a percentage, not a dollar subtraction.** At `workspace/pricing.py:2`, the staged expression `quantity * unit_price - discount_percent` violates `workspace/CONTRACT.md:1`, which defines discount percentage points. For `quote(3, 50, 10)`, the working tree returns 140 dollars instead of 135; for `quote(1, 50, 100)`, it returns -50 instead of zero. Both checks pass against HEAD. The new caller at `workspace/checkout.py:4` exercises this API, but its subtotal of 100 makes its 10% discount coincide with subtracting 10 dollars and therefore masks this defect. Restore percentage multiplication, and verify non-100 subtotals and a full discount. Confidence: confirmed by source and execution.

2. **P1 — Keep the formatter's input in dollars.** At `workspace/display.py:2`, dividing the input by 100 violates `workspace/CONTRACT.md:1`: `dollars` already receives dollars. `dollars(90)` now produces `'$0.90'` instead of `'$90.00'`. The new caller `workspace/checkout.py:4` makes the defect directly observable: `checkout()` returns `'$0.90'`, whereas its contract requires `'$90.00'`. Remove the conversion and verify both direct formatting and the checkout composition. Confidence: confirmed by source and execution.

## Scope and checks

Reviewed the complete pending change against HEAD `84ab0fba8a67385ccd42ca6d3b79d8e9fb8b0d9c`: staged `pricing.py`, unstaged `display.py`, and untracked `checkout.py`, plus the complete tracked contract and baseline implementations. The fixture contains no test suite or package/build configuration.

Selected `instructions/skills/change-review/SKILL.md`, its `references/review-method.md`, and `instructions/roles/quality-engineer/instructions.md` from `instructions/catalog.md`. The first defines the pending-diff review and caller tracing; the role supplies correctness and verification discipline. No additional specialist procedure was needed for these deterministic arithmetic and unit-contract failures.

Executed seven focused comparisons using Python 3.14.7 with `-B`: three current checks passed and four failed, representing the two findings above. All seven HEAD behavior comparisons passed. For the new checkout, the HEAD comparison is the equivalent composition of the two baseline functions, not a nonexistent baseline checkout file. The reproduction intentionally exited 1 on observed contract failures. Both staged and unstaged whitespace checks exited 0. Exact commands and results are in `actions.md`.

The workspace was not edited. Final status matched the initial status, all four file SHA-256 values were unchanged across verification, and no bytecode cache existed. No commits, network, installs, accounts, publication, index changes, or tracker/configuration changes occurred.

## Limits

This is a focused fixture review, not a build, browser, production, security, or release assessment. No repository-native suite was available. I did not author the pending changes. This ran in a separate task session, but full host-side history isolation is not authenticated here. Host identity, concrete model identifier, token use, and timing/cost metrics were not available and are not claimed. No excluded evaluator files or other trials were read.

