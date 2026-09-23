---
name: effect-cli-tools
description: "Use when building typed command-line interfaces, prompts, completions, terminal output, documentation generation, doctests, or OpenAPI code generation with Effect."
---

# Effect CLI and tooling

Use effect/cli for Argument, Command, Flag, Param, Prompt, HelpDoc,
Completions, CliConfig, and CliOutput. Use the separate @effect/docgen,
@effect/doctest, and @effect/openapi-generator packages for repository tools.

## Design a command as a boundary

Parse flags into a typed value, validate it with Schema or a domain
constructor, then call an Effect service. Keep terminal rendering and exit
codes in the CLI layer. Do not put process.env, file paths, or SDK calls in
the command parser.

```ts
import { Effect } from "effect"
import { Command, Flag } from "effect/cli"

const port = Flag.Int("port").pipe(Flag.withDefault(8080))
const serve = Command.make("serve", { port }).pipe(
  Command.withHandler(({ port }) => Effect.logInfo("listening on " + port))
)

const cli = Command.run(serve, {
  version: "1.0.0"
})
```

The CLI API is unstable in v4; verify the current Options/Command names and
the platform runner before copying this shape. Test parsing separately from
the effectful handler.

## Interactive behavior

Prompts need cancellation, non-interactive fallbacks, and a stable exit code.
Completions and HelpDoc should be generated from the same command tree so
documentation does not drift. Never echo secrets typed into a prompt.

## Tooling packages

- Docgen should run against the exact package graph used by CI and publish
  deterministic output.
- Doctest examples are executable contracts; keep them small and avoid
  credentials or network access.
- OpenAPI generation should consume the typed HTTP API contract, not a second
  hand-maintained schema.

## Review traps

- Parsing a number or URL with an unchecked cast.
- Returning a successful process exit after a handler failure.
- Starting a prompt in a CI/non-TTY process without a fallback.
- Generating docs from a different Effect version than the package being
  released.

## References

- [Effect CLI source](https://github.com/Effect-TS/effect/tree/main/packages/effect/src/cli)
- [Effect CLI API](https://effect.website/docs/v4/api/effect)
- [Effect tooling packages](https://github.com/Effect-TS/effect/tree/main/packages/tools)
- [Effect documentation](https://effect.website/docs)
