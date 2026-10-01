# Contributing

Use the stable `effect@4.0.0` package and its pinned
[source policy](docs/version-policy.md) when changing an example. Compare
both the installed export map and declarations before naming a symbol;
`main` may contain unreleased import paths. Keep any added `@effect/*`
integrations on the same exact `4.0.0` version in `package.json` and the
lockfile.

## Skill design

One skill should answer one development decision. A frontmatter description
must say which task triggers it, not enumerate an entire package. Explain
the neighboring module's responsibility, where data/errors/resources pass
between them, the v3/v4 gate, and any unstable API boundary. Link to a
specific API page and to source at the release tag. Keep the skill usable
when it alone is installed: local references must remain inside its folder.

Every skill contains at least one standalone `ts` or `tsx` example. All such
fences are independently typechecked against the pinned stable release; avoid
fragment-only imports or implicit context from a previous fence. Call a snippet
"typechecked" unless a runtime test actually exercises it. Add a scoped
integration test for cross-module behavior rather than implying that a type
check proves network, persistence, or cleanup behavior.

## Checks

```sh
devenv shell -- npm ci
devenv shell -- npm test
devenv shell -- python3 scripts/validate-skills.py --external
```

`npm test` runs packaging and local-link validation, compiles every skill
example, and exercises the real HTTP/SQL example. The external check follows
official documentation and pinned-source links and needs network access.
Run the [Agent Skills reference validator](https://agentskills.io/specification.md)
against each skill when available. The pinned `skills` CLI is exercised in
disposable projects by the repository test:

```sh
devenv shell -- npm run check:install
```

The check covers discovery, single- and multiple-skill installation, and
installed local references without touching the developer's agent setup.
