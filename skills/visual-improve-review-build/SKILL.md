---
name: visual-improve-review-build
description: Improve player-visible art through a mandatory discuss, ideal-visual review, and approved implementation workflow. Use for art optimization, image improvement or replacement, visual redesign, UI/UX styling, icons, effects, scene composition, existing-screen rework, or building a new visual experience from scratch. Trigger when Codex is asked to make visuals better and should show one ideal target image for approval before changing official assets, code, scenes, components, or project implementation.
---

# Visual Improve Review Build

Use three strict phases: align on the visual goal, present one ideal visual, then implement only after approval.

## Non-negotiable gate

Do not modify official assets, project files, scenes, components, UI, UX, gameplay logic, or implementation while the ideal visual is unapproved.

Treat `我同意`, `同意`, `OK`, `ok`, `继续执行`, and equally explicit wording as implementation approval only when the user says it after a specific ideal-visual version has been shown. During the discussion phase, the same wording confirms only the current decision.

If approval is absent or ambiguous, remain in review. If approval covers only part of the visual, implement only that part.

## Phase 1: Inspect and align

1. Inspect supplied images and relevant project files before asking questions. Find facts from the environment instead of asking the user.
2. Treat an existing screen or image as evidence of the current state, reusable material, and possible shortcomings. Do not force it to be the base composition. Design from the latest agreed direction.
3. Ask only decisions that materially affect the result. Ask one question at a time and include a recommended answer.
4. Resolve important branches such as purpose, audience, mood, art direction, composition, color, information hierarchy, interaction states, target format, and technical constraints. Skip irrelevant branches.
5. Avoid endless interrogation. Stop when the remaining uncertainty would not materially change the ideal visual.
6. Summarize the resolved direction and obtain confirmation of shared understanding unless the user's latest message already clearly confirms the complete direction.

Do not create or edit the official implementation in this phase. Read-only inspection and temporary analysis artifacts are allowed.

## Phase 2: Produce the ideal visual

1. Create a fresh ideal visual from the latest discussion. Existing visuals are references, not mandatory edit bases.
2. Default to exactly one recommended version per review round. Produce multiple directions only when the user explicitly requests them.
3. Make the visual as close as practical to the intended final experience: target aspect ratio, composition, color system, scale, hierarchy, representative content, and relevant UI states.
4. Support blank-slate work. The project need not already contain a screen, running scene, component system, or finished assets.
5. Use the appropriate image or design capability. For raster concept generation or editing, use the available image-generation workflow; for a user-owned canvas, use its canvas workflow; for code-native visuals, still present a reviewable ideal rendering before official implementation.
6. Keep the concept technically credible for the target project. Identify any intentionally aspirational element that may require a substitute.
7. Label the proposal as a distinct version and preserve the exact approved artifact or conversation reference as the implementation baseline.
8. Present the visual with a short note covering current shortcomings, the proposed improvement, and the intended visible outcome. Do not substitute a mood board, prose-only description, or loose references for the ideal visual.

Stop and wait for approval. Requested revisions create a new ideal-visual version and return to review; they do not authorize implementation.

## Phase 3: Implement after approval

After approval, begin implementation directly. Do not pause to restate the modification scope or request a second execution confirmation.

1. Build or modify the required assets, components, UX/UI, scenes, effects, code, and supporting systems to realize the approved visual.
2. Permit gameplay-logic or structural changes when they serve the approved result. Keep unrelated changes out of scope.
3. Use the approved visual as a flexible target, not a pixel-locked contract.
4. Allow small implementation-led refinements without renewed approval. Record them for the final report.
5. Require renewed permission or a new ideal visual before changing major visual decisions, including the color system, subject proportions, canvas or screen ratio, core composition, or primary visual hierarchy.
6. Record new ideas discovered during implementation. Do not expand the current result with major unapproved ideas; report them at the end.
7. Preserve user work and follow normal safety boundaries for destructive actions, external publication, credentials, and systems outside the placed-in-scope project.

## Verify and deliver

Verify the finished result against the approved ideal visual using the strongest evidence the project supports. Acceptable evidence includes a final running screen, component preview, scene capture, render, assembled asset view, or equivalent final-state artifact.

Do not require a pre-existing runtime screen before concept work. For blank-slate tasks, create the ideal visual first, build the experience, and capture the final state afterward.

Before declaring completion:

- Compare the final state with the approved version.
- Correct material regressions instead of merely reporting completion.
- Report what was implemented, small deviations, unresolved items, and recorded new ideas.
- Call out any major mismatch that still needs a new approval cycle.
