# Visual QA Checklist

Use real in-engine rendering. A source PNG or editor preview is insufficient.

## Matrix coverage

- Capture every required facing at idle.
- Capture every required action at a representative keyframe.
- Check start and end frames for one-shot actions.
- Check loop seams for idle and movement.
- Exercise fallback behavior only when the contract intentionally permits it.

## Registration and hierarchy

- Keep the foot anchor on the intended ground point and inside the occupied cell.
- Confirm pivots rotate at joints instead of sliding limbs.
- Confirm parent chains keep hands, weapons, hair, coats, and accessories attached.
- Confirm draw order is correct for near/far limbs and front/back weapons.
- Confirm root motion does not move the logical unit or persist after the presentation ends.

## Readability

- Preserve the character silhouette at gameplay zoom.
- Make facing and weapon direction readable without relying only on color.
- Avoid accidental mirroring of asymmetric weapons, clothing, scars, text, or equipment.
- Check overlap against terrain, objectives, effects, dialogue, HUD, and other units.
- Check hit, down, and skill poses under the darkest representative map lighting.

## Viewports and evidence

- Use the project's primary desktop resolution.
- Check every supported UI scale or at least the declared minimum and maximum.
- Prefer background or hidden-window captures when the repository supports them.
- Store only current acceptance evidence; do not promote stale captures after asset changes.
- Record exact commands, scene, character, facing, action, time/keyframe, resolution, and scale.

## Acceptance boundary

Static audit PASS means the declared data matrix is complete. Visual acceptance additionally requires in-engine review, provenance approval, and no regression in the repository's automated tests. Report these states separately.
