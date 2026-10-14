# Future domain candidates

Existing roles/skills cover engineering, design, security review, content/SEO/GEO,
financial validation, crypto research and event forecasting. See the
[current role catalog](CATALOG.md) and [skill mapping](SKILLS.md) before adding entries.
The candidates below are unimplemented; they are not market-demand measurements.
Design reference extraction is now covered by [design-analyst](DESIGN-EXTRACTION.md)
and the design-extraction skill. Capability depth still depends on available tools.

## Next procedure gaps

Assessed 2026-10-14 against current skill/role instructions. Priority reflects
missing repeatable methods and evidence, not quantified market demand. Start with
the work the user actually needs; native work can wait when no native app is planned.

| Priority / area | Proposed procedure | Existing owner | First meaningful fixture |
| --- | --- | --- | --- |
| 1 / apps | Native iOS/Android implementation, lifecycle, offline state, permissions, deep links and device/distribution verification | feature-developer; quality, accessibility and release reviewers | Interrupted offline flow and state restoration, with simulator versus device evidence |
| 1 / analytics | Tracking plans, event/property contracts, identity/deduplication and payload QA; reproducible funnels/cohorts | data-analyst defines measurement; feature-developer implements; quality-engineer verifies | Duplicate events, anonymous-to-known identity, missing properties and incorrect conversion denominators |
| 1 / competition watch | Approved watchlist, dated baseline, normalized material diff, freshness and repeat-run handoff | researcher, with evidence-validator and product/marketing interpretation | Real price/feature change, cosmetic churn and an unavailable page that does not prove removal |
| 2 / discovery | Participant-study planning, recruitment/consent, interviews, coding and synthesis artifacts | user-researcher | Contradictory synthetic transcripts with negative evidence; no invented participants |
| 2 / experiments | Assignment/exposure units, primary metrics, guardrails, stopping policy and trustworthy readout | scientist and data-analyst | Apparently positive result invalidated by assignment or exposure defects |
| 2 / market research | Segment/demand validation, buyer versus user, willingness-to-pay evidence and bottom-up market ranges | researcher; product, marketing and GTM interpret | Incompatible definitions and overlapping segments that cannot be summed |
| 2 / web and engineering | Deeper browser/visual regression and reliability evidence under existing test/performance/release procedures | quality-engineer, performance-engineer, feature-developer | Viewport/theme/locale/state changes, flaky visual baselines and a recovery scenario |

Existing web implementation, API/data design, debugging, testing, security, release,
design and research owners already cover the broad responsibility labels. These
are procedure/evidence gaps, not a reason to duplicate generic frontend, backend,
UI/UX, analyst or research profiles. Competitor monitoring can start as a repeat-run
reference under competitive-research; create a separate skill if its workflow grows.
A cadence needs a real authorized scheduler; these profiles do not supply one.
Analytics recommendations do not authorize tracking in a project that excludes it.

Primary method references: [Android app quality](https://developer.android.com/develop/adaptive-apps/quality-guidelines/core-app-quality),
[Apple distribution](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases/),
[Amplitude tracking plans](https://amplitude.com/docs/data/data-planning-playbook),
[GitHub release sources](https://docs.github.com/en/rest/releases/releases),
[GOV.UK research planning](https://www.gov.uk/service-manual/user-research/plan-user-research-for-your-service),
[Microsoft experiment assignment checks](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/)
and [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots).
These establish concrete methods, not demand, adoption or verified expertise.

## Other domain candidates

| Candidate workflow | Starting responsibility | Required artifact/evidence |
| --- | --- | --- |
| AI-agent security | security-auditor | Tool/data trust boundaries, prompt-injection paths, permission and exfiltration controls, isolated adversarial fixture |
| Cryptography review | security-auditor; add a distinct engineer only for recurring protocol work | Versioned protocol/library and key/nonce lifecycle, official test vectors, dated standards |
| Hardware/PCB | A distinct electronics/embedded owner when work recurs | Schematic/BOM, datasheets, units/tolerances, ERC/DRC and bench/manufacturing status |
| Movies/series | A story/editorial owner when work recurs | Story canon, continuity, episode dependencies, script/timeline formats and media rights |
| Robotics/aviation simulation | A specialist engineering owner with a real toolchain | Units/reference frames, model envelope, traceable requirements, simulation/physical-test distinction |
| Learning content | Existing research/content roles initially | Learner prerequisites, measurable objectives, worked solutions and assessment rubric |

Start with a repeatable procedure under an existing role when responsibility is
already covered. Add a role for a distinct recurring responsibility, not a title
alone. Choose real sample artifacts and a meaningful independent check before
claiming usable coverage. High-consequence engineering requires explicit limits
and appropriate expert review; simulation does not establish operational clearance.

Useful primary starting points include [KiCad CLI](https://docs.kicad.org/9.0/en/cli/cli.html),
[NIST post-quantum work](https://csrc.nist.gov/projects/post-quantum-cryptography),
[OpenVSP](https://openvsp.org/) and [PX4 simulation](https://docs.px4.io/main/en/simulation/).
These establish available tooling/standards, not demand for this collection.
Use [documentation standards](DOCUMENTATION.md) and [observed evaluations](../evals/README.md)
to decide whether a candidate is ready to add.
