# Category map

Use the frontmatter descriptions for automatic routing. This page is a human
index for choosing a smaller installation.

| Skill | Primary modules and packages |
| --- | --- |
| effect-core | Effect, Cause, Exit, Result, Runtime, ManagedRuntime, ExecutionPlan |
| effect-services | Context, Layer, Scope, Resource, LayerMap, LayerRef, scoped caches |
| effect-concurrency | Fiber, FiberHandle, FiberSet, FiberMap, Deferred, Queue, PubSub, Semaphore, Pool |
| effect-state | Ref, SynchronizedRef, SubscriptionRef, ScopedRef, MutableRef, Tx* and mutable collections |
| effect-streams | Stream, Channel, Sink, Take, Pull, Chunk, ChannelSchema |
| effect-time | Schedule, Cron, Duration, DateTime, Clock, Scheduler, Random |
| effect-schema | Schema, SchemaAST, SchemaParser, SchemaIssue, transformations, JsonSchema, StandardSchema |
| effect-config | Config and ConfigProvider |
| effect-data | Option, Result, Data, Array, HashMap, HashSet, records, structs, equality, matching |
| effect-encoding | effect/encoding, Crypto, JsonPatch, JsonPointer |
| effect-platform | platform packages, FileSystem, Path, PlatformError, Stdio, process, net, socket, workers |
| effect-http | effect/http and transport-level HTTP |
| effect-http-api | effect/http-api and typed OpenAPI contracts |
| effect-rpc | effect/rpc and effect/socket |
| effect-sql | effect/sql and @effect/sql-* adapters |
| effect-observability | Logger, Metric, Tracer, ErrorReporter, observability, @effect/opentelemetry |
| effect-cli-tools | effect/cli, docgen, doctest, OpenAPI generator |
| effect-ai | effect/ai and @effect/ai-* providers |
| effect-durable-systems | workflow, cluster, eventlog, persistence |
| effect-testing | effect/testing and @effect/vitest |
| effect-reactivity | effect/reactivity and @effect/atom-* |

The categories intentionally overlap at boundaries. For example, an HTTP
handler normally uses effect-http-api, effect-schema, effect-services, and
effect-core together; install the smallest set that matches the task.
