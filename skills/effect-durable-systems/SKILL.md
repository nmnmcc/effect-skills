---
name: effect-durable-systems
description: Use when building or reviewing Effect v4 durable or distributed systems with effect/workflow, effect/cluster, effect/rpc, effect/eventlog, or effect/persistence. Trigger for durable workflows, activities, queues, deferred values, entity sharding, singleton runners, typed RPC, event journals and replication, persisted caches/queues, rate limiting, Redis or SQL storage, replay, idempotency, or migration boundaries; check the v3/v4 and unstable-module gate first.
---

# Effect durable systems

This skill covers the v4 modules that turn an `Effect` program into a durable
workflow, a distributed entity, a schema-checked RPC, an event log, or a
persistent storage primitive.

| Area | Modules and responsibility |
| --- | --- |
| Workflows | `effect/workflow`: `Workflow`, `WorkflowEngine`, `Activity`, `DurableClock`, `DurableDeferred`, `DurableQueue`, and `WorkflowProxy` for durable execution, suspension, replay, and workflow RPC/HTTP projections. |
| Cluster | `effect/cluster`: `Entity`, `EntityProxy`, `Sharding`, `Runner`/`Runners`, `Singleton`, runner and message storage, and cluster workflow integration. |
| RPC | `effect/rpc`: `Rpc`, `RpcGroup`, `RpcSchema`, `RpcClient`, `RpcServer`, middleware, serialization, worker protocols, and `RpcTest`. |
| Event log | `effect/eventlog`: `EventGroup`, `EventLog`, `EventJournal`, encryption/identity, remote replication, and HTTP/RPC server modules. |
| Persistence | `effect/persistence`: `KeyValueStore`, `Persistence`, `PersistedCache`, `PersistedQueue`, `RateLimiter`, and `Redis` adapters. |

## Activate

Activate when a request mentions one of these import paths, asks for a job that
survives a restart, wants `execute`/`poll`/`resume`, needs a durable queue or
timer, routes messages to entity IDs, adds an RPC transport or worker, records
events for replay/replication, or adds Redis/SQL persistence. Also activate when
reviewing code that assumes exactly-once delivery, performs non-idempotent work
before a suspension, uses an in-memory layer in a production deployment, or
changes a persisted schema without a migration plan.

## Version and stability gate

Inspect `package.json` and the lockfile first. The upstream main snapshot used by
this repository is Effect `4.0.0-rc.117`; `effect/workflow`, `effect/cluster`,
`effect/rpc`, `effect/eventlog`, and `effect/persistence` are currently marked
unstable v4 APIs. npm may still resolve Effect v3 (for example `3.22.x`), whose
module names, constructors, and runtime contracts differ. Do not copy v4
imports into a v3 project without an explicit upgrade or a v3-specific
implementation. Pin compatible package versions and treat workflow payloads,
RPC wire formats, event entries, and persisted values as versioned contracts.

## Choose the boundary

1. Use a `Workflow` when the operation has a stable name, a durable result, and
   a deterministic idempotency key. Give it payload, success, and error schemas.
   `execute` can wait for the result; `{ discard: true }` returns an execution id
   for an asynchronous API, and the engine mediates `poll`, `interrupt`, and
   `resume`.
2. Use an `Activity` for a named effect whose encoded success or typed failure
   can be stored and replayed. Use `DurableClock` and `DurableDeferred` for
   engine-visible time and signals. Use `DurableQueue` when a worker should run
   outside the workflow fiber and later complete its deferred result.
3. Use an `Entity` when state is addressed by an entity id and only one active
   owner should process that id. Define its protocol with `Rpc`; let `Sharding`
   assign shards and runners. Use `Singleton.make` for one active cluster-wide
   effect rather than inventing a leader-election loop.
4. Use `RpcGroup` when a typed request/response or stream crosses a transport.
   Keep schemas independent of HTTP, sockets, workers, or stdio; choose
   `RpcSerialization` and `RpcClient`/`RpcServer` layers at the deployment edge.
5. Use an `EventLog` for append-only facts, replay, conflict handling, or remote
   replication. Define event groups with primary keys, register every handler,
   and choose encrypted identity/journal/remote layers explicitly.
6. Use `Persistence`/`PersistedCache` for schema-encoded exits and TTLs,
   `PersistedQueue` for background work, `RateLimiter` for shared admission
   control, and `KeyValueStore`/`Redis`/SQL layers for the backing store.

## Workflow, activity, and durable queue

```ts
import { Effect, Layer, Schema } from "effect"
import { PersistedQueue } from "effect/persistence"
import { DurableQueue, Workflow, WorkflowEngine } from "effect/workflow"

const Mail = DurableQueue.make({
  name: "mail.send",
  payload: { id: Schema.String, to: Schema.String },
  success: Schema.Void,
  error: Schema.String,
  idempotencyKey: ({ id }) => id
})

const SendMail = Workflow.make("mail.Send", {
  payload: { id: Schema.String, to: Schema.String },
  success: Schema.Void,
  error: Schema.String,
  idempotencyKey: ({ id }) => id
})

const sendMail = ({ to }: { readonly id: string; readonly to: string }) =>
  Effect.log(`send mail to ${to}`).pipe(Effect.asVoid)

const PersistedQueueLayer = PersistedQueue.layer.pipe(
  Layer.provideMerge(PersistedQueue.layerStoreMemory)
)

const AppLayer = Layer.mergeAll(
  SendMail.toLayer((payload) => DurableQueue.process(Mail, payload)),
  DurableQueue.worker(Mail, sendMail, { concurrency: 8 })
).pipe(
  Layer.provideMerge(WorkflowEngine.layerMemory),
  Layer.provideMerge(PersistedQueueLayer)
)

const start = SendMail.execute({ id: "mail-42", to: "ops@example.com" }, { discard: true })
const execution = start.pipe(Effect.provide(AppLayer))
```

The memory layers make this example testable; production uses a durable
`WorkflowEngine` and a shared persisted-queue store. `DurableQueue.process`
offers an encoded item, awaits a `DurableDeferred`, and resumes the workflow
when `DurableQueue.worker` records the handler `Exit`. Delivery is at-least-once:
a crash after the handler succeeds but before acknowledgement can run it again,
so `sendMail` must be idempotent (for example, use `id` as an outbox key).

For a direct workflow activity, define a stable name and result schemas and call
the named effect inside `Workflow.toLayer`:

```ts
import { Effect, Schema } from "effect"
import { Activity, Workflow } from "effect/workflow"

const Charge = Activity.make({
  name: "billing.charge",
  success: Schema.Void,
  error: Schema.String,
  execute: Effect.succeed(undefined)
})

const Billing = Workflow.make("billing.run", {
  payload: { id: Schema.String },
  success: Schema.Void,
  error: Schema.String,
  idempotencyKey: ({ id }) => id
})

const BillingLayer = Billing.toLayer(() => Charge.execute)
```

Completed activity results can be memoized by the engine. If the workflow
suspends on a durable clock, deferred, child workflow, or queue, the body before
the suspension can run again during replay; put external writes in an activity,
make them idempotent, and use `withCompensation` for explicit cleanup. A stable
workflow name or idempotency key is not a substitute for a transaction key in an
external system.

## RPC and cluster entities

```ts
import { Effect, Schema } from "effect"
import { Entity, ShardingConfig } from "effect/cluster"
import { Rpc } from "effect/rpc"

const Account = Entity.make("Account", [
  Rpc.make("balance", {
    payload: { accountId: Schema.String },
    success: Schema.Number,
    error: Schema.Literal("missing")
  })
])

const AccountLayer = Account.toLayer({
  balance: ({ payload }) =>
    payload.accountId === "closed"
      ? Effect.fail("missing" as const)
      : Effect.succeed(100)
})

// The real deployment also provides Sharding, Runners, a runner health layer,
// and message/runner storage. ShardingConfig controls mailbox and assignment
// behavior; do not hide those choices in a global singleton.
const testCall = Effect.scoped(Effect.gen(function*() {
  const makeClient = yield* Entity.makeTestClient(Account, AccountLayer)
  const client = yield* makeClient("account-42")
  return yield* client.balance({ accountId: "account-42" })
})).pipe(Effect.provide(ShardingConfig.layerDefaults))
```

`Entity.make` groups typed RPC definitions, `toLayer` registers handlers with
`Sharding`, and `entity.client` creates an RPC client by entity id. In a real
cluster, shard ownership, runner addresses, mailbox capacity, persisted message
storage, and entity annotations are deployment contracts. A `Singleton.make`
layer starts its effect only on the runner that owns the singleton shard; a
runner move or layer shutdown interrupts it, and an unhandled `run` failure is a
defect. Treat `EntityProxy`/`WorkflowProxy` as generated protocol projections,
not as a replacement for the underlying schemas.

For a non-cluster transport, define an `RpcGroup` from the same `Rpc` values,
implement it with `group.toLayer`, and mount `RpcServer.layerHttp` (or a socket,
worker, stdio, or custom protocol). Construct clients with `RpcClient.make` and
provide the matching serialization and protocol layers. `RpcTest.makeClient`
is the no-serialization path for tests; it should not be mistaken for a network
compatibility test.

## Event log and persistent state

```ts
import { Effect, Layer } from "effect"
import * as EventGroup from "effect/eventlog/EventGroup"
import * as EventJournal from "effect/eventlog/EventJournal"
import * as EventLog from "effect/eventlog/EventLog"
import * as EventLogEncryption from "effect/eventlog/EventLogEncryption"
import { Schema } from "effect"

const Users = EventGroup.empty.add({
  tag: "UserCreated",
  primaryKey: (payload: { readonly id: string }) => payload.id,
  payload: Schema.Struct({ id: Schema.String })
})
const UserSchema = EventLog.schema(Users)

const Handlers = EventLog.group(Users, (handlers) =>
  handlers.handle("UserCreated", ({ payload }) =>
    Effect.log(`rebuild user ${payload.id}`).pipe(Effect.asVoid)
  )
).pipe(Layer.provide(EventLog.layerRegistry))

const LogLayer = EventLog.layer(UserSchema, Handlers).pipe(
  Layer.provide(EventJournal.layerMemory),
  Layer.provide(
    Layer.effect(EventLog.Identity, EventLog.makeIdentity).pipe(
      Layer.provide(EventLogEncryption.layerSubtle)
    )
  )
)

const append = Effect.gen(function*() {
  const write = yield* EventLog.makeClient(UserSchema)
  yield* write("UserCreated", { id: "user-1" })
}).pipe(Effect.provide(LogLayer))
```

The schema only describes events; `EventLog.group` must register handlers before
writing. `EventJournal` owns entries and `EventLog.Identity` authenticates and
optionally encrypts remote replication. Plan primary-key conflicts, compaction,
remote retries, and event schema evolution before shipping an event tag.

`Persistence.layerMemory`, `layerRedis`, `layerSql`, and `layerKvs` provide the
same `Persistence` interface with different durability. `PersistedCache` stores
the lookup `Exit` (including typed failures) with a persistent TTL and a scoped
in-memory cache. `PersistedQueue.offer` de-duplicates by id and `take` retries
failed handlers until `maxAttempts`; exhausted items become dead letters. Run
`PersistedQueue.layerCleanup` from one maintenance instance, and namespace store
ids so independent applications cannot collide. `RateLimiter` requires the same
shared store for cross-process limits; a process-local memory layer is only a
test fixture.

## Failure, lifecycle, and runtime boundaries

- Every workflow, activity, queue payload, RPC request/reply, event payload, and
  persisted value needs an explicit `Schema`. Encoding and decoding services are
  part of the environment and must be provided at the boundary, not hidden in a
  handler.
- Workflow execution is engine-mediated. `poll` can return a suspended result;
  `interrupt` and `resume` act on an execution id and require the same durable
  engine state. A process-local `WorkflowEngine.layerMemory` loses executions on
  restart.
- Durable queues and persisted queues are at-least-once. A crash can redeliver
  work; handlers must be idempotent and safe under concurrent retries. When a
  durable queue item exhausts attempts it can be dead-lettered while its deferred
  remains unresolved, so provide an operational requeue/alert path.
- Durable clock/deferred suspension interrupts the current fiber intentionally.
  Register finalizers with the workflow scope and do not perform an irreversible
  external action immediately before a suspension unless it is replay-safe.
- RPC has two failure planes: typed procedure errors and transport/serialization
  errors (`RpcClientError`, protocol failures, disconnects). Validate both sides,
  keep defect schemas deliberate, and close streaming clients and servers with
  their scopes. A stream request can be cancelled by the client or by layer
  shutdown; handlers must release resources on interruption.
- Cluster ownership is dynamic. Shard reassignment interrupts local entity work;
  persisted messages require a real `MessageStorage` layer, and mailbox or
  runner health settings affect delivery. Do not infer exactly-once behavior from
  local entity tests.
- Event logs are append-only integration data. Encrypt identity keys, authenticate
  remotes, make handlers replay-safe, and version event schemas. A missing event
  handler is a defect; a remote or journal failure is an operational error that
  needs retry/alert policy.
- All store, runner, journal, RPC, and transport layers are scoped resources.
  Compose them with `Layer`, close the enclosing `Scope`, and keep credentials,
  connections, and fibers out of module-level mutable state.

## References

- Workflow API: https://effect.website/docs/v4/api/effect/unstable/workflow/Workflow
- Activity API: https://effect.website/docs/v4/api/effect/unstable/workflow/Activity
- DurableQueue API: https://effect.website/docs/v4/api/effect/unstable/workflow/DurableQueue
- WorkflowEngine API: https://effect.website/docs/v4/api/effect/unstable/workflow/WorkflowEngine
- Cluster Entity API: https://effect.website/docs/v4/api/effect/unstable/cluster/Entity
- RPC API: https://effect.website/docs/v4/api/effect/unstable/rpc/Rpc
- EventLog API: https://effect.website/docs/v4/api/effect/unstable/eventlog/EventLog
- PersistedQueue API: https://effect.website/docs/v4/api/effect/unstable/persistence/PersistedQueue
- Effect v4 source tree: https://github.com/Effect-TS/effect/tree/main/packages/effect/src
- Workflow source: https://github.com/Effect-TS/effect/tree/main/packages/effect/src/workflow
- RPC source: https://github.com/Effect-TS/effect/tree/main/packages/effect/src/rpc
- Cluster source: https://github.com/Effect-TS/effect/tree/main/packages/effect/src/cluster
- Event log source: https://github.com/Effect-TS/effect/tree/main/packages/effect/src/eventlog
- Persistence source: https://github.com/Effect-TS/effect/tree/main/packages/effect/src/persistence
