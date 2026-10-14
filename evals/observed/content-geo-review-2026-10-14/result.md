# Offline editorial and GEO deliverables

This is one synthetic supplied-evidence exercise, not evidence of general behavioral coverage. No network, accounts, publication, or source-repository edits were used. The sole product authority is the complete supplied approved source, revision **launch-7**. Observation excerpts and source descriptions are supplied fixture evidence, not live checks. The measurement date, exact prompts, provider identity, locale, and raw response metadata were not supplied and are not invented.

## Editorial brief

**Assignment:** Update the existing migration article with a useful preparation and verification section. Working title: “Preparing your CSV migration: what to check before and after preview.” The existing article already explains CSV preview, so do not commission a second article repeating that intent. The existing article's full text was not supplied; the editor must compare the proposed delta against it before finalizing sections.

**Audience and problem:** People preparing to move spreadsheet data into Acme who need to understand prerequisites, inspect data, and know what remains outside the product's shipped scope. This audience is an editorial assumption from the migration assignment. Channel: English web help/editorial article; locale unspecified. Use clear, practical, nonpromissory language. Suggested scope: a focused addition of approximately 500–800 words, adjusted to avoid duplication after reviewing the existing article.

**Goal and reader action:** Help readers decide whether their migration is ready to preview and identify unresolved requirements. Direct readers to the existing preview instructions once their preparation checks are complete. Do not prescribe undocumented buttons, field names, schemas, or import/recovery behavior.

**Angle and boundaries:** Give readers a readiness checklist and a way to interpret a preview. Link to or reuse existing preview guidance. Accounting sync is not shipped; migration must not be framed as an accounting integration. Security certification has not been obtained. Avoid speed guarantees, unsupported performance comparisons, customer stories, and invented search demand. Search intent hypothesis: practical CSV migration preparation. No keyword-volume dataset, search results, market, or dated external research is available; this is a utility-led editorial assignment, not a validated search-demand finding or ranking forecast.

### Claim/source ledger

| Claim or proposed material | Authority/status | Writer instruction |
| --- | --- | --- |
| CSV preview is shipped | launch-7, approved | May assert availability; use existing article for verified instructions once reviewed. |
| September pilot: 12 users; 8 completed onboarding within one day | launch-7, approved | If included, retain month, pilot population, denominator, and one-day timeframe. Year unspecified. |
| Pilot has no control group | launch-7, approved | Include with any pilot result; no causal or population-wide inference. |
| Accounting sync is not shipped | launch-7, approved | Explicit scope limit where integration expectations matter. |
| No security certification has been obtained | launch-7, approved | Do not claim certified security; absence of certification is not proof that the product is insecure. |
| Required columns, accepted encodings/types, size limits, validation rules | Not supplied | Product/documentation owner must provide versioned requirements before exact advice is written. |
| Preview fields, handling invalid rows, correction/retry, post-import verification | Not supplied | Obtain documentation and a verified example; do not invent interface steps or successful recovery. |
| Existing preview article content beyond its stated subject | Not supplied | Editor must review the full article and reuse its established terminology and links. |
| Search demand, ranking, comparative speed, testimonials | No evidence | Omit; do not fill the gaps with invented figures or quotations. |

### Outline and evidence assignments

| Section | Reader question and purpose | Required evidence |
| --- | --- | --- |
| Short scope statement | Is this the right guide for my CSV migration? Set expectations without a speed promise. | launch-7; existing article once supplied. |
| Before preview: preparation checklist | What should I check in my source data? Make readiness actionable. | Versioned schema, supported formats/limits, approved example CSV. Research gap until supplied. |
| Preview handoff | Where do I inspect the proposed mapping/data? Avoid repeating existing coverage. | Reviewed existing preview instructions and stable article anchor/link. |
| Interpret and resolve a mismatch | What should I do if something looks wrong? Explain a documented correction path. | Product-approved mismatch example and verified recovery procedure. Pending evidence; do not prescribe exact behavior yet. |
| Verify completion and know the boundaries | How will I know my migration is complete, and what is not included? | Product-approved success criteria; launch-7 for accounting-sync limitation. |
| Optional evidence note | What does the pilot tell me? Provide context only if relevant to this help article. | Exact launch-7 counts and no-control-group limitation. It does not establish expected speed or causality. |

**Counterarguments and limits:** A preview is a useful inspection point but does not, on supplied evidence, establish that the entire migration is correct or complete. A reader seeking accounting synchronization has a requirement outside the shipped scope. Users with unsupported file formats or unknown schema requirements need verified documentation before proceeding.

**Format/accessibility:** Use descriptive headings and a short checklist; explain CSV terminology once. Use real, approved sample data rather than private customer data. Any screenshot must have meaningful alternative text and matching text instructions. No screenshot or visual is needed for this brief.

**Observable acceptance criteria:** The final article reuses existing preview coverage and adds a clearly identified preparation/verification delta; every product-specific step and field matches the named documented version; any error example includes a verified recovery; every material fact traces to the ledger; any pilot statement retains its scope and limitations; no unsupported integration, certification, outcome, customer endorsement, or demand claim remains. The actual article, product schema, recovery instructions, and working links remain inputs for the writer/editor, not completed checks in this offline brief.

## Edited draft

> Acme ships CSV preview. In the September pilot, 8 of 12 users completed onboarding within one day. The sample had no control group, so these results do not establish a guaranteed outcome for other users. Accounting sync is not shipped, and no security certification has been obtained.

This is a substantive factual correction for a general product audience, using a plain, informative voice. It preserves the draft's purpose of describing onboarding and product availability while replacing claims contradicted by launch-7. “Instant” became “within one day”; “every customer base” became the specific 12-user pilot; the guarantee was removed; certified-security and live-accounting-sync claims were corrected. Eight of 12 is two-thirds of this pilot, not evidence about all customers or an effect caused by the product. No testimonial was supplied or invented. No author decision is required to resolve these facts because launch-7 is designated approved authority. Any different product positioning needs new approved evidence.

## Repurposed drafts

Authoritative source: complete supplied launch-7 excerpt. Adaptation is authorized for this exercise; broader rights, publication permission, dates/year, and distribution lists were not supplied. The drafts require no image, audio, or inaccessible visual dependency. Internal provenance below is not a substitute for a public source URL; no approved public report link was supplied.

**Newsletter paragraph:**

Acme's CSV preview is shipped, giving readers a concrete feature to explore as they plan a migration. In the September pilot, 8 of 12 users completed onboarding within one day. With no control group, this small sample does not establish that Acme caused that outcome or guarantee results for other users. Accounting sync is not shipped, and no security certification has been obtained. Before planning your migration, identify your CSV requirements and review the existing preview guidance.

**Social draft — 165 characters, including spaces and punctuation:**

September pilot: 8 of 12 Acme users completed onboarding within one day. No control group; results do not guarantee outcomes for other users. CSV preview is shipped.

| Asset | Reader purpose/action | Source mapping | Added material and limits |
| --- | --- | --- | --- |
| Newsletter | Give migration planners context and direct them toward requirements and existing guidance | launch-7 feature availability, pilot counts/timeframe/control limitation, sync and certification status | Migration-planning framing and suggested reader action are editorial guidance, not new observed product behavior. No link invented. |
| Social | Share one accurately scoped pilot observation alongside shipped feature status | launch-7 pilot month/counts/timeframe/control limitation and preview availability | No added empirical claim, quote, or endorsement. Sync/certification claims are omitted rather than compressed into unsupported promises. |

The social count uses Python 3 `len()` on the exact ASCII draft, excluding the surrounding heading and blank lines. No link is included; adding a link requires recounting and any platform-specific length check. A report link could accompany the newsletter or social when an approved URL exists; it was not fetched or fabricated here. Platform-specific display and publication checks were not performed.

## GEO supplied-observation report

**Scope:** Acme; case-insensitive exact name “Acme” is the only supplied entity alias. Count each answer at most once for each metric, regardless of repetition. A mention is brand text; a recommendation requires explicit advice to choose/consider Acme. A1's feature description and A2's assertion are not coded as explicit recommendations. This is an unbranded synthetic panel, six planned observations, supplied as using the same settings/version. Intended audience and locale, exact prompts, dates/times, provider/model identifiers, and search mode are absent. Those omissions prevent exact reproduction today.

**Missing policy:** A5 provider error and A6 refusal contain no answer and remain in the planned ledger. They are excluded from usable-answer rates, not silently removed from the planned sample and not coded as evidence of nonmention. Coverage reports them explicitly. URL support is assessed only against supplied excerpts and launch-7, not by opening the synthetic URLs.

| ID | Retained supplied answer/status | Acme mention | Explicit Acme recommendation | Citation and support |
| --- | --- | --- | --- | --- |
| A1 | “Acme offers CSV preview.” Usable answer | Yes | No | https://example.invalid/acme-preview — Acme-owned per fixture; supplied excerpt supports CSV preview; consistent with launch-7. |
| A2 | “Acme is certified secure.” Usable answer | Yes | No | https://example.invalid/acme-preview — Acme-owned per fixture; excerpt only describes preview and does not support certification; claim conflicts with launch-7. |
| A3 | “Consider Beta.” Usable answer | No | No | No citation. Explicit recommendation of Beta. |
| A4 | “Try Gamma.” Usable answer | No | No | No citation. Explicit recommendation of Gamma. |
| A5 | Provider error; no answer | Unavailable | Unavailable | No answer to assess; excluded from usable denominator. |
| A6 | Refusal; no answer | Unavailable | Unavailable | No answer to assess; excluded from usable denominator. |

**Metrics (answer-level, this unbranded cohort only):**

| Metric | Numerator / denominator | Result |
| --- | --- | --- |
| Coverage | 4 usable / 6 planned | 66.7% |
| Missing responses | 2 / 6 planned: one error and one refusal | 33.3% |
| Acme mention rate among usable answers | A1 + A2 = 2 / 4 | 50% |
| Any observed URL citation among usable answers | A1 + A2 = 2 / 4 | 50% |
| Acme-owned-domain citation rate among usable answers | A1 + A2 = 2 / 4 | 50% |
| Supporting citation about Acme among usable answers | A1 only = 1 / 4 | 25% |
| Explicit Acme recommendation rate among usable answers | 0 / 4 | 0% |
| Support verification among citation-bearing answers | A1 only = 1 / 2 | 50% |

A2 remains an observed owned-domain URL citation even though its associated claim is unsupported. Ownership, occurrence, claim support, and factual accuracy are distinct measures. The same cited URL appearing in two answers counts as two citation-bearing answers; this is not a count of unique sources. A planned-sample mention yield would be 2/6 = 33.3%, but that is a different metric from the 2/4 conditional answer rate and does not imply the missing answers contained no mention.

**Factual representation:** A1 accurately describes the shipped preview feature. A2's “certified secure” conflicts with the approved fact “No security certification has been obtained.” Its cited preview excerpt provides no certification evidence. Among the two usable answers mentioning Acme, one is consistent and one contains a material factual error; this tiny set is not a general accuracy estimate. A3/A4 provide no Acme claim to verify. Absence of certification should not be restated as proof of unsafe security. These observations establish neither overall brand sentiment nor a market-wide share of visibility.

**Repeat plan:** Retain this input and its hash as the authorized evidence artifact; observation IDs A1–A6 map to it. Obtain and record the exact prompt panel with stable prompt IDs, provider/model version, locale, browsing/search settings, run timestamps and repetition count before repeating. Preserve the unbranded cohort separately from any later branded prompts. Predeclare the same entity, recommendation, citation, support rules, denominator policy, sample size, and retry policy; retain original errors/refusals and any retries as separately identified attempts. Repeat each matched prompt/provider/settings cell at a stated later window; save the authorized full responses and cited source excerpts with IDs/hashes and capture dates. Verify claim support again, retaining changed-source evidence. Compare counts, denominators, and cell-level differences, and report unmatched or missing cells separately. Repeated responses from one provider can be correlated, so this small panel cannot estimate the whole AI market.

**Second batch and causality:** Different prompts and a different model version form a different cohort. They cannot prove that the website edit caused an improvement, and pooling them with this panel would confound prompt/model effects with content effects. Report that batch separately. A stable matched repeat could describe observed differences, but before/after evidence alone still cannot isolate the edit's effect. A causal study would require a suitable controlled design and accounting for model, retrieval, time, and other concurrent changes; none is supplied. The unsupported certification statement is an observed representation gap. Clear source wording is a possible improvement hypothesis, not proof that a source edit will remove it or guarantee citation.

## Checks, limitations, and source provenance

Completed checks: read the full input and all four requested skills; read each skill's linked local template, content examples, and GEO method; compared all product and pilot statements against launch-7; calculated answer-level metrics from the six supplied observations; counted the exact social draft with Python 3; retained file hashes below. No expected acceptance tests were read. No live link, keyword, provider, browser, build, production, publication, or external research check was performed. The brief's product-specific research gaps remain explicit commissioning inputs.

Commands used: `cat` to read only the input and listed skill resources; Python 3 to count the draft; a shell heredoc to write this result; Python 3 for hash retention and final artifact checks. Writes were confined to this temporary result path. The source list below is exhaustive for content used in this run. Hashes identify the exact bytes used; they do not validate the truth of the fixture.

### Source SHA-256 manifest

- `1444d02d2f76f6516f3b7b62b4edc8be44e0619468a71d0ac23024d8111d4cc7` — `/private/tmp/content-geo-forward/input.md`

- `abd6617858000ad47480a2bc2cb84d976c349c57923610c428221b7deb3d4e44` — `/Users/tcsntcsn/TCSN/skills/content-brief/SKILL.md`

- `51540a69c6218b547ea903cf42aca570e4e416296bf5dd2c7f53297100cc1813` — `/Users/tcsntcsn/TCSN/skills/copy-editing/SKILL.md`

- `3a1f8d3649d7e54505b24cb56ef81c0c1deaa90b24b735dfb0c7781fabb4f196` — `/Users/tcsntcsn/TCSN/skills/content-repurposing/SKILL.md`

- `58bd8f1502d26482e986ca828c537e6ff9643a74b90e434d2f1b31da531016b3` — `/Users/tcsntcsn/TCSN/skills/geo-measurement/SKILL.md`

- `3dfa5eb7af19685b98ee88a71492d2ece371d7f42d850a55e96fd673adf9adf6` — `/Users/tcsntcsn/TCSN/skills/content-brief/assets/brief-template.md`

- `0d8c3430c191f550080445d87bb72b08caf1df7766101632ff2370d348072c0d` — `/Users/tcsntcsn/TCSN/skills/content-brief/references/example.md`

- `88f85923d9f1add4c3f43c306e0149c555094b787bbec7c542a6eb2da11abb82` — `/Users/tcsntcsn/TCSN/skills/copy-editing/assets/review-template.md`

- `43806b8e040d36ba56f14b6062cbebdc5416100d88dfda6f9b79be572bf6280c` — `/Users/tcsntcsn/TCSN/skills/copy-editing/references/example.md`

- `ee19576f1b0f63476b542328400f31dbe42fd1c1df553a2f7e949616a315832f` — `/Users/tcsntcsn/TCSN/skills/content-repurposing/assets/output-map.md`

- `d02f4afa5cc9a124baa7fc98785a54e9ed4841d28da1650a1ae72ade705eb5d6` — `/Users/tcsntcsn/TCSN/skills/content-repurposing/references/example.md`

- `8973e36f3e18658334daa6b9c34e625ccb4b0aefb7581f27ba210e0a73bd9e42` — `/Users/tcsntcsn/TCSN/skills/geo-measurement/assets/report-template.md`

- `455a245a66e2333d1a72dacb21de6a4558d6f282b2149d2d25c4c7922cec95e9` — `/Users/tcsntcsn/TCSN/skills/geo-measurement/references/method.md`
