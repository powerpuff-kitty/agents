# Future domain candidates

Existing roles/skills cover engineering, design, security review, content/SEO/GEO,
financial validation, crypto research and event forecasting. See the
[current role catalog](CATALOG.md) and [skill mapping](SKILLS.md) before adding entries.
The candidates below are unimplemented; they are not market-demand measurements.
Design reference extraction is now covered by [design-analyst](DESIGN-EXTRACTION.md)
and the design-extraction skill. Capability depth still depends on available tools.

## Implemented product methods

The 2026-10-14 procedure assessment is implemented in 7 focused skills plus
extensions to testing and performance methods. [Product methods](PRODUCT-METHODS.md)
maps them to existing owners and defines their evidence limits. Browser/device,
participant, production analytics and scheduled-watch execution still require the
actual project, tools, data and authorization. The offline fixtures establish
bounded method behavior, not production coverage or quantified market demand.

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
