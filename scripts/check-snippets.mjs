import { mkdir, readFile, readdir, writeFile } from "node:fs/promises"
import { spawnSync } from "node:child_process"
import path from "node:path"
import { fileURLToPath } from "node:url"
import MarkdownIt from "markdown-it"

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..")
const output = path.join(root, ".cache", "snippets")
const markdown = new MarkdownIt()
const folders = (await readdir(path.join(root, "skills"), { withFileTypes: true }))
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .sort()
const files = []

await mkdir(output, { recursive: true })
for (const folder of folders) {
  const source = await readFile(path.join(root, "skills", folder, "SKILL.md"), "utf8")
  const snippets = markdown.parse(source, {}).filter((token) =>
    token.type === "fence" && /^(ts|tsx)(\s|$)/.test(token.info)
  )
  if (snippets.length === 0) {
    throw new Error(`${folder} must contain a TypeScript example`)
  }
  for (const [index, snippet] of snippets.entries()) {
    const file = path.join(output, `${folder}-${index + 1}.${snippet.info.startsWith("tsx") ? "tsx" : "ts"}`)
    await writeFile(file, snippet.content)
    files.push(file)
  }
}

const config = path.join(output, "tsconfig.json")
await writeFile(config, JSON.stringify({
  extends: "../../tsconfig.json",
  files: [
    ...files.map((file) => path.basename(file)),
    "../../examples/user-api.ts",
    "../../examples/user-api.test.ts"
  ],
  include: []
}))
const check = spawnSync(path.join(root, "node_modules", ".bin", "tsc"), ["--project", config], {
  cwd: root,
  stdio: "inherit"
})
if (check.error) throw check.error
if (check.status !== 0) {
  process.exitCode = check.status || 1
} else {
  console.log(`Typechecked ${files.length} snippets across ${folders.length} skills and the end-to-end example`)
}
