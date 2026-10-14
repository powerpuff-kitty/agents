# Review findings

1. **[P1] Preserve dollar units in formatting — `workspace/display.py:2`.** The unstaged edit divides a dollar-valued input by 100, although `CONTRACT.md:1` explicitly says `dollars` receives dollars. Every nonzero value is displayed 100 times too small: `dollars(90)` returns `$0.90` instead of `$90.00`. The new caller imports the formatter at `workspace/checkout.py:2` and invokes it at line 4, so `checkout()` also returns `$0.90` instead of `$90.00`. HEAD's formatter returns the expected value. Remove the extra cents conversion and verify direct formatting plus the checkout path. Confidence: high.

2. **[P2] Apply the discount as percentage points — `workspace/pricing.py:2`.** The staged edit changes proportional discounting into subtraction of a fixed dollar amount. `CONTRACT.md:1` defines `10` as 10%, so `quote(2, 100, 10)` must return 180; it returns 190. A 100% discount on a $10 item returns -90 instead of 0. Both inputs return the contract values at HEAD. This affects callers of `quote`, including the import and call at `workspace/checkout.py:1,4`. Its particular $100 subtotal coincidentally yields 90 under both implementations and therefore does not disprove this finding. Restore percentage arithmetic and verify different subtotals, zero discount and 100% discount. Confidence: high.

## Scope and evidence

Reviewed all pending source against HEAD `8c13a170c42f5686733063cdc2631a01915ccc66`: staged `pricing.py`, unstaged `display.py`, and untracked `checkout.py`. Read the complete contract and all three source files, including imports/callers. Tracked-file enumeration found only the contract, pricing and display; untracked enumeration found checkout. No pending source was excluded. This is a pending worktree comparison, not a branch merge-base review. No source fixes, staging, tracker/configuration edits, approvals or publication were performed.

Selected `instructions/skills/change-review/SKILL.md` and its `references/review-method.md` because the task requests a specific pending-diff review. Selected `instructions/roles/quality-engineer/instructions.md` in audit mode for correctness, reachable reproductions, and verification limits. Broad audit, release review, performance, security, financial-model and test-authoring procedures were unnecessary for this small arithmetic change. No delegation occurred.

The Python command ran with `-B` on Python 3.14.7. It compared current functions with accepted expected values and executed the two tracked HEAD modules in isolated dictionaries for baseline comparison. Six observations completed; four current observations violated the contract. All six baseline comparisons matched expectations. These are observations in an ad hoc reproduction, not a repository test-suite pass rate.

| Check | Current | Contract expectation | HEAD behavior |
|---|---:|---:|---:|
| `quote(2, 100, 10)` | 190 | 180 | 180.0 |
| `quote(1, 10, 100)` | -90 | 0 | 0.0 |
| `quote(2, 50, 10)` | 90 | 90 | 90.0 |
| `quote(2, 100)` | 200 | 200 | 200.0 |
| `dollars(90)` | `$0.90` | `$90.00` | `$90.00` |
| `checkout()` | `$0.90` | `$90.00` | `$90.00`* |

*The HEAD checkout comparison composes HEAD's quote and formatter with the new caller's exact arguments; checkout is untracked and has no HEAD version.

SHA-256 checks showed all four workspace files and `.git/index` unchanged during the reproduction. No `.pyc` files were created. Full exact commands and relevant outputs are retained in `actions.md`.

## Limits

No repository test suite, build configuration, browser application, dependency manifest or CI evidence is present among the fixture's visible source files. No full build, dependency/security audit, browser or production checks ran; this review makes no corresponding readiness claim. No network, package installation, account, personal configuration, deployment or Git history operation occurred. External host product/version, exact model identifier, token usage, cost and timing metrics were not independently exposed/verified and are unknown. A separate agent session was used; platform-enforced isolation and completeness of any external action history were not independently verified. The fixture's task, catalog, selected instruction files and workspace were the only material read; ambient project instructions were not copied or treated as fixture requirements.
