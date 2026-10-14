# Synthetic product funnel readout

One of three fully observed entrants converted within 48 hours: **33.33%**. One additional entrant has only 24 hours of observation and is reported as immature, not a failure. This describes the supplied mature synthetic cohort; it is not a population estimate or a causal effect.

Question: among observed signup entrants with a full 48-hour follow-up, how many created a project in order within that window? Data revision is the exact retained input hash in `source-manifest.json`. Unit is the supplied `unit_id` user; no identity stitching. Cutoff is 2026-10-08 00:00 UTC, occurrence-time analysis. Data range is 2026-10-01 through 2026-10-07; ingestion timestamps and collection coverage are unknown.

The analysis rule is set explicitly: earliest observed signup per unit; exclude outcomes without observed entry; deduplicate exact `event_id`; reject conflicting payloads; include event timestamps through the cutoff; conversion occurs at or after entry and at or before entry + 48 hours. Endpoint inclusivity is a declared analytic convention. No additional bot/test filters are applied: the whole dataset is synthetic and no traffic classifications are supplied. No record is post-cutoff. No alternative identity map is inferred.

| Metric | Eligibility / entry | Order / window | Numerator | Denominator | Censoring |
| --- | --- | --- | --- | --- | --- |
| Mature 48-hour signup-to-project conversion | Earliest observed signup, full follow-up | Signup ≤ creation ≤ signup + 48h | 1 user | 3 users | 1 immature entrant excluded and separately counted |
| Observed all-entrant fraction, incomplete | All 4 observed entrants | Same event rule, cutoff-limited observation | 1 user | 4 users | 25%; not a finalized 48-hour rate |

| Unit | Entry / follow-up | Outcome evidence | Classification |
| --- | --- | --- | --- |
| A | Oct 1 00:00 UTC; mature | Project at +24h, duplicate event replay removed | Converted |
| B | Oct 1 00:00 UTC; mature | Project at +72h | Not converted within 48h |
| C | Oct 1 00:00 UTC; mature | No observed project | No observed in-window conversion |
| D | Oct 7 00:00 UTC; 24h observed | No observed project; window ends Oct 9 | Immature; finalized outcome unknown |
| E | No observed signup | Project event only | Excluded nonentrant; no fabricated entry |

Raw 8 rows → 8 structurally valid rows → 7 unique events (one repeated `a2`) → 5 distinct users → 4 eligible entrants + 1 excluded nonentrant → 3 mature + 1 immature entrant → 1 mature in-window converter. Four unique signup events and three unique project events reconcile to the seven deduplicated events. The pipeline does not equate three project events with three funnel conversions.

Sensitivity: counting the immature user as a failure changes the displayed fraction to 1/4 = 25% and changes the denominator. Its final 48-hour outcome is unobserved. Conditional on complete supplied historical recording and only this one unresolved entrant, the eventual finalized rate among these four entrants lies between 1/4 and 2/4 (25%–50%). This range is a logical censoring bound, not a confidence interval. Removing the 48-hour restriction would count B and produce 2/3 among mature entrants, answering a different question with different follow-up. Inclusive/exclusive boundary choice does not affect this fixture because no outcome is at 0h or 48h. No repeated signup episodes exist, so alternative repeated-entry definitions cannot be meaningfully evaluated here.

No statistical population interval is given for this tiny deliberately synthetic, nonrandom dataset. No segments or acquisition attribution are supplied; inventing them would misstate the data. No retention or revenue metric is supported. Differences can arise from incomplete recording, late arrival, identity resets or cohort mix as well as behavior; this fixture cannot distinguish them. Absence of a project event is only absence in the supplied snapshot.

Recommended action: preserve D's censoring label and obtain its full window plus ingestion/coverage metadata before finalizing the all-entrant rate. Confirm entry/identity completeness and orphan E before using the funnel operationally. No collection or warehouse change was made.

`calculate.py` and `analytics-calculations.json` retain exact transformations and the per-unit ledger. Local duplicate, timestamp/order, denominator and boundary checks ran successfully. Missing layers: real emission/transport/warehouse reconciliation, ingestion lateness/backfill, bot/traffic classification, source completeness, approved identity lifecycle, population representativeness and causal identification. These are unavailable, not passed.
