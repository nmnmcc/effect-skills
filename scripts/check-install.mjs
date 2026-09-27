import assert from "node:assert/strict"
import { spawnSync } from "node:child_process"
import { existsSync } from "node:fs"
import { mkdtemp, readFile, readdir, rm, writeFile } from "node:fs/promises"
import { tmpdir } from "node:os"
import path from "node:path"
import { fileURLToPath } from "node:url"
import MarkdownIt from "markdown-it"

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..")
const cli = path.join(root, "node_modules", ".bin", "skills")
const markdown = new MarkdownIt()
const rootNames = (await readdir(path.join(root, "skills"), { withFileTypes: true }))
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .sort()

function run(cwd, args) {
  const result = spawnSync(cli, ["add", root, ...args], {
    cwd,
    encoding: "utf8",
    env: { ...process.env, CI: "1", DISABLE_TELEMETRY: "1" }
  })
  if (result.error) throw result.error
  assert.equal(result.status, 0, `${args.join(" ")}\n${result.stdout}\n${result.stderr}`)
  return result.stdout
}

async function assertInstalled(cwd, requested) {
  const installedRoot = path.join(cwd, ".agents", "skills")
  const actual = (await readdir(installedRoot)).sort()
  assert.deepEqual(actual, [...requested].sort())
  for (const name of requested) {
    const skillDir = path.join(installedRoot, name)
    const skill = path.join(skillDir, "SKILL.md")
    assert(existsSync(skill), `${name} was not installed`)
    const tokens = markdown.parse(await readFile(skill, "utf8"), {})
    for (const token of tokens) {
      for (const child of token.children ?? []) {
        if (child.type !== "link_open") continue
        const href = child.attrGet("href")
        if (!href || /^(https?:|#)/.test(href)) continue
        const resolved = path.resolve(skillDir, decodeURIComponent(href.split("#")[0]))
        assert(resolved.startsWith(skillDir + path.sep) && existsSync(resolved), `${name}: unavailable reference ${href}`)
      }
    }
  }
}

async function inProject(test) {
  const project = await mkdtemp(path.join(tmpdir(), "effect-skills-install-"))
  try {
    await writeFile(path.join(project, "package.json"), '{"name":"skills-install-check","private":true}')
    await test(project)
  } finally {
    await rm(project, { recursive: true, force: true })
  }
}

await inProject(async (project) => {
  const listed = run(project, ["--list"])
  for (const name of rootNames) assert(listed.includes(name), `missing from --list: ${name}`)
  assert(!listed.includes("effect-durable-systems") && !listed.includes("effect-cli-tools"))
  run(project, ["--skill", "effect-cluster", "--agent", "codex", "--copy", "-y"])
  await assertInstalled(project, ["effect-cluster"])
})

await inProject(async (project) => {
  const requested = ["effect-core", "effect-schema", "effect-http-api"]
  run(project, ["--skill", ...requested, "--agent", "codex", "--copy", "-y"])
  await assertInstalled(project, requested)
})

console.log(`Verified local discovery and isolated single/multiple installs for ${rootNames.length} available skills`)
