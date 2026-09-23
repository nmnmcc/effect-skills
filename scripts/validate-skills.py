#!/usr/bin/env python3
"""Check Agent Skills packaging; content accuracy still requires human review."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED = {"name", "description"}
LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def check_skill(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if not content.startswith("---\n") or "\n---\n" not in content[4:]:
        return [f"{path}: missing YAML frontmatter"]

    header, body = content[4:].split("\n---\n", 1)
    fields: dict[str, str] = {}
    for line in header.splitlines():
        if ":" not in line:
            errors.append(f"{path}: malformed frontmatter line")
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in fields:
            errors.append(f"{path}: duplicate frontmatter field {key}")
        fields[key] = value

    for key in sorted(fields.keys() - ALLOWED):
        errors.append(f"{path}: unsupported frontmatter field {key}")
    name = fields.get("name", "")
    if name != path.parent.name or len(name) > 64 or not NAME.fullmatch(name):
        errors.append(f"{path}: invalid name or directory mismatch")
    description = fields.get("description", "")
    if description.startswith('"'):
        try:
            description = json.loads(description)
        except json.JSONDecodeError:
            errors.append(f"{path}: invalid quoted description")
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        errors.append(f"{path}: description must be 1-1024 characters")
    if not body.strip():
        errors.append(f"{path}: empty skill body")

    for target in LINK.findall(body):
        if "://" not in target and not target.startswith("#"):
            local = (path.parent / target.split("#", 1)[0]).resolve()
            if not local.is_file():
                errors.append(f"{path}: missing local reference {target}")
    return errors


def main() -> int:
    skills_root = ROOT / "skills"
    files = sorted(skills_root.glob("*/SKILL.md"))
    errors: list[str] = []
    if not files:
        errors.append("No skills/<name>/SKILL.md files found")
    for path in files:
        errors.extend(check_skill(path))
    for directory in skills_root.iterdir():
        if directory.is_dir() and not (directory / "SKILL.md").is_file():
            errors.append(f"{directory}: missing SKILL.md")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Validated packaging for {len(files)} hand-written skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
