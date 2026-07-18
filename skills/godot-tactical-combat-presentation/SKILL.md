---
name: godot-tactical-combat-presentation
description: Design, implement, audit, and verify deterministic tactical-combat presentation in Godot, including map movement, attack windup, release/contact/recovery timing, hit and miss feedback, criticals, dodges, assists, defeat, paper-puppet or sprite animation, VFX, audio, camera shake, damage numbers, playback speed, and skipping. Use for requests such as 战棋动画, 火纹式演出, 攻击或技能演出, 命中反馈不同步, 受击/闪避/暴击动画, combat timeline, AnimationPlayer/AnimationTree choreography, or when presentation must consume resolved gameplay events without changing battle rules.
---

# Godot Tactical Combat Presentation

Build tactical-combat animation as a deterministic projection of already-resolved gameplay. Keep rules authoritative and presentation interruptible, testable, and replaceable.

## Coordinate With Other Skills

- Use `godot-directional-character-pipeline` as well when producing or auditing directional sprites, cutout parts, pivots, anchors, parent chains, or action matrices.
- Use `visual-improve-review-build` as well when redesigning player-visible art or establishing a new visual target; obtain its required approval before changing official visual assets or implementation.
- Do not invoke either skill merely for a timing-only or architecture-only change.

## Workflow

1. Read the repository instructions and authoritative design/architecture/QA documents. Confirm the repository root, engine version, current milestone, dirty state, and explicit no-touch boundaries.
2. Classify the request as audit, choreography design, implementation, asset production, or verification. Do not implement when the user only requested analysis or diagnosis.
3. Trace the complete state flow before editing:

   `command -> resolved rule events -> presentation queue -> action selection -> sampled pose/VFX/audio -> completion`

4. Prove that gameplay outcome, RNG, HP, position, occupancy, status, costs, and objectives are settled outside animation nodes and callbacks. Treat any presentation-to-rules mutation as an architecture defect.
5. Define or update a choreography contract before changing code. Specify outcome branch, stages, markers, action IDs, cue IDs, duration source, fallback, speed behavior, and skip behavior. Read [presentation-contract.md](references/presentation-contract.md) for the contract and acceptance checklist.
6. Implement the smallest coherent slice. Prefer typed GDScript, stable `StringName` IDs, immutable definition resources, copied event payloads, and explicit presentation APIs.
7. Keep `AnimationPlayer`, `AnimationTree`, tweens, paper-puppet evaluators, shaders, particles, audio, camera shake, and floating text inside presentation. Method tracks may emit presentation cues but must never apply combat rules.
8. Derive facing and visual movement from resolved positions or paths. Never let interpolated transforms become the source of logical grid position.
9. Make miss, zero-damage, critical, dodge, assist, push, heal, status, and defeat branches explicit. A miss must not reuse contact feedback; a skipped animation must still reach a clean final visual state without replaying rules.
10. Add focused regression tests for event ordering, branch selection, cue timing, fallback, presentation purity, speed, and skip. Run the repository test entry point, relevant scene smoke tests, and background or hidden-window visual captures when layout or timing is player-visible.
11. Report changed files, tests, manual/visual checks, limitations, and the exact next backlog task required by the repository.

## Guardrails

- Do not recompute hit, damage, targets, assists, or status outcomes in presentation.
- Do not use animation completion as authority for rules or saves.
- Do not introduce nondeterministic gameplay RNG through visual variation. Keep cosmetic variation isolated and seedable when reproducible capture matters.
- Do not copy copyrighted franchise assets or animation frames. Reproduce only general timing and composition principles with original assets.
- Do not add a separate Fire Emblem-style battle screen unless the user authorizes that scope and the production cost is evaluated against the current milestone.
- Preserve fast-forward, skip, headless tests, and scene loading.

## Expected Output

For audits and design requests, provide the current flow, concrete defects, proposed contract, adoption order, and risks. For implementation requests, complete the authorized slice and provide fresh test and visual evidence.
