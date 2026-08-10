# C44.2 — The Load Order

> Where `leveli.mfk` sits in the sequence from "clicked a level" to "driving Springfield."

## The sequence (✅ verified shape)
```
1. GameFlow: LoadingContext (C30) takes over; the loading screen shows.
2. Stream the level's ART: world blocks/terrain (C12), sky dome + baked lighting (C43),
   textures, models, the ped/traffic/car models the init will reference.
3. Run leveli.mfk (this chapter) top-to-bottom: populate the persistent world.
4. GameFlow: GameplayContext; control handed to the player.
5. Missions (m{N}l.mfk) load/unload on top as the player starts/finishes them.
```

## Why art before init
The init script *references assets by name* (`AddPed("male6",…)`, `AddTrafficModel("minivanA",…)`,
`InitLevelPlayerVehicle("famil_v",…)`). Those models must already be resident, so the art stream
runs first. A name the art didn't load can't spawn — the classic "referenced but not packaged"
break from the add-content pipeline (C39.4).

## Why init is one linear script
Level setup is inherently sequential (create a group, add its members, close it), and running it
as a plain top-to-bottom script makes the whole level's initial state readable and editable in one
file — no hidden ordering. It also gives a single, deterministic point where the persistent world
exists before gameplay.

## What happens if you bend it
Reordering init commands can matter (you must `CreatePedGroup` before `AddPed`, then
`ClosePedGroup`). Referencing an asset the art didn't load fails silently — check the packaging
first (C39.4).

## Cross-references
C30 (GameFlow contexts), C12/C43 (level art), C39.4 (author→package→reference→load→render),
C44.3 (the vocabulary that runs here).
