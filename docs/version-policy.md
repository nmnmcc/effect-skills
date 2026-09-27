# Effect v4 version policy

All executable examples in this repository target exactly `effect@4.0.0-rc.117`.
The [official release](https://github.com/Effect-TS/effect/releases/tag/effect%404.0.0-rc.117)
is tagged at commit
[`14a3f140095fdebbff9162944fe7d4ea83e054e6`](https://github.com/Effect-TS/effect/commit/14a3f140095fdebbff9162944fe7d4ea83e054e6).
The [tag reference](https://api.github.com/repos/Effect-TS/effect/git/ref/tags/effect%404.0.0-rc.117)
records that exact commit. At the time of this policy, the
[npm dist-tags](https://registry.npmjs.org/effect) identify `4.0.0-rc.117` as
`rc` but still point `latest` to `3.22.2`: an unversioned install is not a
valid way to run these examples.

Use the [published rc.117 export map](https://registry.npmjs.org/effect/4.0.0-rc.117)
as the import authority, and the [tagged package source](https://github.com/Effect-TS/effect/blob/14a3f140095fdebbff9162944fe7d4ea83e054e6/packages/effect/package.json)
and its type declarations to check named APIs. Stable modules use published
`effect/*` exports (for example `effect/Effect`, `effect/Schema`, and
`effect/Context`). The rc.117 package exports unstable barrels under
`effect/unstable/*`, including `http`, `httpapi`, `sql`, `ai`, `cli`, `rpc`,
`cluster`, `workflow`, `eventlog`, and `persistence`. Use those published paths
in skills and examples, not later paths such as `effect/http`,
`effect/http-api`, `effect/sql`, or `effect/ai`. The
[v4 migration guide](https://github.com/Effect-TS/effect/blob/14a3f140095fdebbff9162944fe7d4ea83e054e6/MIGRATION.md)
states that unstable modules may change incompatibly in minor releases; even
within v4, recheck the package exports and types before upgrading.

Pin separately installed `@effect/*` integration packages to the **same exact
`4.0.0-rc.117` version** when used. The tagged
[migration guide](https://github.com/Effect-TS/effect/blob/14a3f140095fdebbff9162944fe7d4ea83e054e6/MIGRATION.md)
describes the unified v4 release train; published
[`@effect/sql-pg`](https://registry.npmjs.org/@effect%2fsql-pg/4.0.0-rc.117)
and [`@effect/platform-node`](https://registry.npmjs.org/@effect%2fplatform-node/4.0.0-rc.117)
declare peers on `effect@^4.0.0-rc.117`. A compatible peer range is not a
reason to leave this repository's examples floating across RCs.

Effect v3 packages and imports are not compatible with these v4 examples. v4
consolidates former `@effect/platform`, `@effect/rpc`, and other modules into
`effect`, changes service and API names, and replaces some direct imports;
consult the tagged [migration guide](https://github.com/Effect-TS/effect/blob/14a3f140095fdebbff9162944fe7d4ea83e054e6/MIGRATION.md)
and [import map](https://github.com/Effect-TS/effect/blob/14a3f140095fdebbff9162944fe7d4ea83e054e6/migration/v3-to-v4.md)
when porting v3 code. No v3 fallback or compatibility alias is promised here.

Finally, do not substitute the repository's moving `main` branch for the
published RC: a [post-release commit](https://github.com/Effect-TS/effect/compare/14a3f140095fdebbff9162944fe7d4ea83e054e6...0cbb45792b59e9ea00e19001a019e790d53407e6)
changed its [source export map](https://github.com/Effect-TS/effect/blob/0cbb45792b59e9ea00e19001a019e790d53407e6/packages/effect/package.json)
to top-level paths including `effect/http`, `effect/http-api`, and
`effect/sql`. Those paths belong to a later source state and cannot justify
imports in rc.117 examples.
