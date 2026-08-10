# RE-Data — machine-readable tables

Every dataset the HnR Encyclopedia and DonutsSDK rest on, as JSON. All addresses are retail
`Simpsons.exe` VAs (`ImageBase 0x00400000`, no ASLR, MD5 `b3a47b881eec97745424b1e2c86cdcaf` —
see [`exe_meta.json`](exe_meta.json)). Files are UTF-8, 1-space indented.

> **Conventions.** VAs are `0x`-hex. Where a row carries a `source`/`evidence`/`note`, read that
> first. Confidence: ✅ verified (compiler-emitted RTTI or reproduced from bytes) · 🟡 reasoned ·
> ⏳ open. These tables regenerate from the retail data with `tools/` + `DonutsSDK/tools/`.

## The class model (from the executable's RTTI)

| File | Rows | What it is |
|---|--:|---|
| [`class_vtables.json`](class_vtables.json) | 1,131 | `class → vtable_va` — every RTTI-confirmed vtable (965 curated + 166 via SAHRDiag). |
| [`rtti_class_dumps.json`](rtti_class_dumps.json) | 3,971 | The raw RTTI dump rows: class/field/offset/anchor/opcode evidence per record. |
| [`member_offsets.json`](member_offsets.json) | 1,917 | Recovered member offsets (`class, offset, kind, evidence`). |
| [`runtime_object_sizes.json`](runtime_object_sizes.json) | 16 | Object `sizeof` from a live pool-stride capture (SAHRDiag). |
| [`runtime_composition.json`](runtime_composition.json) | 69 | Member/base subobjects by offset from embedded vtables (live capture). |
| [`transition_interior_classes.json`](transition_interior_classes.json) | 41 | The transition / interior / action / animation class reference (C40–C42). |
| [`managers.json`](managers.json) | 43 | **The manager layer** — every manager singleton (class, vtable, category, role), 7 domains (C49). |
| [`economy_effects_classes.json`](economy_effects_classes.json) | — | Reward/economy + particle/projectile classes (C50/C51). |
| [`particle_effect_slots.json`](particle_effect_slots.json) | 7 | The seven `SetParticleTexture` effect slots + triggers, from the devs' own comments (C51.2). |

## Formats & assets (from the shipped files)

| File | Rows | What it is |
|---|--:|---|
| [`chunk_ids.json`](chunk_ids.json) | 179 | The master Pure3D chunk-ID table (id, role, occurrences, name, confidence). |
| [`shader_params.json`](shader_params.json) | 21 | Shader FourCC parameter names. |
| [`texture_names.json`](texture_names.json) | 751 | Every texture name observed in the retail assets. |
| [`vehicle_roster.json`](vehicle_roster.json) | 90 | The vehicle roster. |
| [`rcf_archives.json`](rcf_archives.json) | 10 | The ten `RADCORE CEMENT LIBRARY` archives + sizes. |
| [`file_census.json`](file_census.json) | — | File count by extension across the whole retail tree. |

## Scripts, missions, gameplay (from the scripts + exe)

| File | Rows | What it is |
|---|--:|---|
| [`command_vocabulary.json`](command_vocabulary.json) | 202 | **Every distinct MFK/CON command** across all scripts, with occurrence counts + example files. |
| [`mfk_commands.json`](mfk_commands.json) | 172 | Curated MFK command reference. |
| [`con_commands.json`](con_commands.json) | 40 | Curated CON (vehicle-handling) command reference. |
| [`mission_objectives.json`](mission_objectives.json) | 20 | Mission objective types. |
| [`mission_conditions.json`](mission_conditions.json) | 7 | Mission condition types. |
| [`gags.json`](gags.json) | 367 | **Every touch-gag** parsed from `level.mfk`/`demo.mfk`: `file, p3d, interior, sound, coins`. |
| [`interiors.json`](interiors.json) | 8 | The verified interior list (level 1): id, display name, level. |

## Runtime protocol & subsystems (from the exe)

| File | Rows | What it is |
|---|--:|---|
| [`event_names.json`](event_names.json) | 6 | The complete set of `EVENT_*` string events — the interior-transition + iris-wipe protocol (C40). |
| [`animation_action_tokens.json`](animation_action_tokens.json) | 14 | Verified animation/action clip tokens (`getin`, `incar`, `jump_kick`, `locomotion8`, `wasp_attack`, …) (C42). |
| [`engine_string_anchors.json`](engine_string_anchors.json) | 289 | Subsystem anchor names (`*Manager`/`*Controller`/`*Behaviour`/`*Locomotion`/`*Objective`/`*Action`/`*Loader`). |
| [`engine_limit_strings.json`](engine_limit_strings.json) | 14 | The engine's own limit/assert guards (`too many…`, `static heap full`, `…required for locomotion`) (C39). |
| [`exe_meta.json`](exe_meta.json) | — | Build identity: MD5/SHA-1/size/base/arch. |
| [`trigger_effect_map.json`](trigger_effect_map.json) | 10 | **The "what fires what" map** — trigger → event → effect → outcome across the confirmed subsystems (interiors, attacks, gags, police, missions, time-of-day). |
| [`file_extensions.json`](file_extensions.json) | 30 | Complete file-extension census of the retail tree (excl. `.asi`/`.log`). |

## Regenerating

The class/format tables come from `DonutsSDK/data/*.csv` (extracted by `DonutsSDK/tools/`); the
script/gag/event tables are extracted fresh from the retail scripts + `Simpsons.exe` by the
encyclopedia's extractor. Re-run against your own retail copy to reproduce every count above.

> **Scope.** Reverse-engineering data for interoperability/documentation of a game you own.
> Single-player/offline. See the DonutsSDK and SAHRDiag repos for the tools that produce these.
