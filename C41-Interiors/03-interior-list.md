# C41.3 — The Interior List

> The named interiors, recovered from the retail scripts. Each id is the string passed to
> `GagSetInterior("<id>")` in the level's `level.mfk` (C41.4).

## Level 1 (✅ verified, 8 interiors)
| id | Place |
|---|---|
| `kwikemart` | Kwik-E-Mart |
| `simpsonshouse` | Simpsons House |
| `bartroom` | Bart's Room |
| `springfieldelementary` | Springfield Elementary |
| `moe1` | Moe's Tavern |
| `android` | The Android's Dungeon (comic shop) |
| `dmv` | DMV |
| `observatory` | Observatory |

Occurrence counts (gag bindings) in the retail level-1 scripts: `kwikemart` ×84,
`simpsonshouse` ×77, `springfieldelementary` ×59, `observatory` ×32, `moe1` ×25, `android` ×15,
`dmv` ×9, `bartroom` ×8.

## Other levels
Levels 2–7 define their own interiors the same way (their `level.mfk` uses `GagSetInterior`
with that level's ids). The **system is identical per level**; the *list* is per-level content.
This chapter's verified enumeration is level 1 (the scripts most fully present in the retail
tree); the mechanism (C41.1/41.2) is universal.

## Where this list lives in the SDK
`DonutsSDK/data/interiors.csv` carries the ids, display names, and level. Regenerate/extend it
by grepping `GagSetInterior` across a level's scripts.

## Cross-references
C41.4 (how the ids are declared), C41.1 (the system), the Legend (master index).
