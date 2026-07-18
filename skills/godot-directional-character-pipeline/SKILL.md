---
name: godot-directional-character-pipeline
description: Build, audit, complete, and verify directional 2D character asset pipelines in Godot projects. Use when Codex must produce or review multi-direction sprites, cutout puppets, layered character rigs, facing-specific parts, action matrices, foot anchors, pivots, parent chains, texture references, or in-engine visual acceptance for `.tres`, `.res`, `.gd`, PNG, WebP, or sprite-sheet assets. Also use for requests to find missing directions/actions, turn one approved facing into a production baseline, or establish a repeatable character-art manifest without changing gameplay rules.
---

# Godot Directional Character Pipeline

Turn an approved character-facing baseline into a complete, auditable asset matrix. Keep art production, presentation data, and gameplay state separate.

## Workflow

1. Read the repository instructions and art/technical source-of-truth documents. Confirm the Godot version, repository root, current milestone, asset provenance policy, and no-touch boundaries.
2. Inspect the live runtime contract before proposing assets. Locate the character definition, facing definition, part definition, action definition, catalog, renderer, tests, and screenshot entry point. Do not infer the contract from filenames alone.
3. Inventory the current matrix before editing. Copy `assets/directional-character-manifest.template.json` into a project-controlled location, replace its examples with the real definitions, and set the required facings, actions, and minimum or exact part expectations.
4. Run `scripts/audit_directional_assets.py --manifest <manifest> --project-root <root>`. Preserve the baseline output; distinguish missing production work from malformed data.
5. Choose one bounded production batch: one character and one facing, or one shared action across already-complete facings. Use an approved facing as the structural baseline, but redraw direction-sensitive anatomy, weapons, clothing overlap, and accessories instead of silently mirroring them.
6. Produce or edit assets through the applicable visual workflow. Keep stable part IDs where the runtime contract requires cross-facing reuse. Record source, license or generation method, review state, and modifications in the project's provenance ledger.
7. Integrate through presentation definitions and catalogs only. Never let a sprite, animation callback, facing cache, or pose key decide movement, hit, damage, turn order, or save state.
8. Re-run the static audit, project tests, Godot import, scene smoke tests, and the repository's real screenshot workflow. Use the visual checklist in `references/visual-qa-checklist.md`.
9. Report the completed matrix, commands and results, screenshots checked, unresolved directions/actions, provenance status, and the exact next batch.

## Audit Rules

- Treat stable IDs and runtime definitions as authoritative; display text and filenames are not identifiers.
- Require every manifest-facing and action exactly once unless the project contract explicitly says otherwise.
- Require unique part IDs within each facing, valid parent references within that facing, and resolvable texture paths.
- Use `min_parts_per_facing` for staged production and `expected_parts_by_facing` when an approved exact rig exists.
- A composite fallback may keep a scene runnable, but it does not satisfy a declared production-part requirement.
- A passing file audit does not approve visual quality. Always perform in-engine checks when assets changed.
- Do not count generated imports, mirrored placeholders, unreviewed candidates, or stale screenshots as finished production work.

## Resources

- Read `references/asset-contract.md` when creating or changing a manifest, adapting the auditor to another Godot resource schema, or interpreting failures.
- Read `references/visual-qa-checklist.md` before accepting player-visible assets or reporting a direction/action complete.
- Copy `assets/directional-character-manifest.template.json` as the starting manifest; do not edit the bundled template for one project.
- Run `scripts/audit_directional_assets.py --help` for command options. The script uses only the Python standard library and does not modify project files.
