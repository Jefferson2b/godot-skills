#!/usr/bin/env python3
"""Read-only Godot project delivery audit."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


CONCERNS = {
    "product_brief": (
        "product_brief.md", "gdd.md", "game_design_document.md",
        "demo_vertical_slice.md", "readme.md",
    ),
    "milestones": (
        "milestones.md", "roadmap.md", "implementation_status.md",
        "current_tasks.md", "refactor_progress.md",
    ),
    "acceptance": (
        "acceptance.md", "pre_playtest_quality_bar.md", "playtest_checklist.md",
        "release_checklist.md", "demo_vertical_slice.md",
    ),
    "technical_decisions": (
        "technical_decisions.md", "decisions.md", "architecture.md",
        "technical_decisions_log.md",
    ),
    "content_coverage": (
        "content_matrix.md", "implementation_status.md", "asset_scope.md",
        "content_manifest.md",
    ),
    "playtest_record": (
        "playtest_log.md", "playtest_plan.md", "playtest_checklist.md",
        "playtest_results.md",
    ),
}


def run_git(root: Path, *args: str) -> tuple[int, str]:
    process = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return process.returncode, process.stdout.strip()


def read_project_config(project_file: Path) -> dict[str, object]:
    text = project_file.read_text(encoding="utf-8-sig", errors="replace")
    section = ""
    values: dict[tuple[str, str], str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";") or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[(section, key.strip())] = value.strip()

    def clean(value: object) -> object:
        if not isinstance(value, str):
            return value
        if len(value) >= 2 and value[0] == value[-1] == '"':
            return value[1:-1]
        return value

    return {
        "config_version": clean(values.get(("", "config_version"))),
        "name": clean(values.get(("application", "config/name"))),
        "run_main_scene": clean(values.get(("application", "run/main_scene"))),
        "features": clean(values.get(("application", "config/features"))),
    }


def collect_markdown(root: Path) -> list[Path]:
    files: list[Path] = []
    for child in root.iterdir():
        if child.is_file() and child.suffix.lower() == ".md":
            files.append(child)
        elif child.is_dir() and child.name.lower() == "docs":
            files.extend(path for path in child.rglob("*.md") if path.is_file())
    return sorted(set(files), key=lambda path: str(path).lower())


def concern_candidates(root: Path, markdown: list[Path]) -> dict[str, object]:
    result: dict[str, object] = {}
    for concern, exact_names in CONCERNS.items():
        candidates: list[Path] = []
        for path in markdown:
            name = path.name.lower()
            stem = path.stem.lower()
            exact = name in exact_names
            semantic = (
                (concern == "acceptance" and (
                    "acceptance" in stem
                    or "quality_bar" in stem
                    or "rc_checklist" in stem
                    or "complete_contract" in stem
                    or stem in {"playtest_plan", "smoke_test_plan"}
                ))
                or (concern == "milestones" and "milestone" in stem)
                or (concern == "technical_decisions" and ("decision" in stem or "architecture" in stem))
                or (concern == "content_coverage" and (
                    "asset_scope" in stem
                    or "implementation_status" in stem
                    or ("content" in stem and ("matrix" in stem or "manifest" in stem or "scope" in stem))
                ))
                or (concern == "playtest_record" and "playtest" in stem)
            )
            if exact or semantic:
                candidates.append(path)
        relative = [path.relative_to(root).as_posix() for path in candidates]
        result[concern] = {
            "status": "missing" if not relative else "present" if len(relative) == 1 else "multiple_candidates",
            "candidates": relative,
        }
    return result


def audit(root: Path) -> dict[str, object]:
    root = root.resolve()
    project_file = root / "project.godot"
    if not project_file.is_file():
        raise ValueError(f"Not a Godot project: {root}")

    markdown = collect_markdown(root)
    return_code, git_root = run_git(root, "rev-parse", "--show-toplevel")
    git: dict[str, object] = {"available": return_code == 0}
    if return_code == 0:
        _, branch = run_git(root, "branch", "--show-current")
        _, head = run_git(root, "rev-parse", "--short", "HEAD")
        _, status = run_git(root, "status", "--porcelain")
        changes = status.splitlines() if status else []
        git.update({
            "root": git_root,
            "branch": branch or None,
            "head": head or None,
            "dirty": bool(changes),
            "change_count": len(changes),
        })

    install_record_path = root / "addons" / "jq_common" / ".jq-common-install.json"
    install_record: object = None
    if install_record_path.is_file():
        try:
            install_record = json.loads(install_record_path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as error:
            install_record = {"invalid": str(error)}

    concerns = concern_candidates(root, markdown)
    risks: list[str] = []
    if not (root / "AGENTS.md").is_file():
        risks.append("missing_root_agents")
    if git.get("dirty"):
        risks.append("dirty_worktree")
    if not any(root.rglob("test*.gd")):
        risks.append("no_godot_tests_detected")
    for concern, value in concerns.items():
        if value["status"] == "missing":
            risks.append(f"missing_authority:{concern}")

    return {
        "project_root": str(root),
        "project": read_project_config(project_file),
        "git": git,
        "root_agents": (root / "AGENTS.md").is_file(),
        "markdown_count": len(markdown),
        "authorities": concerns,
        "jq_common_install": install_record,
        "godot_ai_present": (root / "addons" / "godot_ai" / "plugin.cfg").is_file(),
        "godot_test_count": sum(1 for _ in root.rglob("test*.gd")),
        "risks": risks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    try:
        result = audit(args.project_root)
    except (OSError, ValueError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
