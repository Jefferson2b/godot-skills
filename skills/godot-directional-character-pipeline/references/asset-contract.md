# Directional Asset Contract

## Manifest schema

The auditor consumes JSON with `schema_version: 1`.

```json
{
  "schema_version": 1,
  "required_facings": ["north", "east", "south", "west"],
  "required_actions": ["idle", "move", "attack", "skill", "hit", "down"],
  "characters": [
    {
      "id": "character_id",
      "definition": "res://data/presentation/character_id.tres",
      "min_parts_per_facing": 12,
      "required_actions": ["idle", "move", "attack", "skill", "hit", "down"],
      "expected_parts_by_facing": {
        "east": ["torso", "head", "near_upper_arm"]
      }
    }
  ]
}
```

`project_root` may be stored in the manifest, but an explicit `--project-root` takes precedence. Prefer an explicit root in automation so copied manifests remain portable.

### Character fields

- `id`: stable expected puppet or character ID.
- `definition`: `.tres` path, either filesystem-relative or `res://`.
- `required_facings`: optional per-character override.
- `required_actions`: optional per-character override.
- `min_parts_per_facing`: integer or facing-to-integer object. Use zero when composite-only directions are intentionally accepted.
- `expected_parts_by_facing`: optional exact part-ID lists. The auditor reports both missing and unexpected parts.

## Supported Godot resource shape

The bundled auditor recognizes text `.tres` resources whose subresources reference scripts ending in:

- `paper_puppet_facing_def.gd`
- `paper_puppet_part_def.gd`
- `paper_puppet_action_def.gd`

It reads `puppet_id`, `facing_id`, `part_id`, `parent_part_id`, `texture`, `composite_texture`, and `action_id`. Adapt the suffix constants in the script if a repository uses different class filenames; do not weaken the project contract to fit the tool.

Texture references must resolve through declared `ExtResource` paths. `res://` paths resolve from the supplied project root. Missing imports are not checked; run Godot import separately.

## Failure interpretation

- Missing facing/action: incomplete matrix or a mismatched manifest.
- Too few parts: staged candidate still below its declared production baseline.
- Missing/unexpected exact parts: cross-facing rig drift.
- Duplicate part: ambiguous pose targeting.
- Broken parent: invalid local hierarchy for that facing.
- Missing texture: stale resource reference or incomplete asset copy.
- ID mismatch: manifest points at the wrong definition or the runtime ID changed without migration.

Run with `--format json` when another script needs structured output. Exit code is `0` only when all declared contracts pass, `1` for audit failures, and `2` for invalid input or unsupported resource structure.
