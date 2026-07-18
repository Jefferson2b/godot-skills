# Godot Skills

Reusable Codex skills for shipping and reviewing Godot game projects.

## Included skills

- `godot-production-lead` — drives a Godot project through production-complete, player-visible milestones.
- `godot-directional-character-pipeline` — builds and audits directional 2D character asset pipelines.
- `godot-tactical-combat-presentation` — implements deterministic tactical-combat animation and feedback.
- `github-game-architecture-study` — studies open-source game architecture without copying gameplay or assets.
- `visual-improve-review-build` — enforces an approve-the-ideal-visual-before-implementation workflow.

Each folder under `skills/` is self-contained and includes its `SKILL.md`, references, scripts, templates, and agent metadata where applicable.

## Install on another Windows PC

Install all skills into the current user's Codex profile:

```powershell
git clone https://github.com/Jefferson2b/godot-skills.git
cd godot-skills
.\install.ps1
```

Install selected skills:

```powershell
.\install.ps1 -Skill godot-production-lead,godot-directional-character-pipeline
```

Existing skill folders are protected by default. Pass `-Force` only when you intentionally want to replace the installed copies:

```powershell
.\install.ps1 -Force
```

Restart Codex after installation so the new skills are discovered.

## Manual installation

Copy any complete folder from `skills/` into `%USERPROFILE%\.codex\skills\`. Keep the folder structure intact because skills may reference their bundled `scripts/`, `references/`, or `assets/` paths.

## Requirements

- Codex with local skill support.
- Godot 4 for Godot project workflows.
- Python 3 for the audit scripts included with `godot-production-lead` and `godot-directional-character-pipeline`.
- GitHub CLI and the `agent-reach` skill for live GitHub research performed by `github-game-architecture-study`.
