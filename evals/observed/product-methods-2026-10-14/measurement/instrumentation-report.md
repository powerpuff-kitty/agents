# Synthetic tracking contract and payload QA

The supplied four payloads do not constitute four valid unique signups. Under a local strict allowed-field policy, two rows pass the supplied contract, both share the same exact event ID and contents, and one unique payload remains after deduplication. Two rows fail: row 3 lacks `occurred_at`; row 4 includes the disallowed direct-identifier field `email`. Only its field name is reported here. This finding is offline payload evidence; no collector or business completion was observed.

## Decision, scope and proposed metric

Decision: whether this supplied tracking contract/payload sample is ready to support a count of business-confirmed signups. Product: unspecified synthetic exercise. Owner, collection permission/eligibility, retention and deployed revision are not supplied. Source snapshot is SHA-256 pinned in `source-manifest.json`; the contract declares revision 1.

| Metric and unit | Denominator / window | Trigger | Contract | Allowed / excluded |
| --- | --- | --- | --- | --- |
| Unique qualifying signup event count; event unit | No population denominator supplied; fixture only | Business-confirmed signup, never a button click | `signup_completed`, v1 | Only the contract allowlist; unexpected fields rejected locally |
| Signup conversion rate | Undefined: eligible-attempt denominator and observation window absent | Requires a separately approved attempt contract | Not specified | No new collection implemented |

An event count is not necessarily a unique person count. `anonymous_id` is a pseudonymous identifier in the fixture; its stable unit scope, reset behavior and relationship to business accounts are unprovided.

| Field | Supplied constraint | Proposed local type check | Owner / deployed state |
| --- | --- | --- | --- |
| `event` | Must equal `signup_completed` for this reviewed contract | Expected event equality | Unknown / uninspected |
| `schema_version` | Contract version 1 | Expected revision equality | Unknown / uninspected |
| `event_id` | Required, allowed | Nonempty string; exact duplicate comparison | Unknown / uninspected |
| `occurred_at` | Required, allowed | Nonempty string, parseable timestamp with timezone | Unknown / uninspected |
| `anonymous_id` | Required, allowed | Nonempty string | Unknown / uninspected |

The contract does not formally declare types or optionality for the event/revision keys. The equality and string/timestamp checks above are explicit review assumptions, not a claim that a supplied type schema exists. Required/allowed-key checks follow the actual supplied lists. No payload defaults or enrichment are applied.

## Reconciliation and actual checks

| Payload QA scenario | Actual local evidence | Result / unverified layer |
| --- | --- | --- |
| Complete allowed payload | Rows 1 and 2 contain all required fields, expected event/revision and parseable UTC time | Shape passes; actual business success unverified |
| Retry / duplicate ID | Rows 1 and 2 have identical ID and contents | One replay removed locally; no transport retry observed |
| Missing field | Row 3 lacks `occurred_at` | Rejected locally |
| Extra field | Row 4 contains `email` | Rejected locally; synthetic fixture unchanged |
| Conflicting duplicate | No conflicting duplicate observed | Conflict detector executed; no positive conflict fixture supplied |
| Cancellation / denied or revoked collection | No eligibility/cancellation records or pipeline supplied | Unavailable; do not infer collection permission |
| Identity changes / shared device / logout | No approved identity map or lifecycle records | Unavailable; no joins attempted |
| Clock skew / ingestion ordering | Occurrence strings parse; no ingestion timestamps or trusted clock | Skew/order cannot be assessed |
| Emitted → transport accepted → warehouse accepted | Only static payload rows exist | No actual emission, network, collector or warehouse check |

Raw 4 = 2 shape-passing rows + 2 rejected rows. Shape-passing 2 = 1 accepted unique row + 1 duplicate. There are 3 distinct event IDs in the raw fixture; duplicate and rejected counts are retained separately in `instrumentation-calculations.json`. “Accepted” describes this local validator policy only. It is not delivery acceptance or durable business success. No event-loss estimate is possible without an emitted/accepted ledger.

## Identity, ordering and lifecycle proposals

Within this fixture only, deduplicate by exact `event_id`, keep the first identical payload, flag conflicting content rather than silently merge it. No production deduplication location, retry budget, queue expiry, event ID scope or retention window is known. The local batch is the deduplication window. Preserve occurrence time and any future separately approved ingestion time; do not invent late-arrival/backfill behavior. No exactly-once guarantee is established.

No anonymous-to-known join is authorized or performed. A future contract needs explicit allowed evidence, effective times, merge/split/logout/reset and shared-device semantics. Do not infer a person join from email, device, name or timestamp.

Recommended next action: supply owner, classification/retention, required types, eligibility policy, ingestion time, pipeline guarantees and business-trigger proof before relying on these events. Remove unapproved extra fields at the source; do not treat dashboard filtering as collection protection. For a future breaking change, propose a new version with a documented consumer migration, bounded compatibility period and explicit retirement of v1; additive changes also require an allowlist update. No migration, rollout or rollback was executed. A future source rollback would restore its previously reviewed implementation/configuration and verify payloads again, without deleting raw historical evidence.

Reproduce with `python3 calculate.py` from this output directory. The exact code, raw synthetic input copy, manifest and command output are retained. Original fixture remains recoverable and unchanged. No live instrumentation claim is made.
