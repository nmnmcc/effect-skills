import { PgliteClient } from "@effect/sql-pglite"
import { NodeHttpServer } from "@effect/platform-node"
import { Context, Effect, Layer, Schema } from "effect"
import { HttpRouter } from "effect/http"
import { HttpApi, HttpApiBuilder, HttpApiEndpoint, HttpApiGroup, HttpApiSchema } from "effect/http-api"
import { SqlClient } from "effect/sql"
import { createServer, type Server } from "node:http"

export const User = Schema.Struct({ id: Schema.String, name: Schema.String })
export const CreateUser = Schema.Struct({ name: Schema.NonEmptyString })
type User = typeof User.Type
type CreateUser = typeof CreateUser.Type

export class UserNotFound extends Schema.TaggedError<UserNotFound>()("UserNotFound", {
  id: Schema.String
}) {}

class Users extends Context.Service<Users, {
  readonly create: (input: CreateUser) => Effect.Effect<User>
  readonly get: (id: string) => Effect.Effect<User, UserNotFound>
}>()("example/Users") {}

const UsersLive = Layer.effect(Users, Effect.gen(function* () {
  const sql = yield* SqlClient.SqlClient
  yield* sql`CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, name TEXT NOT NULL)`

  return {
    create: (input: CreateUser) => Effect.gen(function* () {
      const user = { id: crypto.randomUUID(), name: input.name }
      yield* sql`INSERT INTO users (id, name) VALUES (${user.id}, ${user.name})`
      return user
    }).pipe(Effect.orDie),
    get: (id: string) => Effect.gen(function* () {
      const rows = yield* sql`SELECT id, name FROM users WHERE id = ${id}`
      if (rows.length === 0) return yield* new UserNotFound({ id })
      return yield* Schema.decodeUnknownEffect(User)(rows[0])
    }).pipe(Effect.catchTags({ SqlError: Effect.die, SchemaError: Effect.die }))
  }
}))

const UsersApi = HttpApiGroup.make("users")
  .add(HttpApiEndpoint.post("create", "/users", {
    payload: CreateUser,
    success: User.pipe(HttpApiSchema.status(201))
  }))
  .add(HttpApiEndpoint.get("get", "/users/:id", {
    params: { id: Schema.String },
    success: User,
    error: UserNotFound.pipe(HttpApiSchema.status(404))
  }))

const Api = HttpApi.make("user-api").add(UsersApi)
const Handlers = HttpApiBuilder.group(Api, "users", Effect.fn(function* (handlers) {
  const users = yield* Users
  return handlers.handleAll({
    create: ({ payload }) => users.create(payload),
    get: ({ params }) => users.get(params.id)
  })
}))

export const makeServerLayer = (dataDir: string, onServer: (server: Server) => void) => {
  const database = PgliteClient.layer({ dataDir })
  const routes = HttpApiBuilder.layer(Api).pipe(
    Layer.provide(Handlers.pipe(Layer.provide(UsersLive.pipe(Layer.provide(database)))))
  )
  return HttpRouter.serve(routes).pipe(
    Layer.provide(NodeHttpServer.layer(() => {
      const server = createServer()
      onServer(server)
      return server
    }, { port: 0, host: "127.0.0.1" }))
  )
}
