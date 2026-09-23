# Effect Skills

Hand-written [Agent Skills](https://agentskills.io/specification) for building
with [Effect](https://github.com/Effect-TS/effect). Each skill covers one
related area and teaches the decisions that matter there: which abstraction
fits, how to compose it, and where errors, resources, and version boundaries
belong. This is an independent repository, not an official Effect release.

The layout follows [Cloudflare's skills repository](https://github.com/cloudflare/skills):
each skill lives in its own skills/<name>/SKILL.md directory and can be
installed separately with the [skills.sh CLI](https://www.skills.sh/docs/cli).

## Development environment

The repository includes a reproducible [devenv](https://devenv.sh/) shell and
[direnv](https://direnv.net/) integration. The shell provides Node.js 22 with
npm/npx, Python 3.12 with PyYAML, Git, and Curl.

After installing Nix, devenv, and direnv:

```sh
# Enable the hook once per shell (Bash example).
eval "$(direnv hook bash)"
direnv allow
devenv test
```

Use the equivalent `direnv hook zsh` or `direnv hook fish` command for other
shells. `devenv shell` remains available when you do not want automatic
Direnv loading.

Without direnv, enter the same environment with `devenv shell`. The
`check:skills` task runs the repository packaging validator.

## Install

From this directory, with Node.js and npm installed:

```sh
npx skills add . --list
npx skills add . --skill effect-core
npx skills add . --skill effect-schema --skill effect-http
```

After publishing this directory to GitHub, replace <owner>/effect-skills below
with the actual repository path:

```sh
npx skills add <owner>/effect-skills --list
npx skills add <owner>/effect-skills --skill effect-core
```

An agent can also select a skill automatically when its description matches
the task. Install only the areas relevant to the project.

## Skills

| Area | Skill | Use for |
| --- | --- | --- |
| Execution | [effect-core](skills/effect-core/SKILL.md) | Lazy effects, typed failures, Causes, runtimes |
| Dependencies | [effect-services](skills/effect-services/SKILL.md) | Context, Layer, Scope, resource ownership |
| Concurrency | [effect-concurrency](skills/effect-concurrency/SKILL.md) | Fibers, queues, pub-sub, semaphores |
| State | [effect-state](skills/effect-state/SKILL.md) | Ref variants, atomic updates, reactive state |
| Pipelines | [effect-streams](skills/effect-streams/SKILL.md) | Stream, Sink, Channel, backpressure |
| Time | [effect-time](skills/effect-time/SKILL.md) | Schedule, Cron, Duration, Clock |
| Data | [effect-data](skills/effect-data/SKILL.md) | Option, Result, collections, equality |
| Validation | [effect-schema](skills/effect-schema/SKILL.md) | Schema, decoding, transformations |
| Configuration | [effect-config](skills/effect-config/SKILL.md) | Config and ConfigProvider |
| Encoding | [effect-encoding](skills/effect-encoding/SKILL.md) | Wire formats, codecs, Crypto |
| Platform | [effect-platform](skills/effect-platform/SKILL.md) | Runtime adapters, files, processes, workers |
| HTTP | [effect-http](skills/effect-http/SKILL.md) | HTTP clients, servers, transport |
| Typed APIs | [effect-http-api](skills/effect-http-api/SKILL.md) | HTTP endpoint contracts and OpenAPI |
| RPC | [effect-rpc](skills/effect-rpc/SKILL.md) | RPC contracts and sockets |
| SQL | [effect-sql](skills/effect-sql/SKILL.md) | SQL clients, transactions, migrations |
| Observability | [effect-observability](skills/effect-observability/SKILL.md) | Logs, metrics, tracing, exporters |
| CLI | [effect-cli-tools](skills/effect-cli-tools/SKILL.md) | Commands, prompts, code generation |
| AI | [effect-ai](skills/effect-ai/SKILL.md) | Language models, tools, MCP, providers |
| Durable systems | [effect-durable-systems](skills/effect-durable-systems/SKILL.md) | Workflows, cluster, persistence, event log |
| Testing | [effect-testing](skills/effect-testing/SKILL.md) | TestClock, deterministic Layers, Vitest |
| Reactivity | [effect-reactivity](skills/effect-reactivity/SKILL.md) | Atoms and UI bindings |

## Version policy

These skills use Effect's v4 release-candidate source and documentation as
their primary reference, inspected at 4.0.0-rc.117 (upstream commit
0cbb45792b59e9ea00e19001a019e790d53407e6). Check the consuming project's
lockfile before applying an example: npm's default tag may still resolve to
v3, and unstable v4 entrypoints can change. Where a skill covers an unstable
area, it states the compatibility boundary explicitly.

## Contributing

The files are maintained by hand. See CONTRIBUTING.md and run
python3 scripts/validate-skills.py for packaging checks. That check does not
establish that a TypeScript snippet is valid for every Effect version; confirm
it against the installed declarations or upstream source.

Licensed under MIT.
