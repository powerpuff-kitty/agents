# Acme supplied-observation comparison

This offline review contains four retained answers, not a controlled before/after experiment. The later answers mention Acme more often, but every prompt, the model identifier and locale changed. There are **zero matched prompt/model/locale cells**. These observations cannot measure the content update's effect or establish a visibility improvement.

## Scope and evidence

Brand: Acme. Alias rule: exact, case-sensitive whole-word `Acme`; repeated occurrences within one answer count once. Audience is unspecified; query intent is CSV tool discovery in the before wave and direct product fact checking in the after wave. Geographic audience cannot be inferred from locale. The only observed competitor is Beta; no comparison set was predefined.

Source: `/private/tmp/behavior-geo/workspace/observations.json`, SHA-256 `fd0287fa6a1729a7e2d296667ac45ed4db4fc59ba1246eb23bc7312023391e82`. Observation IDs below are assigned in this report and map to JSON array indices. Raw response text and URL strings remain in that artifact; no separate per-answer hash is implied. Date, model and locale are supplied metadata, not independently verified provider identities. No live URL retrieval, provider query, account access, upload, publication or source edit occurred.

Approved facts from `/approved_facts`: CSV preview shipped; certification none. `/source_excerpt` says the cited synthetic page only says CSV preview is shipped. Source support below is checked against this supplied excerpt only; the complete page, ownership, freshness and live accessibility are unverified. All citation strings are `https://example.com/acme-preview`.

## Retained observation ledger

| ID / JSON location | Exact prompt | Supplied date / model / locale | Raw answer | Coding and evidence |
| --- | --- | --- | --- | --- |
| B1 / `/before/answers/0` (prompt 0) | CSV preview tools | 2026-09-10 / provider-A-v1 / en-US | “Acme provides CSV preview.” | Unbranded prompt; Acme mention, no explicit recommendation. One URL. CSV claim agrees with approved fact and supplied source excerpt. |
| B2 / `/before/answers/1` (prompt 1) | CSV migration alternatives | 2026-09-10 / provider-A-v1 / en-US | “Use Beta.” | Unbranded prompt; no Acme mention or citation; explicit Beta recommendation. No Beta feature claim is supplied to validate. |
| A1 / `/after/answers/0` (prompt 0) | Does Acme offer CSV preview? | 2026-10-10 / provider-B-v2 / fr-BE | “Acme provides CSV preview.” | Branded prompt; Acme mention, no explicit recommendation. One URL. CSV claim agrees with approved fact and supplied source excerpt. |
| A2 / `/after/answers/1` (prompt 1) | Is Acme certified? | 2026-10-10 / provider-B-v2 / fr-BE | “Acme is certified secure.” | Branded prompt; Acme mention, no explicit recommendation. One URL, but supplied excerpt does not support certification; claim conflicts with approved certification `none`. |

All four retained texts are nonempty and usable. There are two prompt/answer pairs in each wave, apparently one retained response per prompt. The intended number of runs, repetitions, omitted failures, retries, exclusions, sampling protocol, exact times/timezones, browsing/search mode, provider settings and conversation context are not supplied. No failures or refusals are recorded; this does not prove none occurred. The after prompts and answers remain English despite `fr-BE` metadata.

## Metrics and denominators

Unit: one retained usable answer. Mention and citation metrics are answer-level, not word counts or URL occurrence shares. An explicit recommendation requires wording such as “Use [entity]”; a descriptive mention alone does not qualify. “Any observed URL” means at least one retained citation string, irrespective of ownership or claim support. “Supported entity citation” means at least one citation supporting the answer's Acme assertion according to the supplied excerpt. This is not live verification.

No answers are excluded from the supplied sample. Missing-response policy: never count unknown or failed responses as nonmentions in conditional rates; record them separately in the planned ledger. Here the planned ledger is absent, so usable/planned coverage cannot be calculated. Usable/retained is 2/2 in each wave (4/4 overall), which is only artifact completeness, not planned coverage.

| Conditional metric | Before: unbranded, provider-A-v1, en-US | After: branded, provider-B-v2, fr-BE |
| --- | --- | --- |
| Acme mentions / usable answers | 1/2 = 50% | 2/2 = 100% |
| Explicit Acme recommendations / usable answers | 0/2 = 0% | 0/2 = 0% |
| Any observed URL citation / usable answers | 1/2 = 50% | 2/2 = 100% |
| Supported Acme citation / usable answers, excerpt basis | 1/2 = 50% | 1/2 = 50% |
| Supported Acme citation / answers containing URLs | 1/1 = 100% | 1/2 = 50% |
| Acme factual error / usable answers, approved-fact basis | 0/2 = 0% | 1/2 = 50% |
| Beta mentions and explicit recommendations / usable answers | 1/2 = 50% each | 0/2 = 0% each |

Citation occurrences are 1 before and 2 after; each wave has one distinct URL string. Ownership is unspecified, so an Acme-owned-domain citation rate is **unavailable**, not 50% or 100%. No share-of-voice or sentiment score is claimed: the comparison set, sampling frame and sentiment rubric were not established. No pooled branded/unbranded headline rate is useful here.

The arithmetic mention and URL-rate differences are each +50 percentage points across these different cohorts. They are not matched changes. Supported citation rates remain 50% of usable answers in each cohort; this too is only a descriptive comparison. All four observations are unmatched. The before wave is the sole supplied unbranded sample; the after wave provides no unbranded discovery estimate, while the before wave provides no branded fact-check baseline. Two observations per wave and one response per prompt cannot characterize variability, stable placement or market-wide visibility.

## Findings and supported priorities

1. **Certification accuracy needs attention.** A2's “Acme is certified secure” contradicts `/approved_facts/certification: none`. Its preview citation fails support for that assertion. First verify that public certification/security copy consistently reflects the approved fact and offers a clear primary source. If a public source asserts a certification, correct it through the source owner's normal process. This review has no public-source inventory and establishes no existing content defect or cause; none was edited.
2. **CSV preview representation agrees with supplied facts.** B1 and A1 describe the shipped feature correctly, and the supplied excerpt supports it. Preserve clear, primary feature documentation and ensure factual consistency during the next authorized source review. The observations do not establish source freshness, indexing or crawl eligibility.
3. **Repair the measurement design before judging the update.** Lock prompts and settings, retain all attempts and repeat both branded and unbranded cohorts. The prompt redesign is itself enough to prevent a controlled comparison. A newer measurement cannot reconstruct the missing matched historical baseline.

No negative sentiment is established; the certification claim is an accuracy problem despite its favorable wording. Beta appears as a recommendation once, which does not establish a competitive trend. There is no evidence that the update, a file, schema or wording choice caused any answer or would guarantee citation. Search inclusion, citation, training and crawler permission remain distinct and untested. Current provider access documentation was not checked because this task is offline; no platform-specific eligibility rule is asserted.

## Next measurement plan

- Confirm audience, approved aliases, actual named providers, target locale/language, query intents, comparison set and access authority. Keep private project data out of external tests. Resolve certification facts with the owner before designing any public-source changes.
- Freeze a four-prompt panel using stable IDs: U1 “CSV preview tools”, U2 “CSV migration alternatives”, B1 “Does Acme offer CSV preview?”, B2 “Is Acme certified?”. Analyze U and B separately. If changing prompt language for fr-BE, create a separate documented panel rather than silently replacing English prompts.
- As a bounded prospective design, collect three fresh-session repetitions per prompt per fixed provider/model/locale/settings cell in each of two dated windows: 12 planned observations per window per cell, 24 across both windows. Three repetitions are a practical initial variability check, not a claim of statistical sufficiency. If comparing two providers or locales, stratify them and multiply the planned ledger accordingly. Do not relabel a model change as the same cell.
- Before collection, record planned run IDs, exact prompts, timestamps/timezones, provider/model identifiers as exposed, locale, session context, browsing/search mode and relevant generation settings. Predeclare retries; retain failed/refused/empty attempts and retry links. Capture raw answers and URLs with hashes and privacy limits. Use only authorized tooling; accounts, paid queries or uploads need their own scoped authority and are not part of this review.
- Apply the same mention/recommendation rule; separately count URL presence, verified ownership, claim support and factual errors. Check support from an authorized retained source snapshot or authorized retrieval, recording retrieval date and primary evidence. Report conditional usable-answer metrics alongside usable/planned coverage and all missing reasons. Do not infer an owned domain from a URL path.
- Check current official documentation for each actual platform before a future online crawl/access assessment. Hold provider/model, locale, prompt, search mode and settings constant within matched comparisons, show unmatched cells separately, and retain the cohort breakdown. Record content-update dates and other concurrent changes. Even a stable repeated panel remains observational unless a suitable controlled design supports causal inference.

This deliverable is a supplied-evidence review and future measurement plan. Live discovery, historical response completeness, public-source consistency, citation ownership and current provider behavior remain unverified.
