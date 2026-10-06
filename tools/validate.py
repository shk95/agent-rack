#!/usr/bin/env python3
"""Validate the collection's distribution contract without third-party modules."""

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def contained(base, value):
    require(not Path(value).is_absolute(), f"Absolute package path: {value}")
    path = (base / value).resolve()
    require(path.is_relative_to(base.resolve()), f"Escaping package path: {value}")
    require(path.exists(), f"Missing package path: {path}")
    return path


def main():
    marketplace = read_json(ROOT / ".agents/plugins/marketplace.json")
    require(marketplace["name"] == "agent-rack", "Wrong marketplace identity")
    require(marketplace["interface"]["displayName"], "Missing marketplace display name")
    claude = read_json(ROOT / ".claude-plugin/marketplace.json")
    require(claude["name"] == marketplace["name"], "Marketplace identity drift")
    require(claude["owner"]["name"], "Missing Claude marketplace owner")
    require(len({p["name"] for p in claude["plugins"]}) == len(claude["plugins"]), "Duplicate Claude entries")
    claude_sources = {p["name"]: p["source"] for p in claude["plugins"]}
    names = set()
    count = 0
    for entry in marketplace["plugins"]:
        name = entry["name"]
        require(name not in names, f"Duplicate marketplace entry: {name}")
        names.add(name)
        require(entry["source"]["source"] == "local", f"Unexpected source type: {name}")
        require(entry["policy"]["installation"] == "AVAILABLE", f"Unexpected install policy: {name}")
        require(entry["policy"]["authentication"] == "ON_INSTALL", f"Unexpected auth policy: {name}")
        require(entry["category"], f"Missing category: {name}")
        package = contained(ROOT, entry["source"]["path"])
        require(claude_sources.get(name) == entry["source"]["path"], f"Claude source drift: {name}")
        require(package == ROOT / "plugins" / name, f"Unexpected source: {name}")
        manifest = read_json(package / "plugin.json")
        require(manifest["name"] == name, f"Manifest name mismatch: {name}")
        require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name), f"Invalid name: {name}")
        require(re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]), f"Invalid version: {name}")
        require(manifest["description"].strip(), f"Empty description: {name}")
        interface = manifest["extensions"]["com.openai"]["interface"]
        require(len(interface["shortDescription"]) <= 30, f"Subtitle too long: {name}")
        for host in ("claude", "codex"):
            adapter = read_json(package / f".{host}-plugin/plugin.json")
            for field in ("name", "version", "description", "author", "license"):
                require(adapter[field] == manifest[field], f"Adapter drift: {name}/{host}/{field}")
            if host == "codex":
                require(adapter["interface"] == interface, f"Interface drift: {name}")
                require(contained(package, adapter["skills"]) == package / "skills", f"Skill path drift: {name}")
        require((package / "LICENSE").is_file(), f"Missing license: {name}")
        skills = sorted((package / "skills").glob("*/SKILL.md"))
        require(skills, f"No skills in {name}")
        for skill in skills:
            text = skill.read_text(encoding="utf-8")
            parts = text.split("---", 2)
            require(len(parts) == 3 and not parts[0], f"Missing frontmatter: {skill}")
            fields = dict(re.findall(r"^(name|description): (.+)$", parts[1], re.M))
            require(fields.get("name") == skill.parent.name, f"Skill name mismatch: {skill}")
            require(fields.get("description", "").strip(), f"Missing skill description: {skill}")
            require(parts[2].strip(), f"Empty instructions: {skill}")
            count += 1
        for path in package.rglob("*"):
            require(not path.is_symlink(), f"Distribution symlink: {path}")
            require(path.name not in {".env", ".DS_Store"}, f"Local state in package: {path}")
    actual = {p.name for p in (ROOT / "plugins").glob("*") if p.is_dir()}
    require(actual == names, "Marketplace does not match plugin directories")
    require(set(claude_sources) == names, "Claude marketplace differs from Codex")
    for document in ROOT.rglob("*.md"):
        if "imports" in document.relative_to(ROOT).parts:
            continue  # Original references belong to the source repository.
        for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            contained(ROOT, str(document.parent.relative_to(ROOT) / target.split("#")[0]))
    print(f"Validated {len(names)} plugins and {count} skills (structural checks only).")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        sys.exit(1)
