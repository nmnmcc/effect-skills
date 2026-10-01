# Effect Skills

Independently installable [Agent Skills](https://agentskills.io/specification) for
Effect developers. Each skill is organized around a development decision: when
to choose a module, what the neighboring modules own, and where errors and
resources cross the boundary. This is a community repository, not an official
Effect release.

## Version

The code targets the stable **`effect@4.0.0`** release at upstream commit
`67ba4e46a11ccda0b6761578bfd22c04ae00167d`. Its `@effect/*` integrations are
pinned to the same version. Effect v4 is now the npm `latest` line; do not
apply these imports to a v3 project without an explicit migration. See the
[version and source policy](docs/version-policy.md) for published export paths,
stability annotations, and compatibility limits.

## Install the skills you need

With Node.js and npm, discover and install individual skills from GitHub:

```sh
npx skills add nmnmcc/effect-skills --list
npx skills add nmnmcc/effect-skills --skill effect-core --agent codex -y
npx skills add nmnmcc/effect-skills --skill effect-schema --skill effect-http-api --agent codex -y
```

From a checkout, substitute `.` for `nmnmcc/effect-skills`. The installer
places only the selected skill directories in the agent's project; a skill's
instructions and references remain usable without installing its neighbors.
Installing a skill does **not** install Effect into the consuming application.
Pin that application's `effect` and any `@effect/*` packages separately.

## Choose a skill

| Task | Skill |
| --- | --- |
| Execution and typed failures | [effect-core](skills/effect-core/SKILL.md) |
| Service graphs and resource lifetime | [effect-services](skills/effect-services/SKILL.md) |
| Fibers, queues, and coordination | [effect-concurrency](skills/effect-concurrency/SKILL.md) |
| Atomic in-process state | [effect-state](skills/effect-state/SKILL.md) |
| Incremental streams and backpressure | [effect-streams](skills/effect-streams/SKILL.md) |
| Retries, scheduling, and clocks | [effect-time](skills/effect-time/SKILL.md) |
| Pure data, absence, and collections | [effect-data](skills/effect-data/SKILL.md) |
| Boundary validation and codecs | [effect-schema](skills/effect-schema/SKILL.md) |
| Deployment configuration | [effect-config](skills/effect-config/SKILL.md) |
| Text, bytes, and wire formats | [effect-encoding](skills/effect-encoding/SKILL.md) |
| Node/browser adapters and platform I/O | [effect-platform](skills/effect-platform/SKILL.md) |
| HTTP transport and clients | [effect-http](skills/effect-http/SKILL.md) |
| Schema-defined HTTP endpoints | [effect-http-api](skills/effect-http-api/SKILL.md) |
| Remote procedure protocols | [effect-rpc](skills/effect-rpc/SKILL.md) |
| Relational persistence and transactions | [effect-sql](skills/effect-sql/SKILL.md) |
| Key-value stores, persisted queues, and caches | [effect-persistence](skills/effect-persistence/SKILL.md) |
| Restart-surviving executions | [effect-workflow](skills/effect-workflow/SKILL.md) |
| Sharded entity ownership | [effect-cluster](skills/effect-cluster/SKILL.md) |
| Event journals and replay | [effect-eventlog](skills/effect-eventlog/SKILL.md) |
| Logs, metrics, and tracing | [effect-observability](skills/effect-observability/SKILL.md) |
| Typed command-line programs | [effect-cli](skills/effect-cli/SKILL.md) |
| AI models, tools, and providers | [effect-ai](skills/effect-ai/SKILL.md) |
| Deterministic Effect tests | [effect-testing](skills/effect-testing/SKILL.md) |
| UI atoms and bindings | [effect-reactivity](skills/effect-reactivity/SKILL.md) |

The [category and composition index](docs/category-map.md) shows which skills
to combine for HTTP APIs, validation, service dependencies, and persistence.
A [complete user API example](examples/user-api.ts) connects Schema,
HttpApi, Context/Layer, a Node HTTP server, and file-backed PGlite. Its
[integration test](examples/user-api.test.ts) exercises actual HTTP requests
and a database restart.

## Verify the repository

The included [devenv](https://devenv.sh/) shell supplies Node.js 22, npm,
Python, PyYAML, and a Markdown parser. After installing devenv:

```sh
devenv shell -- npm ci
devenv shell -- npm test
devenv shell -- python3 scripts/validate-skills.py --external
```

`npm test` validates packaging and local references, typechecks **every**
TypeScript code fence in the skills against the pinned release, runs the
HTTP/database integration test, and checks isolated single/multiple installs.
`--external` fetches the linked official
sources and API pages; it requires network access. See [CONTRIBUTING.md](CONTRIBUTING.md)
for update and independent-install checks.

Licensed under [MIT](LICENSE).
