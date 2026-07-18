#!/usr/bin/env python3
"""Audit a Godot directional character resource against a JSON manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


EXT_RESOURCE_RE = re.compile(
    r'^\[ext_resource\s+type="[^"]+"\s+path="([^"]+)"\s+id="([^"]+)"\]$'
)
SUB_RESOURCE_RE = re.compile(r'^\[sub_resource\s+type="[^"]+"\s+id="([^"]+)"\]$')
SCRIPT_RE = re.compile(r'^script\s*=\s*ExtResource\("([^"]+)"\)$')
STRING_NAME_RE = re.compile(r'^([A-Za-z0-9_]+)\s*=\s*&"([^"]*)"$')
RESOURCE_VALUE_RE = re.compile(r'^(texture|composite_texture)\s*=\s*ExtResource\("([^"]+)"\)$')

FACING_SCRIPT_SUFFIX = "paper_puppet_facing_def.gd"
PART_SCRIPT_SUFFIX = "paper_puppet_part_def.gd"
ACTION_SCRIPT_SUFFIX = "paper_puppet_action_def.gd"


@dataclass
class ResourceBlock:
    resource_id: str
    script_id: str = ""
    names: dict[str, str] = field(default_factory=dict)
    resources: dict[str, str] = field(default_factory=dict)


@dataclass
class ParsedPuppet:
    puppet_id: str
    facings: dict[str, ResourceBlock]
    facing_ids: list[str]
    parts: dict[str, list[ResourceBlock]]
    actions: list[str]
    ext_paths: dict[str, str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit directional Godot .tres character definitions against a manifest."
    )
    parser.add_argument("--manifest", required=True, type=Path, help="JSON manifest path")
    parser.add_argument(
        "--project-root",
        type=Path,
        help="Godot project root; overrides manifest project_root",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read manifest {path}: {exc}") from exc
    if payload.get("schema_version") != 1:
        raise ValueError("manifest schema_version must be 1")
    characters = payload.get("characters")
    if not isinstance(characters, list) or not characters:
        raise ValueError("manifest characters must be a non-empty array")
    return payload


def resolve_project_path(raw_path: str, project_root: Path) -> Path:
    if raw_path.startswith("res://"):
        return project_root / raw_path.removeprefix("res://")
    candidate = Path(raw_path)
    return candidate if candidate.is_absolute() else project_root / candidate


def parse_tres(path: Path) -> ParsedPuppet:
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except OSError as exc:
        raise ValueError(f"cannot read definition {path}: {exc}") from exc

    ext_paths: dict[str, str] = {}
    blocks: list[ResourceBlock] = []
    current: ResourceBlock | None = None
    root_names: dict[str, str] = {}

    for raw_line in lines:
        line = raw_line.strip()
        ext_match = EXT_RESOURCE_RE.match(line)
        if ext_match:
            ext_paths[ext_match.group(2)] = ext_match.group(1)
            current = None
            continue
        sub_match = SUB_RESOURCE_RE.match(line)
        if sub_match:
            current = ResourceBlock(resource_id=sub_match.group(1))
            blocks.append(current)
            continue
        if line.startswith("[resource]"):
            current = None
            continue
        script_match = SCRIPT_RE.match(line)
        if current is not None and script_match:
            current.script_id = script_match.group(1)
            continue
        name_match = STRING_NAME_RE.match(line)
        if name_match:
            target = current.names if current is not None else root_names
            target[name_match.group(1)] = name_match.group(2)
            continue
        resource_match = RESOURCE_VALUE_RE.match(line)
        if current is not None and resource_match:
            current.resources[resource_match.group(1)] = resource_match.group(2)

    def script_path(block: ResourceBlock) -> str:
        return ext_paths.get(block.script_id, "")

    facing_blocks = [b for b in blocks if script_path(b).endswith(FACING_SCRIPT_SUFFIX)]
    part_blocks = [b for b in blocks if script_path(b).endswith(PART_SCRIPT_SUFFIX)]
    action_blocks = [b for b in blocks if script_path(b).endswith(ACTION_SCRIPT_SUFFIX)]
    if not facing_blocks and not part_blocks and not action_blocks:
        raise ValueError(
            f"unsupported definition {path}: no recognized facing, part, or action subresources"
        )

    facings: dict[str, ResourceBlock] = {}
    facing_ids: list[str] = []
    for block in facing_blocks:
        facing_id = block.names.get("facing_id", "")
        if facing_id:
            facing_ids.append(facing_id)
        if facing_id and facing_id not in facings:
            facings[facing_id] = block

    parts: dict[str, list[ResourceBlock]] = {}
    for block in part_blocks:
        facing_id = block.names.get("facing_id", "")
        parts.setdefault(facing_id, []).append(block)

    actions = [
        block.names["action_id"]
        for block in action_blocks
        if block.names.get("action_id")
    ]
    return ParsedPuppet(
        puppet_id=root_names.get("puppet_id", ""),
        facings=facings,
        facing_ids=facing_ids,
        parts=parts,
        actions=actions,
        ext_paths=ext_paths,
    )


def texture_exists(ext_id: str, parsed: ParsedPuppet, project_root: Path) -> bool:
    raw_path = parsed.ext_paths.get(ext_id, "")
    if not raw_path:
        return False
    return resolve_project_path(raw_path, project_root).is_file()


def required_list(character: dict[str, Any], manifest: dict[str, Any], key: str) -> list[str]:
    value = character.get(key, manifest.get(key, []))
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{character.get('id', '<unknown>')} {key} must be an array of IDs")
    return value


def minimum_for_facing(character: dict[str, Any], facing_id: str) -> int:
    raw = character.get("min_parts_per_facing", 0)
    if isinstance(raw, int) and raw >= 0:
        return raw
    if isinstance(raw, dict):
        value = raw.get(facing_id, 0)
        if isinstance(value, int) and value >= 0:
            return value
    raise ValueError(
        f"{character.get('id', '<unknown>')} min_parts_per_facing must be a non-negative integer or facing map"
    )


def audit_character(
    character: dict[str, Any], manifest: dict[str, Any], project_root: Path
) -> dict[str, Any]:
    character_id = character.get("id")
    definition = character.get("definition")
    if not isinstance(character_id, str) or not character_id:
        raise ValueError("every character requires a non-empty id")
    if not isinstance(definition, str) or not definition:
        raise ValueError(f"{character_id} requires a definition path")

    definition_path = resolve_project_path(definition, project_root)
    parsed = parse_tres(definition_path)
    required_facings = required_list(character, manifest, "required_facings")
    required_actions = required_list(character, manifest, "required_actions")
    exact_by_facing = character.get("expected_parts_by_facing", {})
    if not isinstance(exact_by_facing, dict):
        raise ValueError(f"{character_id} expected_parts_by_facing must be an object")

    errors: list[str] = []
    warnings: list[str] = []
    if parsed.puppet_id != character_id:
        errors.append(f"definition puppet_id is '{parsed.puppet_id}', expected '{character_id}'")

    for facing_id in required_facings:
        facing_count = parsed.facing_ids.count(facing_id)
        if facing_count > 1:
            errors.append(f"facing '{facing_id}' is declared {facing_count} times")
        facing = parsed.facings.get(facing_id)
        if facing is None:
            errors.append(f"missing facing '{facing_id}'")
            continue
        composite_id = facing.resources.get("composite_texture", "")
        if composite_id and not texture_exists(composite_id, parsed, project_root):
            errors.append(f"facing '{facing_id}' has a missing composite texture")

        facing_parts = parsed.parts.get(facing_id, [])
        part_ids = [part.names.get("part_id", "") for part in facing_parts]
        duplicates = sorted({part_id for part_id in part_ids if part_id and part_ids.count(part_id) > 1})
        for part_id in duplicates:
            errors.append(f"facing '{facing_id}' has duplicate part '{part_id}'")
        known_parts = {part_id for part_id in part_ids if part_id}
        minimum = minimum_for_facing(character, facing_id)
        if len(known_parts) < minimum:
            errors.append(
                f"facing '{facing_id}' has {len(known_parts)} unique parts, requires at least {minimum}"
            )

        exact = exact_by_facing.get(facing_id)
        if exact is not None:
            if not isinstance(exact, list) or not all(isinstance(item, str) and item for item in exact):
                raise ValueError(f"{character_id} exact parts for {facing_id} must be an array of IDs")
            missing = sorted(set(exact) - known_parts)
            unexpected = sorted(known_parts - set(exact))
            if missing:
                errors.append(f"facing '{facing_id}' missing exact parts: {', '.join(missing)}")
            if unexpected:
                errors.append(f"facing '{facing_id}' has unexpected parts: {', '.join(unexpected)}")

        for part in facing_parts:
            part_id = part.names.get("part_id", "<empty>")
            parent_id = part.names.get("parent_part_id", "")
            if parent_id and parent_id not in known_parts:
                errors.append(
                    f"facing '{facing_id}' part '{part_id}' references missing parent '{parent_id}'"
                )
            texture_id = part.resources.get("texture", "")
            if not texture_id or not texture_exists(texture_id, parsed, project_root):
                errors.append(f"facing '{facing_id}' part '{part_id}' has a missing texture")

    for action_id in required_actions:
        count = parsed.actions.count(action_id)
        if count == 0:
            errors.append(f"missing action '{action_id}'")
        elif count > 1:
            errors.append(f"action '{action_id}' is declared {count} times")
    undeclared_actions = sorted(set(parsed.actions) - set(required_actions))
    if undeclared_actions:
        warnings.append(f"additional actions: {', '.join(undeclared_actions)}")

    return {
        "id": character_id,
        "definition": str(definition_path),
        "status": "PASS" if not errors else "FAIL",
        "facings": {key: len({p.names.get('part_id', '') for p in value if p.names.get('part_id')}) for key, value in parsed.parts.items()},
        "actions": parsed.actions,
        "errors": errors,
        "warnings": warnings,
    }


def render_text(results: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for result in results:
        lines.append(f"[{result['status']}] {result['id']}")
        facing_summary = ", ".join(
            f"{facing}={count}" for facing, count in sorted(result["facings"].items())
        )
        lines.append(f"  facings: {facing_summary or '<none>'}")
        lines.append(f"  actions: {', '.join(result['actions']) or '<none>'}")
        lines.extend(f"  ERROR: {message}" for message in result["errors"])
        lines.extend(f"  WARN: {message}" for message in result["warnings"])
    passed = sum(result["status"] == "PASS" for result in results)
    lines.append(f"SUMMARY: {passed} passed, {len(results) - passed} failed")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        manifest = load_manifest(args.manifest.resolve())
        root_value = args.project_root or manifest.get("project_root") or args.manifest.parent
        project_root = Path(root_value).resolve()
        results = [
            audit_character(character, manifest, project_root)
            for character in manifest["characters"]
        ]
    except (TypeError, ValueError) as exc:
        print(f"INPUT ERROR: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    else:
        print(render_text(results))
    return 0 if all(result["status"] == "PASS" for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
