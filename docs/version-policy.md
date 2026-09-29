# Effect v4 version policy

All executable examples in this repository target exactly `effect@4.0.0-rc.118`.
The [official release](https://github.com/Effect-TS/effect/releases/tag/effect%404.0.0-rc.118)
is tagged at commit
[`ad61db80efd52637e2901c5ee56b9e0fb4e8ac48`](https://github.com/Effect-TS/effect/commit/ad61db80efd52637e2901c5ee56b9e0fb4e8ac48).
The [tag reference](https://api.github.com/repos/Effect-TS/effect/git/ref/tags/effect%404.0.0-rc.118)
records that exact commit. At the time of this policy, the
[npm dist-tags](https://registry.npmjs.org/effect) identify `4.0.0-rc.118` as
`rc` but still point `latest` to `3.22.2`: an unversioned install is not a
valid way to run these examples.

Use the [published rc.118 export map](https://registry.npmjs.org/effect/4.0.0-rc.118)
as the import authority, and the [tagged package source](https://github.com/Effect-TS/effect/blob/ad61db80efd52637e2901c5ee56b9e0fb4e8ac48/packages/effect/package.json)
and its type declarations to check named APIs. Stable modules use published
`effect/*` exports (for example `effect/Effect`, `effect/Schema`, and
`effect/Context`). The rc.118 package exports formerly unstable barrels at
top-level paths under `effect/*`, including `http`, `http-api`, `sql`, `ai`,
`cli`, `rpc`, `cluster`, `workflow`, `eventlog`, and `persistence`; these APIs
remain marked `@stability unstable`. Use those published paths in skills and
examples. The old `effect/unstable/*` paths are removed, and `httpapi` is now
`http-api`. `Arbitrary` is available from `effect` or `effect/Arbitrary`.
The former `effect/Encoding` module is split into format-specific modules under
`effect/encoding`, including `Base64`, `Base64Url`, `Hex`, and `EncodingError`.
The
[v4 migration guide](https://github.com/Effect-TS/effect/blob/ad61db80efd52637e2901c5ee56b9e0fb4e8ac48/MIGRATION.md)
states that unstable modules may change incompatibly in minor releases; even
within v4, recheck the package exports and types before upgrading.

Pin separately installed `@effect/*` integration packages to the **same exact
`4.0.0-rc.118` version** when used. The tagged
[migration guide](https://github.com/Effect-TS/effect/blob/ad61db80efd52637e2901c5ee56b9e0fb4e8ac48/MIGRATION.md)
describes the unified v4 release train; published
[`@effect/sql-pg`](https://registry.npmjs.org/@effect%2fsql-pg/4.0.0-rc.118)
and [`@effect/platform-node`](https://registry.npmjs.org/@effect%2fplatform-node/4.0.0-rc.118)
declare peers on `effect@^4.0.0-rc.118`. A compatible peer range is not a
reason to leave this repository's examples floating across RCs.

Effect v3 packages and imports are not compatible with these v4 examples. v4
consolidates former `@effect/platform`, `@effect/rpc`, and other modules into
`effect`, changes service and API names, and replaces some direct imports;
consult the tagged [migration guide](https://github.com/Effect-TS/effect/blob/ad61db80efd52637e2901c5ee56b9e0fb4e8ac48/MIGRATION.md)
and [import map](https://github.com/Effect-TS/effect/blob/ad61db80efd52637e2901c5ee56b9e0fb4e8ac48/migration/v3-to-v4.md)
when porting v3 code. No v3 fallback or compatibility alias is promised here.

Finally, do not substitute the repository's moving `main` branch for the
published RC: `main` may contain unreleased changes after rc.118. Use the
tagged package source and published export map above when checking imports.
