# Effect v4 version policy

All executable examples in this repository target exactly `effect@4.0.0`.
The [official release](https://github.com/Effect-TS/effect/releases/tag/effect%404.0.0)
is tagged at commit
[`67ba4e46a11ccda0b6761578bfd22c04ae00167d`](https://github.com/Effect-TS/effect/commit/67ba4e46a11ccda0b6761578bfd22c04ae00167d).
The [tag reference](https://api.github.com/repos/Effect-TS/effect/git/ref/tags/effect%404.0.0)
records that exact commit. The [npm dist-tags](https://registry.npmjs.org/effect)
publish `4.0.0` as the stable `latest` line. Keep the exact pin in this
repository so snippets and integration dependencies cannot drift independently.
The [4.0.0 migration research note](effect-4.0.0-migration.md) records the
stable release's post-RC API changes and the verification sources used here.

Use the [published 4.0.0 export map](https://registry.npmjs.org/effect/4.0.0)
as the import authority, and the [tagged package source](https://github.com/Effect-TS/effect/blob/67ba4e46a11ccda0b6761578bfd22c04ae00167d/packages/effect/package.json)
and its type declarations to check named APIs. Stable modules use published
`effect/*` exports (for example `effect/Effect`, `effect/Schema`, and
`effect/Context`). The 4.0.0 package exports formerly separate and unstable
barrels at top-level paths under `effect/*`, including `http`, `http-api`, `sql`, `ai`,
`cli`, `rpc`, `cluster`, `workflow`, `eventlog`, and `persistence`; these APIs
remain marked `@stability unstable`. Use those published paths in skills and
examples. The old `effect/unstable/*` paths are removed, and `httpapi` is now
`http-api`. `Arbitrary` is available from `effect` or `effect/Arbitrary`.
The former `effect/Encoding` module is split into format-specific modules under
`effect/encoding`, including `Base64`, `Base64Url`, `Hex`, and `EncodingError`.
The
[v4 migration guide](https://github.com/Effect-TS/effect/blob/67ba4e46a11ccda0b6761578bfd22c04ae00167d/MIGRATION.md)
states that unstable modules may change incompatibly in minor releases; even
within v4, recheck the package exports and types before upgrading.

Pin separately installed `@effect/*` integration packages to the **same exact
`4.0.0` version** when used. The tagged
[migration guide](https://github.com/Effect-TS/effect/blob/67ba4e46a11ccda0b6761578bfd22c04ae00167d/MIGRATION.md)
describes the unified v4 release train; published
[`@effect/sql-pg`](https://registry.npmjs.org/@effect%2fsql-pg/4.0.0)
and [`@effect/platform-node`](https://registry.npmjs.org/@effect%2fplatform-node/4.0.0)
declare peers on `effect@^4.0.0`. A compatible peer range is not a
reason to leave this repository's examples floating across releases.

Effect v3 packages and imports are not compatible with these v4 examples. v4
consolidates former `@effect/platform`, `@effect/rpc`, and other modules into
`effect`, changes service and API names, and replaces some direct imports;
consult the tagged [migration guide](https://github.com/Effect-TS/effect/blob/67ba4e46a11ccda0b6761578bfd22c04ae00167d/MIGRATION.md)
and [import map](https://github.com/Effect-TS/effect/blob/67ba4e46a11ccda0b6761578bfd22c04ae00167d/migration/v3-to-v4.md)
when porting v3 code. No v3 fallback or compatibility alias is promised here.

Finally, do not substitute the repository's moving `main` branch for the
published release: `main` may contain unreleased changes after 4.0.0. Use the
tagged package source and published export map above when checking imports.
