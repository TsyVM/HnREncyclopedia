# C12.1 — The Seven Levels & Terrain

**What it is.** The top-level structure of the game world: seven story levels, each anchored by a terrain
file, plus a separate multiplayer tree. This is the map of maps.

**How it works (✅ verified).** The retail data has **seven terrain files** — `L1_TERRA.p3d`, `l2_TERRA.p3d`,
`l3_TERRA.p3d`, `L4_TERRA.p3d`, `l5_TERRA.p3d`, `l6_TERRA.p3d`, `L7_TERRA.p3d` — one per story level. The
`scripts/missions/` tree carries `level01`–`level09` plus an **`h2h`** directory (head-to-head/multiplayer),
and `art/missions/` has `level01`–`level08` plus `generic` and `h2h`. The seven `*_TERRA` files are the
ground each level is built on; the higher level-numbers (08/09) are additional mission/bonus content rather
than new terrains.

The three levels whose terrain is capitalised — **L1, L4, L7** — are the game's three acts: the residential
neighbourhood (Level 1), the downtown/central area (Level 4), and the nuclear-plant/rural edge (Level 7). The
lower-cased `l2/l3/l5/l6` are the intervening levels. Each is a distinct slice of Springfield with its own
terrain, blocks, missions, and streamed zones (C12.3).

**Why split the world into levels at all.** SHAR's Springfield is far too large to hold in memory at once on
2003 hardware. Splitting it into seven levels — each a self-contained terrain plus its own asset set — bounds
how much world must ever be loaded, and gives the story its structure (each level is a chapter). Within a
level, streaming (C12.3) bounds it further. So the world is a hierarchy of budgets: seven levels, each split
into blocks, each split into zones — and only the current level's nearby zones are ever resident.

**The terrain file's role.** `L*_TERRA.p3d` is the base ground mesh and its collision — the surface cars
drive on and characters walk. It is the one asset always resident while its level is active, the canvas the
streamed blocks (C12.2) and props are placed over. Reading a terrain file (with the C7/C11 decoders) gives
you the level's shape and drivable surface.

**What happens if you bend it.**

- *Assume the whole game world is one map* — it's seven, streamed. Level transitions load a new terrain and
  asset set. Work within one level's data at a time.
- *Edit terrain without its collision* — the ground looks changed but cars drive the old surface (C11). Edit
  both.
- *Expect `level08`/`level09` to be new terrains* — they're additional mission content on existing worlds,
  not new grounds. Check the terrain files (seven) for the actual maps.
