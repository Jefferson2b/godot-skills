# Repository Evaluation Rubric

## Evidence to Collect

| Area | Evidence |
| --- | --- |
| Identity | owner/name, default branch, archive status, repository URL |
| Maintenance | latest meaningful code commit, releases, issue/PR activity when relevant |
| Technology | engine version, language, renderer/platform, manifest/project files |
| License | repository license, asset licenses, third-party notices, provenance |
| Dependencies | addons, network-fetched packages, native binaries, editor plugins |
| Architecture | entry point, model/state, commands/services, controllers, views, persistence |
| Determinism | RNG ownership, time/physics dependencies, ordering, replay/log support |
| Data design | immutable definitions, runtime state, stable IDs, serialization schema |
| Presentation | event/result consumption, timelines, animation callbacks, skip/speed behavior |
| Quality | automated tests, CI, headless entry point, smoke scenes, documentation accuracy |

## Source-Availability Classes

- `A — reusable source`: clear license, relevant source, compatible constraints.
- `B — adaptable reference`: licensed source but old engine, partial architecture, or substantial migration cost.
- `C — study only`: missing/unclear license, reverse engineering, franchise data, or unsafe assets.
- `D — unsuitable`: no relevant source, incompatible architecture, abandoned/broken evidence, or misleading repository scope.

## Recommendation Template

For each candidate, record:

1. What it actually implements.
2. The evidence files inspected.
3. The state/data flow.
4. What the target project already has.
5. `adopt`, `adapt`, `study only`, or `reject`.
6. License and asset boundary.
7. Smallest safe experiment or next action.

## Common Warning Signs

- One large player/unit script owns input, rules, animation, UI, and saves.
- Animation callbacks apply damage or decide hit/miss.
- Display text is used as an identifier.
- Mutable definition resources double as runtime state.
- Random calls are global and unseeded.
- Save files serialize scene nodes or opaque objects without schema versioning.
- Repository metadata says MIT while bundled art is ripped, noncommercial, or uncredited.
- Recent repository activity reflects stars/issues rather than recent code pushes.
