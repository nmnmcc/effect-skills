import assert from "node:assert/strict"
import { mkdtemp, rm } from "node:fs/promises"
import { type Server } from "node:http"
import { tmpdir } from "node:os"
import path from "node:path"
import { test } from "node:test"
import { Effect, Layer } from "effect"
import { makeServerLayer } from "./user-api.js"

test("validated HTTP API persists a user across server and database restarts", async () => {
  const dataDir = await mkdtemp(path.join(tmpdir(), "effect-skills-user-api-"))
  const start = async (run: (baseUrl: string) => Promise<void>) => {
    let server: Server | undefined
    await Effect.runPromise(Effect.scoped(Effect.gen(function* () {
      yield* Layer.build(makeServerLayer(dataDir, (created) => { server = created }))
      const address = server?.address()
      assert(address && typeof address !== "string")
      yield* Effect.promise(() => run(`http://127.0.0.1:${address.port}`))
    })))
  }

  try {
    let id = ""
    await start(async (baseUrl) => {
      const invalid = await fetch(`${baseUrl}/users`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ name: "" })
      })
      assert.equal(invalid.status, 400)

      const created = await fetch(`${baseUrl}/users`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ name: "Ada" })
      })
      assert.equal(created.status, 201)
      const user: { id: string; name: string } = await created.json()
      assert.equal(user.name, "Ada")
      id = user.id

      const found = await fetch(`${baseUrl}/users/${id}`)
      assert.equal(found.status, 200)
      assert.deepEqual(await found.json(), user)

      const missing = await fetch(`${baseUrl}/users/missing`)
      assert.equal(missing.status, 404)
    })

    await start(async (baseUrl) => {
      const found = await fetch(`${baseUrl}/users/${id}`)
      assert.equal(found.status, 200)
      assert.deepEqual(await found.json(), { id, name: "Ada" })
    })
  } finally {
    await rm(dataDir, { recursive: true, force: true })
  }
})
