---
name: effect-encoding
compatibility: "Examples target effect@4.0.0-rc.117; Effect v3 requires migration."
description: "Use when encoding or decoding bytes and text, handling Base64, Hex, YAML, TOML, SSE, NDJSON, cryptography, or JSON patch boundaries in Effect."
---

# Effect encoding and cryptographic boundaries

Use the stable `Encoding` module for Base64, Base64Url, and Hex. The
`effect/unstable/encoding` modules add Ini, Ndjson, SchemaBinary, Sse, Toml,
and Yaml. Pair them with Crypto or JsonPatch only when signing or patching is
part of the wire protocol.

## Make the wire format explicit

Choose an encoding based on the protocol, not convenience. Base64Url is not
interchangeable with Base64, and text encodings must declare their character
set. A decoder should return a typed error rather than silently replacing
invalid bytes.

```ts
import { Effect, Encoding } from "effect"

const decodeToken = (token: string) =>
  Effect.fromResult(Encoding.decodeBase64Url(token)).pipe(
    Effect.mapError((cause) => ({ _tag: "InvalidToken" as const, cause }))
  )
```

`decodeBase64Url` returns a `Result` in rc.117; `Effect.fromResult` raises its
typed `EncodingError` in an Effect before mapping it to the domain error.

## Serialization and streaming

Use NDJSON and SSE when records arrive incrementally; do not collect an
unbounded input merely to parse it. Use SchemaBinary or a Schema-backed
format when both validation and serialization must be versioned. Preserve
record boundaries and reject trailing garbage when the protocol requires a
single document.

## Crypto and patch safety

Keep key material in a secret service and use Crypto through a Layer or
platform adapter. Authenticate before applying a JsonPatch supplied by an
untrusted caller, validate the path policy, and record the expected document
version. Encoding is not encryption and Base64 is not a security boundary.

## Review traps

- Decoding a user-controlled payload before applying size limits.
- Treating malformed UTF-8 as harmless replacement text.
- Applying JSON patches to a mutable shared object without a version check.
- Logging encoded credentials or ciphertext that is still sensitive.
- Mixing v3 and v4 module paths; encoding subpaths are unstable in v4.

## References

- [Encoding API](https://effect.website/docs/v4/api/effect/Encoding)
- [Pinned Encoding source](https://github.com/Effect-TS/effect/blob/effect%404.0.0-rc.117/packages/effect/src/Encoding.ts)
- [JsonPatch API](https://effect.website/docs/v4/api/effect/JsonPatch)
- [Crypto API](https://effect.website/docs/v4/api/effect/Crypto)
- [Effect source](https://github.com/Effect-TS/effect/tree/effect%404.0.0-rc.117/packages/effect/src/unstable/encoding)
