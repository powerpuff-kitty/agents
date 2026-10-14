# Contributing

Edit portable sources in `agents/`, `teams/`, `packs/` and `shared/`; host-specific
formatting belongs in `adapters/`. Generated `dist/` outputs are ignored. Read
[AGENTS.md](AGENTS.md) and the [architecture contract](docs/ARCHITECTURE.md) before
changing source ownership, renderer behavior or installation.

Use an existing role for a new task method when its responsibility already fits.
Reusable procedures belong in the separate [skills source](https://github.com/powerpuff-kitty/ai-skills).
See [role-to-skill guidance](docs/SKILLS.md). A new role needs a distinct ongoing
responsibility, narrow metadata, 1 owning pack and 2 observable acceptance
specifications. A new team must preserve dependency order, scoped authorization
and exclusive writers. Update current catalog/pack/team documentation alongside
accepted changes; retained raw evaluation records keep their original scope.

Run the exact source/build/test commands in [AGENTS.md](AGENTS.md). Tests use
isolated synthetic destinations. Do not install into personal host configuration
or run model sessions as part of ordinary source checks. Host loading requires
an explicitly selected executable and isolated installation scope; behavioral
claims require retained observed sessions. The normal CI workflow performs no
model calls, publication or deployment.

The repository owner reviews source and compatibility changes; there is no implied
multi-maintainer approval process. Keep PRs focused, explain meaningful changed
behavior and link actual validation. Report defects with the affected revision,
minimal non-sensitive reproduction and observed versus expected result. Avoid
public issue attachments containing credentials, private transcripts or project
data. Authored profiles/tooling use the root MIT [LICENSE](LICENSE); retain notices
when redistributing substantial copies and preserve third-party terms.
