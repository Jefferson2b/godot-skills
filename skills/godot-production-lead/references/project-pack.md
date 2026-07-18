# Project authority pack

Use six concerns, not necessarily six files. Prefer an existing file that already owns a concern.

| Concern | Common existing authorities | Required content |
|---|---|---|
| Product brief | `README.md`, `PRODUCT_BRIEF.md`, `GDD.md`, `DEMO_VERTICAL_SLICE.md` | core experience, audience, product boundary, non-goals |
| Milestones | `ROADMAP.md`, `MILESTONES.md`, `IMPLEMENTATION_STATUS.md`, `CURRENT_TASKS.md` | ordered milestones, active milestone, completion state |
| Acceptance | `ACCEPTANCE.md`, milestone acceptance files, quality bars, release checklists | reachable player behavior and evidence required to close |
| Technical decisions | `DECISIONS.md`, `TECHNICAL_DECISIONS.md`, `ARCHITECTURE.md` | chosen boundary, alternatives, consequences, migration |
| Content coverage | `CONTENT_MATRIX.md`, content manifests, asset scopes, implementation status | required versus completed content and fallback state |
| Playtest record | `PLAYTEST_LOG.md`, `PLAYTEST_PLAN.md`, `PLAYTEST_CHECKLIST.md` | build, route, observer, findings, decisions, regressions |

## Selection rules

1. Read candidates and declare one authority per concern.
2. Update that authority rather than adding a competing file.
3. Link detailed milestone evidence from the authority instead of expanding the authority indefinitely.
4. Keep facts that Codex must reason from in version-controlled text. A visual board may supplement references but must not be the only authority.
5. Do not write guessed status. Derive it from current code, tests, runtime evidence, and explicit product decisions.
6. Do not mark human visual approval, fun, clarity, or commercial readiness as passed without corresponding human or playtest evidence.

## Missing concerns

If a concern is truly missing, select only the matching template from `assets/project-pack/`, rename it to fit the project's existing convention, and replace every bracketed instruction. Add it to the project's document index when one exists.

## Conflict resolution

When two files disagree, prefer current runtime evidence first, then the explicitly designated current authority, then the newer scoped decision. Preserve useful history but label superseded claims rather than silently deleting them.
