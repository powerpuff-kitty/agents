# Onchain and DeFi research

The `crypto` pack owns onchain-analyst and `/team-crypto-review`. It depends on
finance, science-data and core through dependency closure: 22 profiles and 12
workflows. The full catalog has 35 profiles, 20 workflows and 7 packs.

## Responsibilities and methods

[Onchain analyst](../agents/onchain-analyst/instructions.md) owns chain/protocol
research and evidence. Security-auditor owns scoped contract exploitability;
portfolio-risk-analyst owns relevant economic/holdings scenarios. A role title
does not provide blockchain access, an audited contract or a wallet runtime.

| Skill | Scope and resource |
| --- | --- |
| [onchain-data-analysis](https://github.com/powerpuff-kitty/ai-skills/tree/main/onchain-data-analysis) | Chain/block/finality, event/state semantics, integer token units, coverage and attribution. |
| [smart-contract-review](https://github.com/powerpuff-kitty/ai-skills/tree/main/smart-contract-review) | EVM/Solidity source/control paths, accounting, signatures, upgrades and actual deployment-match evidence. Other contract languages need their own supported method. |
| [defi-risk-analysis](https://github.com/powerpuff-kitty/ai-skills/tree/main/defi-risk-analysis) | Mechanism-specific collateral/liquidation, AMM/LP, liquidity/oracle/governance/dependency scenarios. |

Each standalone skill includes a focused guide, report template and 6 unrun
acceptance specifications. Install skills separately via the Skills [installation
prompt](https://github.com/powerpuff-kitty/ai-skills/blob/main/INSTALL.md). Missing
skills permit bounded direct methods rather than automatic installation.

## Select the pack

```sh
python3 scripts/validate.py --pack crypto
python3 scripts/build.py --adapter portable --pack crypto
python3 scripts/build.py --adapter opencode --pack crypto
python3 scripts/install.py --pack crypto --dry-run
python3 scripts/install.py --pack crypto
```

Use the actual intended destinations and preserve customizations per [INSTALL.md](../INSTALL.md).
These commands describe an authorized installation; they are not a record of a
personal-host change. Installing profiles does not connect wallets or install skills.

## Worked requests and expected evidence

The following are synthetic examples, not observed model outcomes.

- “Analyze these transfers.” Raw amount 123456789 at corroborated decimals 6 is
  123.456789 tokens. Chain/address/block hash, success and canonicality matter;
  duplicate events, failed attempts and orphaned blocks cannot inflate completed
  transfer counts. Partial logs or a rebasing token do not prove a full balance.
- “Review this withdrawal source.” Trace actual guards and the state/external-call
  sequence. A reachable accounting/callback risk can be reported for supplied
  source, but a deployed exploit requires deployment/implementation and prerequisite
  evidence. An effective invoked guard is counterevidence. No live exploit is run.
- “Stress this lending position.” With collateral value 120, threshold .75 and debt
  60, the declared simple health factor is 1.5. A collateral-only -40% shock gives
  .9. This models a threshold breach; it does not establish actual liquidation,
  liquidation amount or maximum loss.
- “Explain this LP comparison.” In a fee-free full-range constant-product model,
  relative price ratio 4 gives LP/HODL value .8, or -20% relative to holding the
  original assets. It is not a -20% USD return or a concentrated-liquidity result.

A useful report pins the actual snapshot and mechanism, traces units/parameters,
shows calculations/counterevidence and names missing coverage. No snapshot means
no current factual position-risk number. Contract correctness, economic exposure,
finality, liquidity and administrator trust remain distinct questions.

## Workflow and evidence limits

`/team-crypto-review <scope>` frames chain/protocol identity, checks supplied data,
then selects onchain, contract-security and economic reviews as needed. Independent
checks follow completed analysis. Onchain-analyst is the sole writer only when a
saved artifact was requested; the actual artifact is checked after writing.

The workflow does not retrieve keys, sign/approve, bridge, borrow, move funds,
claim rewards or execute swaps. It does not provide cryptographic protocol proof,
non-EVM expertise by default, financial execution or an eligibility certification.
Source checks, generated profiles, isolated installs, native loading and observed
reasoning have separate evidence; acceptance specifications remain not_run.

1 [retained independent synthetic skill review](../evals/observed/crypto-forecast-review-2026-10-14/manifest.json)
checks chain/finality, contract counterevidence, DeFi scenarios, odds/fees, proper
scores and settlement boundaries. Reports and exact arithmetic are retained; this
is not a profile/host-loading evaluation or broad outcome benchmark.
