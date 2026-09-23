---
name: effect-http-api
description: "Use when defining typed HTTP endpoints and middleware with effect/http-api, HttpApiBuilder, HttpApiClient, OpenApi, security, HttpApiScalar, HttpApiSwagger, or generated tests."
---

# Effect typed HTTP APIs

Use this skill when an HTTP surface should be a typed contract rather than a
collection of ad hoc handlers. It covers HttpApi, HttpApiEndpoint,
HttpApiGroup, HttpApiSchema, HttpApiMiddleware, HttpApiSecurity,
HttpApiBuilder, HttpApiClient, OpenApi, HttpApiScalar, HttpApiSwagger, and
HttpApiTest.

## Define the contract first

Start with endpoint input, output, and error Schemas. Group related endpoints,
name the security requirement, and decide which errors are part of the public
contract. Generate OpenAPI from that same contract; do not maintain a second
hand-written specification.

```ts
import { Schema } from "effect"
import {
  HttpApi,
  HttpApiEndpoint,
  HttpApiGroup,
  HttpApiSchema
} from "effect/http-api"

const User = Schema.Struct({ id: Schema.String, name: Schema.String })
const NotFound = Schema.Struct({ _tag: Schema.Literal("NotFound") }).pipe(
  HttpApiSchema.status(404)
)

const getUser = HttpApiEndpoint.get("getUser", "/users/:id", {
  params: Schema.Struct({ id: Schema.String }),
  success: User,
  error: NotFound
})

const Users = HttpApiGroup.make("users").add(getUser)
const api = HttpApi.make("users-api").add(Users)
```

The v4 API is still unstable; verify builder method names and imports in the
installed package before copying this shape.

## Implement and consume

Use HttpApiBuilder to provide handlers as Effects. Keep handler code focused
on mapping the validated request to a domain service. Use HttpApiClient for
callers so path parameters, success values, and declared errors stay typed.
Compose authentication and authorization through HttpApiSecurity and
middleware rather than duplicating checks in every handler.

## OpenAPI and compatibility

Treat generated OpenAPI as a review artifact. Check that status codes,
examples, pagination, error bodies, and security schemes are accurate.
HttpApiScalar and HttpApiSwagger are presentation tools; they must not become
the source of truth.
When evolving an API, add fields compatibly, version breaking changes, and
test old clients with HttpApiTest.

## Review traps

- Declaring a success schema but returning an unvalidated SDK object.
- Putting internal exception messages in a public error schema.
- Defining authorization in middleware but forgetting one endpoint group.
- Generating an OpenAPI document that omits a middleware or security scheme.
- Importing v3 http-api examples into a v4 release-candidate project.

## References

- [Effect HTTP API modules](https://effect.website/docs/v4/api/effect)
- [HttpApi source](https://github.com/Effect-TS/effect/tree/main/packages/effect/src/http-api)
- [OpenAPI API](https://effect.website/docs/v4/api/effect/unstable/httpapi/OpenApi)
- [Effect documentation](https://effect.website/docs)
