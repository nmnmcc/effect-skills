# Contributing

Enter the pinned development environment before making changes:

```sh
direnv allow
devenv test
```

`devenv shell` is the manual alternative when direnv is not enabled.

Keep one skill per related area of Effect, not one skill per exported module.
These are hand-written instructions for agent decisions, not a generated API
catalogue.

When changing a skill:

1. Check the project's pinned Effect version and the corresponding source
   before recommending an import or example. Document v4-only or unstable
   behavior explicitly.
2. Make the frontmatter description a short, specific trigger: what the skill
   helps with and when it applies. The name must match the directory.
3. Give the agent useful choices and boundaries (errors, resources,
   cancellation, compatibility). Link official API/source pages for details
   that might change.
4. Verify executable examples against the version they claim to support.
   Clearly label conceptual snippets that cannot stand alone.
5. Run python3 scripts/validate-skills.py and the bundled Agent Skills
   validator if available. Review the result by hand: structural validation
   alone does not prove guidance is correct.

Use skills/<area>/SKILL.md for the entrypoint. Put substantial guidance needed
only by a subset of requests in references/ and link it from the entrypoint;
avoid copying the upstream manual.
