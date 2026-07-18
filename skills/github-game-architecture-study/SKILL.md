---
name: github-game-architecture-study
description: Research and evaluate GitHub game repositories to extract transferable architecture without copying gameplay or assets. Use when the user shares or names a GitHub game repo, asks whether an open-source game fits their project, requests examples of how games implement animation, combat, AI, saves, dialogue, tactics, management, or other systems, or says to 学习架构/找开源项目/看看源码/不要抄玩法. Produces source-backed license, engine, maintenance, test, dependency, state-flow, and adopt/adapt/reject analysis grounded in the target project's current constraints.
---

# GitHub Game Architecture Study

Study repositories as evidence, not as templates to copy. Extract module boundaries, state flow, data contracts, and validation techniques that fit the target project.

## Required Tool Routing

Use `agent-reach` for every GitHub URL, repository search, or internet lookup. Read its GitHub/dev routing instructions before research. Prefer GitHub CLI/API evidence and exact repository files over summaries or search snippets.

## Workflow

1. Anchor the target project first. Read repository instructions and authoritative architecture/status/backlog documents. Record engine/language, genre, milestone, determinism, dependency, licensing, localization, save, and no-touch constraints.
2. Convert the question into evaluation criteria before searching. Example dimensions: rule/presentation separation, data-driven definitions, deterministic RNG, event flow, animation authoring, editor tooling, tests, content scale, and commercial reuse.
3. Search broadly enough to avoid confirmation bias, then shortlist only repositories with relevant readable source. Do not rank by stars alone.
4. For every shortlisted repository, inspect the evidence listed in [repository-evaluation-rubric.md](references/repository-evaluation-rubric.md). Read README plus the actual entry points, core models/services/controllers, representative content definitions, tests, project/manifest files, and license.
5. Reconstruct a concrete state flow such as:

   `input -> intent/command -> model mutation -> result/events -> presentation -> persistence`

   Mark missing or coupled seams explicitly.
6. Separate findings into:

   - transferable architecture or workflow;
   - engine/version-specific implementation details;
   - code that licensing may permit but still needs adaptation;
   - assets, franchise data, or reverse-engineered material that must not be reused;
   - patterns that conflict with the target project.

7. Compare each pattern with the target code that already exists. Prefer strengthening an existing seam over importing a parallel framework.
8. Classify recommendations as `adopt`, `adapt`, `study only`, or `reject`. State the reason, expected benefit, migration cost, and verification requirement.
9. Cite exact GitHub files or authoritative pages near each claim. Distinguish confirmed facts from inference.
10. Do not clone into the target workspace or modify project files for a research-only request. Use a temporary location when local inspection is necessary. Do not implement unless the user separately authorizes a change.
11. For a large research pass, run the Agent Reach update check required by its skill and report an available update without interrupting the task.

## Decision Rules

- Missing license means study only; do not copy code or assets.
- A repository license does not prove every bundled asset is safe. Inspect asset provenance and per-folder notices.
- Decompilations, ROM-hacking projects, fan recreations, and franchise asset repositories are architecture references only unless independently licensed original material is proven.
- Old engine code may still teach state flow, but classify direct portability separately.
- A runnable demo without tests is evidence of behavior, not evidence of deterministic correctness.
- README claims are hypotheses until confirmed in source.
- Reject systems that place gameplay mutations in UI, animation callbacks, physics timing, or unseeded presentation code when the target requires deterministic simulation.

## Expected Output

Lead with the suitability verdict. Then provide a compact comparison of candidates, explain the transferable architecture, identify legal and technical boundaries, and recommend the smallest next action. Include the target repository's required completion-report fields when applicable.
