# Task and composition index

Select a skill by the decision being made, not simply by an imported symbol.
Every skill stands alone after installation; these combinations are optional
paths through related responsibilities. All module paths below are for the
[pinned 4.0.0 release](version-policy.md).

| Decision | Primary skill | Adjacent responsibility |
| --- | --- | --- |
| Describe execution, errors, and a run boundary | [core](../skills/effect-core/SKILL.md) | [services](../skills/effect-services/SKILL.md) provides dependencies and Scope |
| Assemble dependencies and scoped clients | [services](../skills/effect-services/SKILL.md) | [config](../skills/effect-config/SKILL.md) loads settings; [platform](../skills/effect-platform/SKILL.md) supplies runtime adapters |
| Coordinate fibers and bounded queues | [concurrency](../skills/effect-concurrency/SKILL.md) | [streams](../skills/effect-streams/SKILL.md) owns incremental pipelines; [time](../skills/effect-time/SKILL.md) owns scheduling |
| Update in-process state atomically | [state](../skills/effect-state/SKILL.md) | [reactivity](../skills/effect-reactivity/SKILL.md) connects atoms to UI; [persistence](../skills/effect-persistence/SKILL.md) survives restarts |
| Represent absence or pure data | [data](../skills/effect-data/SKILL.md) | [schema](../skills/effect-schema/SKILL.md) proves untrusted representations |
| Validate or transform external values | [schema](../skills/effect-schema/SKILL.md) | [encoding](../skills/effect-encoding/SKILL.md) handles bytes/text; [config](../skills/effect-config/SKILL.md) describes application settings |
| Send or serve ordinary HTTP | [HTTP](../skills/effect-http/SKILL.md) | [HTTP API](../skills/effect-http-api/SKILL.md) adds endpoint contracts and OpenAPI |
| Define typed remote procedures | [RPC](../skills/effect-rpc/SKILL.md) | [cluster](../skills/effect-cluster/SKILL.md) routes entity IDs to owners |
| Query relational records and transact | [SQL](../skills/effect-sql/SKILL.md) | [persistence](../skills/effect-persistence/SKILL.md) owns key-value/cache/queue abstractions |
| Resume a named job after restart | [workflow](../skills/effect-workflow/SKILL.md) | [persistence](../skills/effect-persistence/SKILL.md) backs engine/queues; [eventlog](../skills/effect-eventlog/SKILL.md) records domain events |
| Emit operational signals | [observability](../skills/effect-observability/SKILL.md) | [testing](../skills/effect-testing/SKILL.md) proves behavior without live exporters |
| Parse an interactive command | [CLI](../skills/effect-cli/SKILL.md) | [platform](../skills/effect-platform/SKILL.md) owns process lifecycle |
| Call models or expose tools | [AI](../skills/effect-ai/SKILL.md) | [schema](../skills/effect-schema/SKILL.md) validates tools/output; [services](../skills/effect-services/SKILL.md) provides clients |

## Common composition paths

### HTTP API backed by SQL

`effect-schema` defines request, response, and public error schemas;
`effect-http-api` binds them to routes and generated clients;
`effect-services` keeps handlers dependent on a `Users` capability;
`effect-sql` implements that capability with parameterized statements and a
scoped client; `effect-platform` runs the server. Use `effect-http` directly
for transport details or a client without a typed API contract. Decode at
the HTTP boundary, translate expected domain failures to declared status
codes, and keep SQL and connection lifetime outside individual requests.

The checked [implementation](../examples/user-api.ts) and
[test](../examples/user-api.test.ts) create a user over HTTP (201), fetch it
(200), reject an invalid body (400), return a typed missing-user error (404),
and reopen a file-backed database before fetching the same user again. Run
`devenv shell -- npm test` after `npm ci` to exercise the full path.

### Validate external data

Use `effect-encoding` to decode the declared byte/text format, then
`effect-schema` to turn `unknown` into a domain value. Use `effect-data` for
pure absence and variants after decoding. `effect-config` is the separate
boundary for environment settings and secrets: evaluate it at startup and
inject the resolved value via `effect-services`. Test malformed, missing,
optional, and transformed inputs without a type cast.

### Provide a service graph

Define a `Context.Service` capability in `effect-services`; provide one
scoped `Layer` composed from `effect-config` and the selected
`effect-platform`, HTTP, or SQL adapter. Domain Effects retain their service
requirement. `effect-testing` substitutes a deterministic Layer and checks
construction failure, interruption, and finalization. Run only at the host
boundary described by `effect-core`.

### Select persistence

Choose `effect-state` for process-local atomic values, `effect-sql` for
relational queries/transactions, and `effect-persistence` for a key-value
store, persisted cache/queue, or shared rate limiter. `effect-workflow`
adds restart-surviving execution identity and replay; `effect-eventlog`
adds append-only facts and replayable handlers; `effect-cluster` assigns
sharded entity ownership. A memory Layer only proves wiring, never durability
or cross-process delivery. Version persisted schemas and make redelivered
external writes idempotent.
