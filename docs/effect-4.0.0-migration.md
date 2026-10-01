# Effect 4.0.0 migration research

This note records the verified target for the repository's v4 adaptation.
Before this migration, the repository targeted `effect@4.0.0-rc.118` at
[`ad61db80`](https://github.com/Effect-TS/effect/commit/ad61db80efd52637e2901c5ee56b9e0fb4e8ac48).
The current [version policy](./version-policy.md) pins stable 4.0.0.
The requested stable release is now published: the
[GitHub release `effect@4.0.0`](https://github.com/Effect-TS/effect/releases/tag/effect%404.0.0)
is non-prerelease, was published on 2026-10-01, and its
[tag reference](https://api.github.com/repos/Effect-TS/effect/git/ref/tags/effect%404.0.0)
points to commit
[`67ba4e46`](https://github.com/Effect-TS/effect/commit/67ba4e46a11ccda0b6761578bfd22c04ae00167d).
The [npm `effect@4.0.0` metadata](https://registry.npmjs.org/effect/4.0.0)
and tarball are also available. npm now reports `latest: 4.0.0`, while the
`rc` dist-tag remains `4.0.0-rc.118`; examples should therefore pin the stable
version explicitly during this migration.

## Package and import surface

The release notes state that all Effect ecosystem packages share one version
and are released together. Functionality from `@effect/platform`,
`@effect/rpc`, `@effect/cluster`, `@effect/cli`, `@effect/ai`, `@effect/sql`,
`@effect/workflow`, and `@effect/experimental` is consolidated into `effect`.
Separate packages remain for platform adapters, SQL drivers, AI providers,
atom framework bindings, OpenTelemetry, Vitest, and tooling. See the
[stable release packaging notes](https://github.com/Effect-TS/effect/releases/tag/effect%404.0.0)
and the tagged [v3-to-v4 import map](https://github.com/Effect-TS/effect/blob/67ba4e46a11ccda0b6761578bfd22c04ae00167d/migration/v3-to-v4.md).

The stable [npm export map](https://registry.npmjs.org/effect/4.0.0) exposes
`effect/ai`, `effect/cli`, `effect/cluster`, `effect/encoding`,
`effect/eventlog`, `effect/http`, `effect/http-api`, `effect/net`,
`effect/observability`, `effect/persistence`, `effect/process`,
`effect/reactivity`, `effect/rpc`, `effect/schema`, `effect/socket`,
`effect/sql`, `effect/testing`, `effect/workers`, and `effect/workflow`, as
well as their module files. Imports must use these paths; the old
`effect/unstable/*` segment has no compatibility export. The release notes mark
these modules `@stability unstable`, so a future minor can still break them.
`effect` has no runtime dependencies.

The stable source has `Context.Service` and `Context.Reference` in
[`packages/effect/src/Context.ts`](https://github.com/Effect-TS/effect/blob/67ba4e46a11ccda0b6761578bfd22c04ae00167d/packages/effect/src/Context.ts).
There is no `ServiceMap` module or `effect/ServiceMap` export at this tag:
`Context` itself is the typed map of service implementations. Do not add a
`ServiceMap` import while adapting the examples. The tagged
[services migration](https://github.com/Effect-TS/effect/blob/67ba4e46a11ccda0b6761578bfd22c04ae00167d/migration/services.md)
requires `Context.Tag`, `Context.GenericTag`, `Effect.Tag`, and `Effect.Service`
callers to move to `Context.Service`; class syntax changes to
`class X extends Context.Service<X, Shape>()("X") {}`. `Effect.Tag` accessor
proxies are gone; use `yield* X` (preferred), `X.use`, or `X.useSync`. A
`Context.Service` `make` option stores construction logic but does not create a
`.Default` layer; build one explicitly with `Layer.effect` and provide its
dependencies with `Layer.provide`.

## Core and error-handling changes

The v4 release notes describe the rewritten fiber runtime, flat `Cause`,
`Context.Reference` replacing `FiberRef`, and the new STM boundary
(`Effect.tx` with `Tx*` data types). The tagged
[fiber-reference migration](https://github.com/Effect-TS/effect/blob/67ba4e46a11ccda0b6761578bfd22c04ae00167d/migration/fiberref.md)
and [runtime migration](https://github.com/Effect-TS/effect/blob/67ba4e46a11ccda0b6761578bfd22c04ae00167d/migration/runtime.md)
are the authority for code that still mentions `FiberRef` or `Runtime<R>`;
`Runtime<R>` was removed and execution uses `Effect.run*` with a `Context`.

The tagged [error-handling migration](https://github.com/Effect-TS/effect/blob/67ba4e46a11ccda0b6761578bfd22c04ae00167d/migration/error-handling.md)
gives these renames:

| v3 API | v4 API |
| --- | --- |
| `Effect.catchAll` | `Effect.catch` |
| `Effect.catchAllCause` | `Effect.catchCause` |
| `Effect.catchAllDefect` | `Effect.catchDefect` |
| `Effect.catchSome` | `Effect.catchFilter` |
| `Effect.catchSomeCause` | `Effect.catchCauseFilter` |
| `Effect.catchSomeDefect` | removed |

`catchTag`, `catchTags`, and `catchIf` remain. v4 also adds `catchReason`,
`catchReasons`, and the eager `catchEager` variant.

## Schema and testing changes

Schema v4 is a new implementation with class-based schemas, `make`
constructors, effectful decoding with services, and `SchemaRepresentation`
support for JSON Schema, OpenAPI, TypeScript code generation, and AI
structured output. The tagged [Schema migration](https://github.com/Effect-TS/effect/blob/67ba4e46a11ccda0b6761578bfd22c04ae00167d/migration/schema.md)
is required for v3 code: `validate*` and `Schema.Data` were removed, `Date` now
means the self schema (`DateFromString` preserves the v3 string transform),
`*FromSelf` names were simplified, and optional fields use `optionalKey` versus
`optional` explicitly.

Stable 4.0.0 also contains changes after rc.118. The release body records that
`Schema.brand` accepts one concrete identifier at a time and is type-only (it
is not retained in AST annotations or `SchemaRepresentation`); reapply the
brand after rebuilding a representation, while `Schema.fromBrand` checks remain
preserved. `Array`, `Chunk`, `Effect`, `Record`, and `Option` partition/separate
helpers now return `[successes, failures]`, so code using rc.118's previous
order must swap its tuple handling. `TestSchema.verifyLosslessTransformation`
is renamed to `verifyRoundTrip`, and stable 4.0.0 adds
`succeedEffect`, `failEffect`, and `verifyRoundTripEffect`. These exact changes
are listed in the [stable release notes](https://github.com/Effect-TS/effect/releases/tag/effect%404.0.0)
and implemented by commits
[`cbfc7b42`](https://github.com/Effect-TS/effect/commit/cbfc7b422046111c439a69ecbce7fc4f4899789d),
[`ef7d77f3`](https://github.com/Effect-TS/effect/commit/ef7d77f382dcb2a4f7648211ed6d674984a47c36),
[`35ac25a8`](https://github.com/Effect-TS/effect/commit/35ac25a80bec4977a082af57a618d6a02bb41e25), and
[`735b77b6`](https://github.com/Effect-TS/effect/commit/735b77b65ca909ca6e41915f0d1366531c32142a).

The old fast-check bridge is no longer the Schema property-testing authority.
The tagged migration says to use `effect/Arbitrary` (`Arbitrary.schema`,
`sampleEffect`, and `checkEffect`) and to change `@effect/vitest` options from
`fastCheck: { numRuns }` to `arbitrary: { runs }`. Raw fast-check values are not
accepted by `it.prop`, `it.effect.prop`, or `it.live.prop`; use a Schema or a
native Arbitrary, or use fast-check directly. Stable `@effect/vitest` requires
Vitest 5 (`>=5.0.0 <6.0.0`) and peers on `effect: ^4.0.0`, as shown by its
[published package metadata](https://registry.npmjs.org/@effect%2fvitest/4.0.0).

## Platform and companion package pins

Pin every installed Effect package to `4.0.0` while adapting this repository.
Verified stable metadata:

- [`@effect/platform-node@4.0.0`](https://registry.npmjs.org/@effect%2fplatform-node/4.0.0)
  peers on `effect: ^4.0.0`, depends on `@effect/platform-node-shared: ^4.0.0`,
  and requires Node `>=18.0.0`.
- [`@effect/ai-openai@4.0.0`](https://registry.npmjs.org/@effect%2fai-openai/4.0.0)
  peers on `effect: ^4.0.0`.
- [`@effect/sql-pglite@4.0.0`](https://registry.npmjs.org/@effect%2fsql-pglite/4.0.0)
  peers on `effect: ^4.0.0` and depends on `@electric-sql/pglite`.
- [`@effect/vitest@4.0.0`](https://registry.npmjs.org/@effect%2fvitest/4.0.0)
  peers on `effect: ^4.0.0` and Vitest 5.

The release also documents new packages (`@effect/platform-deno`,
`@effect/sql-pglite`, `@effect/ai-openai-compat`, `@effect/ai-typesafe`,
framework atom bindings, `@effect/openapi-generator`, and
`@effect/doctest`) and requires TypeScript 5.9 or newer (TypeScript 7 is
recommended). Platform-specific driver/provider APIs and the Vitest re-export
remain `@stability unstable` because they expose third-party dependencies.

## Adaptation checklist

1. Change `effect` and each installed `@effect/*` package from `4.0.0-rc.118`
   to exact `4.0.0`; keep platform/driver/provider packages separate where the
   stable package map requires them.
2. Re-run import checks against the stable export map and remove any
   `effect/unstable/*` path; use `effect/http-api` rather than `httpapi`.
3. Audit service examples for `Context.Service` class/function syntax, removed
   tag accessors, explicit layers, and any mistaken `ServiceMap` import.
4. Audit `catchAll*`/`catchSome*`, `FiberRef`, `Runtime<R>`, and Schema v3
   constructors against the tagged migration files.
5. Update partition/separate tuple order, Schema branding, TestSchema names,
   and native Arbitrary/Vitest options before running snippets and examples.
