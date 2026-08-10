# C12.4 — The `level.mfk`: Missions & Teleports

**What it is.** The script that assembles a level's *content* — its missions, bonus missions, fast-travel
destinations, and selectable vehicles. If the terrain and blocks (C12.1–C12.2) are the level's *body*, the
`level.mfk` is its *table of contents*.

**How it works (✅ verified).** `scripts/missions/level01/level.mfk` declares, in order:

```
AddMission("m0"); AddMission("m1"); … AddMission("m7");     // the 8 story missions
AddBonusMission("sr1"); AddBonusMission("sr2");             // street races
AddBonusMission("sr3"); AddBonusMission("gr1");
AddBonusMission("bm1");                                      // bonus mission
AddTeleportDest("Simpsons' House", 220, 3.5, -172, "l1z1.p3d;l1r1.p3d;l1r7.p3d;");
… 12 teleport destinations …
AddVehicleSelectInfo(…);                                    // selectable cars for this level
```

So a level is: **8 story missions** (`m0`–`m7`, whose logic lives in the `m{N}i.mfk` files of C16),
**bonus missions** (street races `sr*`/`gr*`, bonus `bm*`), **12 teleport destinations** (the fast-travel
map, each with coordinates and its streaming set, C12.3), and **vehicle-select info** (which cars the player
can drive here). The `level.mfk` names all of it; the individual mission and car files (C15/C16) provide the
detail.

**Why a content manifest.** Keeping the level's roster in one script means the *structure* of a level — what
you can do and where you can go — is editable in one place, separate from the *implementation* of each
mission (its own `m{N}i.mfk`, C16) and each car (its own `.con`, C15). Add a mission to a level by adding one
`AddMission` line and authoring its mission file; add a fast-travel point with one `AddTeleportDest`. This is
the same "manifest + parts" pattern as the load files (C14.2): the level script lists what exists; the parts
define what each thing is.

**The teleport destinations as a level map.** The 12 `AddTeleportDest` entries are effectively the level's
map legend — every named place (Simpsons' House, Kwik-E-Mart, Church, Springfield Elementary, Burns' Mansion,
Stonecutters Tunnel, Power Plant, Tomacco, Trailer Park, Cletus' House…), its world coordinates, and the
world data to stream there. Reading them gives you the level's geography and its streaming plan at once, which
is why they're the single most informative lines in a `level.mfk`.

**What happens if you bend it.**

- *Add a mission file without an `AddMission` line* — the mission exists but the level never offers it. List
  it in `level.mfk`.
- *Give a teleport destination the wrong streaming set* — you fast-travel there and the world is missing or
  wrong (C12.3). Match the set to the location.
- *Add a car to `AddVehicleSelectInfo` that isn't loaded* — it can't be selected/spawned. Ensure its `.p3d`
  (C7) and `.con` (C15) are available.
