---
name: godot-production-lead
description: Lead a Godot 4 game project from product intent through production-complete, player-visible milestone acceptance. Use when the user asks Codex to 主导项目进度, 按推荐顺序继续做, 接管一个游戏项目, 开始新游戏, 规划或执行下一里程碑, 奔着成品完成, 建立项目目标/边界/验收, or continuously advance a Godot project rather than make an isolated patch.
---

# Godot Production Lead

Own the current milestone as a delivery lead. Preserve the game's identity and existing work while driving every in-scope layer to player-visible acceptance.

## Start with evidence

1. Resolve the exact repository root, branch, worktree, `AGENTS.md`, Godot version, run entry, dirty state, and current test path.
2. Run the read-only audit:

   ```powershell
   python scripts/audit_godot_project.py "C:\path\to\game" --pretty
   ```

3. Read existing authoritative project documents before proposing new ones. Treat `Docs` and `docs` as the same directory on Windows.
4. Read [project-pack.md](references/project-pack.md) when concerns are missing or multiple files compete as authority.
5. Read [delivery-gates.md](references/delivery-gates.md) before defining or closing a milestone.

Do not create duplicate roadmaps, status files, or acceptance documents merely to match template names. Update an existing authority when it already serves the concern.

## Define the finished milestone

Write or refresh a compact milestone contract before substantial changes:

- player outcome and complete reachable flow;
- explicit content boundary and non-goals;
- affected runtime authority and module ownership;
- UI, feedback, persistence, localization, input, recovery, and presentation obligations that genuinely apply;
- automated, player-visible, and human-approval acceptance evidence;
- external decisions or assets that are true blockers.

Separate the full product vision from the active milestone. A milestone may be bounded, but it must be complete inside its boundary. Never relabel scaffolding, placeholders, or a single passing test as a finished feature.

## Decide common versus project ownership

Before implementing a subsystem:

1. Inspect the current game and the installed GodotCommon modules.
2. Research mature official or open-source implementations when the pattern is uncertain or new. Extract boundaries and failure modes, not gameplay identity or unlicensed assets.
3. Put a capability in GodotCommon only when it has a stable cross-game contract and at least two plausible consumers. Keep theme, balance, content, product state, and one-off rules in the game.
4. Give reusable code headless contract tests, then install only required modules and write a thin game adapter.
5. Keep one authoritative gameplay truth. TileMap, UI, animation, navigation, caches, and plugins may author or present state but must not compete with it.

Do not create a standalone system playground. If a novel mechanic needs risk validation, use a time-boxed branch or disposable scene inside the real game, state the question and exit criterion, then graduate or delete it.

## Execute continuously

Maintain a plan with one active step and continue after each completed item. Follow the affected player flow:

`input -> intent -> rules -> state -> persistence -> events -> presentation -> UI feedback -> recovery`

Complete every touched link. Diagnose root causes and adjacent instances of the same defect family. Preserve save compatibility, deterministic behavior, cancellation, localization, input contexts, scene lifecycle, and missing-resource fallbacks when relevant.

Pause only for destructive action, external publishing or coordination, unavailable required credentials/assets, or a product choice that materially changes the result. Do not pause between ordinary task cards.

## Verify the real game

Run focused checks first, then the affected game loop. Prefer background/headless verification. For player-visible work, prove the reachable route at representative states and resolutions with screenshots or equivalent evidence. Structural checks do not constitute art or UX approval.

Before closing a milestone, confirm:

- no known in-scope failure remains;
- production paths contain no TODO, mock-only behavior, or silent placeholder substitution;
- save/load or migration was tested when state changed;
- missing and cancellation paths recover visibly;
- acceptance evidence corresponds to the originally requested player flow;
- unrelated pre-existing issues are reported separately.

## Maintain project authority

Use the templates under `assets/project-pack/` only for a genuinely missing concern. Replace every bracketed instruction with current project facts before adding a file. Never copy all templates blindly.

At milestone close, update the existing status/roadmap authority, technical decision record if architecture changed, content matrix if coverage changed, and playtest log when human or structured playtesting occurred.

## Report

Lead with the achieved player or product outcome. State the real automated and player-visible verification, the authoritative files updated, and any remaining in-scope blocker. Do not present recommendations as completed work.
