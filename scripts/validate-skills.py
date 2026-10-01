#!/usr/bin/env python3
"""Validate Agent Skills packaging and repository Markdown references."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

import yaml
from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EFFECT_VERSION = "4.0.0"
EFFECT_TAG = "effect%40" + EFFECT_VERSION
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
LEGACY_IMPORT = re.compile(
    r"(?<![@/\w])effect/(?:unstable(?:/[a-z-]+)*|httpapi|Encoding|arbitrary(?:/[a-z-]+)*)\b"
)


class StrictLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader: StrictLoader, node: yaml.MappingNode) -> dict:
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in mapping:
            raise yaml.constructor.ConstructorError(None, None, f"duplicate YAML key: {key}", key_node.start_mark)
        mapping[key] = loader.construct_object(value_node)
    return mapping


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
MARKDOWN = MarkdownIt("commonmark")


def check_skill(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n") or "\n---\n" not in content[4:]:
        return [f"{path}: missing YAML frontmatter"]
    header, body = content[4:].split("\n---\n", 1)
    try:
        fields = yaml.load(header, Loader=StrictLoader)
    except yaml.YAMLError as error:
        return [f"{path}: invalid YAML: {error}"]
    if not isinstance(fields, dict):
        return [f"{path}: frontmatter must be a mapping"]

    errors = [f"{path}: unsupported frontmatter field {key}" for key in fields.keys() - FIELDS]
    name = fields.get("name")
    if not isinstance(name, str) or name != path.parent.name or not 1 <= len(name) <= 64 or not NAME.fullmatch(name):
        errors.append(f"{path}: invalid name or directory mismatch")
    description = fields.get("description")
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        errors.append(f"{path}: description must be 1-1024 characters")
    compatibility = fields.get("compatibility")
    if compatibility is not None and (not isinstance(compatibility, str) or not 1 <= len(compatibility) <= 500):
        errors.append(f"{path}: compatibility must be 1-500 characters")
    metadata = fields.get("metadata")
    if metadata is not None and (not isinstance(metadata, dict) or any(
        not isinstance(key, str) or not isinstance(value, str) for key, value in metadata.items()
    )):
        errors.append(f"{path}: metadata must map strings to strings")
    for key in ("license", "allowed-tools"):
        if key in fields and (not isinstance(fields[key], str) or not fields[key]):
            errors.append(f"{path}: {key} must be a nonempty string")
    if not body.strip():
        errors.append(f"{path}: empty skill body")
    if LEGACY_IMPORT.search(body):
        errors.append(f"{path}: uses an import path not exported by {EFFECT_VERSION}")
    if "github.com/Effect-TS/effect/" not in body or f"{EFFECT_TAG}/" not in body:
        errors.append(f"{path}: missing pinned upstream source link")
    return errors


def check_links(path: Path, external: set[str]) -> list[str]:
    errors = []
    tokens = MARKDOWN.parse(path.read_text(encoding="utf-8"))
    targets = (
        token.attrGet("href" if token.type == "link_open" else "src")
        for top in tokens for token in (top, *(top.children or []))
        if token.type in ("link_open", "image")
    )
    for target in targets:
        if target is None:
            continue
        parsed = urlsplit(target)
        if parsed.scheme in ("http", "https"):
            external.add(target)
            continue
        if parsed.scheme or target.startswith("//"):
            errors.append(f"{path}: unsupported link {target}")
            continue
        if not parsed.path:
            continue
        local = (path.parent / unquote(parsed.path)).resolve()
        if not local.is_file():
            errors.append(f"{path}: missing local reference {target}")
        if SKILLS in path.parents and SKILLS / path.relative_to(SKILLS).parts[0] not in local.parents:
            errors.append(f"{path}: reference escapes independently installed skill: {target}")
    return errors


def check_external(url: str) -> str | None:
    for method in ("HEAD", "GET"):
        try:
            with urlopen(Request(url, method=method, headers={"User-Agent": "effect-skills-validator"}), timeout=15) as response:
                if response.status < 400:
                    return None
        except HTTPError as error:
            if method == "HEAD" and error.code in (403, 405):
                continue
            return f"{url}: HTTP {error.code}"
        except URLError as error:
            return f"{url}: {error.reason}"
    return f"{url}: inaccessible"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--external", action="store_true", help="also check source links over the network")
    args = parser.parse_args()
    files = sorted(SKILLS.glob("*/SKILL.md"))
    errors = []
    external: set[str] = set()
    if not files:
        errors.append("No skills/<name>/SKILL.md files found")
    for path in files:
        errors.extend(check_skill(path))
    for directory in SKILLS.iterdir():
        if directory.is_dir() and not (directory / "SKILL.md").is_file():
            errors.append(f"{directory}: missing SKILL.md")
    markdown_files = [ROOT / "README.md", ROOT / "CONTRIBUTING.md", *sorted((ROOT / "docs").glob("*.md"))]
    for directory in SKILLS.iterdir():
        if directory.is_dir():
            markdown_files.extend(directory.rglob("*.md"))
    for path in markdown_files:
        errors.extend(check_links(path, external))
    if args.external:
        for url in sorted(external):
            error = check_external(url)
            if error:
                errors.append(error)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {len(files)} skills, local references, and {len(external)} source URLs"
          + (" (fetched)" if args.external else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
