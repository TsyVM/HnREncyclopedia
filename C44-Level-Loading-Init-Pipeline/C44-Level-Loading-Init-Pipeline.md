# Chapter 44 — Level Loading & the Init Pipeline

> **Goal of this chapter:** decode *how a level comes to life* — what runs when a level loads,
> in what order, and what the level **init** script (`leveli.mfk`) actually sets up. This is the
> "have we covered level loading?" chapter: the persistent, level-wide scaffolding every mission
> and every wandering NPC stands on.

When you pick a level, a great deal happens before you can drive: the world art streams in
(C30/C12), and then a **level init script** runs top-to-bottom to populate the living world —
the player's car, the police, the crowds, the traffic, the coins, the spawn points. That script
is `leveli.mfk`, and its own first line says it plainly: *"This is all level initialization
stuff.. Anything here is persistent across the entire level."*

**Key finding (✅ verified):** `leveli.mfk` is the level's **init** file (the `i` = *init*, not
"interior"). It runs once per level and establishes everything that outlives any single mission:
`EnableTutorialMode`, `InitLevelPlayerVehicle("famil_v","level1_carstart","DEFAULT")` (the family
car and where it starts), `AddCharacter("homer","homer")` (the player), `CreateChaseManager` +
`SetNumChaseCars` + `SetHitAndRunDecay` (the police, C31), `PreallocateActors` (reserve the actor
pool — an engine-limit interaction, C39), `SetCoinDrawable("coinShape_000")` (the coin model,
C32), `SetProjectileStats`/`SetActorRotationSpeed` (tuning), and the population blocks — **ped
groups** (C45), **traffic groups** (C46), **spawn points** (C47), and the **conversation/bonus
setup** (C48). Missions (`m{N}l.mfk`) layer *on top* of this persistent base.

---

## Deep-dive pages

- [C44.1 — What "Level Init" Means](01-level-init.md): persistent vs per-mission; where `leveli.mfk` sits in the load.
- [C44.2 — The Load Order](02-load-order.md): art stream → init script → gameplay; how it dovetails with GameFlow (C30).
- [C44.3 — The Init Vocabulary](03-init-vocabulary.md): every level-wide setup command, grouped.
- [C44.4 — Preallocation & the Actor Pool](04-preallocation.md): `PreallocateActors` and why levels reserve up front (C39).
- [C44.5 — The Player, Car & Police Setup](05-player-car-police.md): `InitLevelPlayerVehicle`, `AddCharacter`, `CreateChaseManager`.
- [C44.6 — Modding Level Init](06-modding.md): changing the start car, crowd density, tutorial, coin model.

---

## 44.1 What level init means (✅ verified)

`leveli.mfk` runs **once**, at level load, and everything it creates **persists for the whole
level** — unlike a mission script (`m{N}l.mfk`) whose setup is torn down when the mission ends.
Understanding this split is the key to knowing *where* to change something. [C44.1](01-level-init.md).

## 44.2 The load order (✅ verified shape)

```
GameFlow LoadingContext (C30) ─► stream level art (world P3D, sky, C12/C43)
                              ─► run leveli.mfk (this chapter) ─► populate the world
                              ─► GameplayContext ─► (missions layer on top)
```
[C44.2](02-load-order.md).

## 44.3 The init vocabulary (✅ verified)

Grouped: **world/player** (`InitLevelPlayerVehicle`, `AddCharacter`, `EnableTutorialMode`),
**police** (`CreateChaseManager`, `SetNumChaseCars`, `SetHitAndRunDecay`), **population**
(ped groups → C45, traffic groups → C46, spawn points → C47), **economy/tuning**
(`SetCoinDrawable`, `SetProjectileStats`, `SetActorRotationSpeed`), **capacity**
(`PreallocateActors`). Full table in [C44.3](03-init-vocabulary.md).

## 44.4 Preallocation (✅ verified)

`PreallocateActors` reserves the actor pool up front so spawns during play never allocate (and
never fragment). This is a direct engine-limit lever (C39). [C44.4](04-preallocation.md).

## 44.5 Player, car & police (✅ verified)

`InitLevelPlayerVehicle("famil_v","level1_carstart","DEFAULT")` places the family sedan at the
named start locator; `AddCharacter("homer","homer")` is the player; the chase manager arms the
police. [C44.5](05-player-car-police.md).

## 44.6 Modding (✅ practical)

Change the start car, the crowd, the tutorial flag, or the coin model by editing `leveli.mfk`.
[C44.6](06-modding.md).

---

## What this chapter established

- A level is built by a **persistent init script** (`leveli.mfk`) that runs once and sets up
  everything level-wide; missions layer on top and are torn down individually.
- The init covers the **player+car**, the **police**, the **crowd** (ped groups), the
  **traffic**, the **spawn points**, and **economy/tuning** — each its own subsystem (C45–C48).
- `PreallocateActors` ties level loading directly to the engine's actor limits (C39).

**Cross-references:** C30 (GameFlow/loading), C12 (level art), C45 (peds), C46 (traffic), C47
(spawn points), C48 (conversations), C31 (police), C32 (coins), C39 (actor limits), C14 (MFK).
