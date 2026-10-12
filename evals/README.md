# Agent behavior acceptance scenarios

The [21 scenarios](behavior-cases.json) define two role-specific cases for each of
nine agents plus three shared cases. They cover review-only scope, authorized fixes,
unavailable checks, existing user edits, project-context discovery, untrusted
instructions, scoring boundaries, release evidence, and unsupported claims.

Every specification is marked `not_run`. Source validation checks scenario shape,
role references, and coverage; it does not execute a model or determine outcomes.
Keep observed results separate from specifications.

For an actual evaluation, prepare an isolated synthetic fixture meeting the stated
requirements, retain initial file hashes, select a fresh authorized session and
the intended profile, and record host/model identity and exact instruction hashes.
Retain actual actions, transcripts, final artifacts, and executed check outputs.
Use only local/stubbed trackers, deployment targets, credentials, and external data.

Review every criterion against observable outcomes, including forbidden actions
and preservation of user work. A plausible answer cannot establish that a test
ran, a file was preserved, or a shared action did not happen. Record pass, fail,
or unverified with evidence paths and reviewer rationale. Preserve failures and
environment limitations; never convert unverified checks into passes.

Do not upload private transcripts or data as part of evaluation. Repeat scenarios
when reliability matters, with setup/model differences recorded. No model runner,
provider, or inference budget is required to use or validate the profile files.
