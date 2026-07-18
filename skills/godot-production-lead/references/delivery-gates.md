# Production delivery gates

## Gate 0: identity and scope

- Exact repository, branch/worktree, Godot version, and current run entry are known.
- Core player promise and active milestone boundary are explicit.
- Non-goals prevent unrelated refactors and feature expansion.

## Gate 1: risk and ownership

- The largest product and technical uncertainties are named.
- Existing project and mature external implementations were inspected where appropriate.
- GodotCommon versus game ownership is decided.
- Any risk spike has one question, an exit criterion, and a deletion or graduation path inside the real project.

## Gate 2: complete implementation

- The reachable player flow works end to end.
- Applicable domain, state, UI, feedback, save, localization, input, presentation, and recovery layers are complete.
- Production paths contain no mock-only branch, TODO, or hidden debug requirement.

## Gate 3: automated proof

- Shared contracts and game-specific regression tests pass.
- The original player route is exercised, not only direct methods.
- Save compatibility, deterministic replay, invalid input, cancellation, and missing resources are covered when affected.

## Gate 4: player-visible proof

- The real scene is reachable and responsive.
- Representative states and resolutions were captured or observed.
- Text, controls, consequences, and recovery are visible to the player.
- Human-only judgments remain explicitly pending until reviewed.

## Gate 5: closeout

- Active milestone and content coverage authorities reflect reality.
- Architectural decisions and migrations are recorded when changed.
- Known unrelated issues are separated from in-scope gaps.
- No known in-scope failure remains.

Do not advance a gate because the token budget is low or because implementation is difficult. A blocked gate must name the exact external decision, asset, credential, or destructive permission required.
