---
name: effect-encoding
description: "Use when encoding or decoding bytes and text, handling Base64, Hex, YAML, TOML, SSE, NDJSON, cryptography, or JSON patch boundaries in Effect."
---

# Effect encoding and cryptographic boundaries

Use the effect/encoding modules for explicit wire formats: Base64,
Base64Url, Hex, Ini, Ndjson, SchemaBinary, Sse, Toml, and Yaml. Pair them with
Crypto, JsonPatch, and JsonPointer when an encoded representation is signed,
patched, or transported.

## Make the wire format explicit

Choose an encoding based on the protocol, not convenience. Base64Url is not
interchangeable with Base64, and text encodings must declare their character
set. A decoder should return a typed error rather than silently replacing
invalid bytes.

```ts
import { Effect } from "effect"
import * as Base64Url from "effect/encoding/Base64Url"

const decodeToken = (token: string) =>
  Effect.fromResult(Base64Url.decode(token)).pipe(
    Effect.mapError((cause) => ({ _tag: "InvalidToken" as const, cause }))
  )
```

Read the installed v4 declarations for the exact return shape: some encoding
helpers are pure and some are represented as Effect failures. Keep that
difference visible at the boundary.

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

- [Effect encoding entrypoint](https://effect.website/docs/v4/api/effect)
- [JsonPatch API](https://effect.website/docs/v4/api/effect/JsonPatch)
- [Crypto API](https://effect.website/docs/v4/api/effect/Crypto)
- [Effect source](https://github.com/Effect-TS/effect/tree/main/packages/effect/src/encoding)
