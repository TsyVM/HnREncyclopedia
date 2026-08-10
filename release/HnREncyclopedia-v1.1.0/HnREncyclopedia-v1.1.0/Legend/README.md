# The Legend — Master Index of the Whole Game

The **Legend** is the exhaustive, categorized index the chapters point into: every named thing in *The
Simpsons: Hit & Run*, listed and grouped. Where the chapters explain **how systems work**, the Legend lists
**what exists** — every function, vehicle, character, costume, texture, object, mission, level, and class.

Everything here is ✅ **verified by extraction** from the retail data (or the executable's RTTI), and
reproducible with the tools in [`../tools/`](../tools/) and `DonutsSDK/tools/`.

## Contents

| Index | Contents | Count |
|---|---|---:|
| [functions.md](functions.md) | Every script command — MFK (level/mission) + CON (vehicle handling), categorized | 172 + 40 |
| [vehicles.md](vehicles.md) | Every vehicle: id, name, top speed, driver | 90 |
| [characters.md](characters.md) | Every character/pedestrian model | 132 |
| [costumes.md](costumes.md) | Costumes & skins ("clothes") — the `a_*`/`b_*` variants | 11 |
| [textures.md](textures.md) | Every distinct texture name (stored in the clear, C5.1) | 751 |
| [objects.md](objects.md) | Generic world/mission objects + map-icon vocabulary | — |
| [missions.md](missions.md) | Mission index by level (story + bonus) | 7 levels |
| [levels-maps.md](levels-maps.md) | The 3 shared maps, 7 levels, named locations | — |
| [classes.md](classes.md) | Runtime class namespace summary (full table in DonutsSDK) | 1,207 |

## How the Legend relates to the chapters

- A **function** in [functions.md](functions.md) is explained in C14 (MFK) or C15 (CON).
- A **vehicle** in [vehicles.md](vehicles.md) has its handling in C15 and its runtime in C24.
- A **character/costume** ([characters.md](characters.md)/[costumes.md](costumes.md)) is rigged in C8, run in
  C25, choreographed in C17.
- A **texture** ([textures.md](textures.md)) is decoded in C5, bound by a shader in C6.
- A **class** ([classes.md](classes.md)) is the runtime model of C23–C32; the full table with inheritance and
  verified vtable addresses is `DonutsSDK/data/shar_dumps.csv` + `class_vtables.csv`.
- The master **chunk-ID** table is the [Glossary](../Glossary/chunk-ids.md) (179 ids); the **terminology** is
  the [Glossary](../Glossary/terminology.md).

## Confidence

Names, ids, and counts are ✅ **Verified** — read directly from the shipped files or the executable's RTTI.
Where a human-readable *interpretation* is inferred (a costume's theme, a texture's use), it is a light
annotation, not a byte-proven claim; the *name* itself is verified. Mission *display titles* come from the
localized TextBibles (C22, ⏳ not decoded) — the Legend uses the script IDs, which are the modding handles.
