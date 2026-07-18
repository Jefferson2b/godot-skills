# Tactical Presentation Contract

## Standard Stages

| Stage | Purpose | Allowed outputs |
| --- | --- | --- |
| `move` | Display a resolved path | visual position, facing, footsteps |
| `windup` | Establish intent and anticipation | pose, anticipation VFX/audio |
| `release` | Commit the visible attack or skill | weapon/projectile motion, cast cue |
| `contact` | Show an already-resolved hit/effect | hit VFX, hit audio, shake, numbers, target reaction |
| `recovery` | Return control/readability | recovery pose, effect cleanup |
| `down` | Show an already-resolved defeat | down pose, death cue, visibility transition |

Use stable project-specific stage IDs when an existing contract already exists. Map them to these semantics instead of renaming blindly.

## Required Outcome Branches

- Hit: include `contact` and target reaction.
- Miss/dodge: omit hit contact feedback; use miss/dodge cues.
- Zero damage/block: show contact only if physical contact occurred, with distinct blocked/no-damage feedback.
- Critical: use the same resolved damage, with stronger presentation only.
- Ranged: separate release/projectile travel from contact.
- Assist/redirect: make every resolved recipient visible at contact.
- Defeat: schedule `down` after the final applicable contact.

## Marker Rules

- Store markers as normalized time or named cue entries owned by presentation definitions.
- Prefer `anticipation`, `release`, `contact`, `recovery`, and `complete`.
- Trigger damage numbers, hit sound, hit VFX, target hit pose, and camera impact from the same resolved contact marker.
- Never call damage, status, occupancy, inventory, objective, or save APIs from a marker.

## Duration and Playback

- Choose one authoritative duration source per action.
- Scale stage advancement, poses, VFX, audio policy, and cleanup consistently for fast-forward.
- On skip, snap visual state to the resolved final state, clear transient nodes/cues, and emit presentation completion once.

## Acceptance Checklist

- Same resolved event batch selects the same branch and action IDs.
- Presentation cannot mutate battle state, command log, RNG, or save data.
- Miss produces no hit sound, damage number, hit shake, or target hit pose.
- Contact cues occur together and only after windup/release.
- Defeat occurs after the final contact.
- Direction/fallback behavior is explicit and stable.
- Playback speed preserves ordering.
- Skip leaves no stuck input lock, VFX, audio loop, or displaced visual.
- Headless tests pass and representative visible frames remain readable at supported UI scales.
