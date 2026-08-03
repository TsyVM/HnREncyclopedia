# Chapter 14 — MFK Level & Mission Scripts

> **Goal of this chapter:** read the scripts that build every level and drive every mission. After this
> chapter you can open any `.mfk`, follow how a level loads its assets and how a mission sequences its
> stages, objectives, gags, and NPCs — and change any of it.

If the `.con` files (Chapter 15) are the game's *nouns* — the cars — the **`.mfk` files are its verbs**.
There are **344 `.mfk` scripts**, and together they use a vocabulary of **172 distinct commands**
(✅ verified by extraction across the whole tree). They assemble each level from Pure3D files, place its
NPCs and traffic, and — mission by mission — script the stages, objectives, conditions, collectibles, and
comedy "gags" that are the actual game. Like `.con`, MFK is plain text: `Name(args);` calls and `//`
comments. Unlike `.con`, its vocabulary is large and its files are structured into blocks by convention.

Everything here is grounded in the shipped scripts: every command and its call-count come from parsing all
344 files, and the mission structure below is read directly from real mission scripts like
`scripts/missions/level01/bm1i.mfk`.

---

## Deep-dive pages

- [C14.1 — The MFK Language & File Roles](01-the-mfk-language.md): syntax, and the `l`/`i`/`sd` file-role convention.
- [C14.2 — Asset Loading](02-asset-loading.md): `LoadP3DFile`, `LoadDisposableCar`, `SetDynaLoadData` — the level's file manifest.
- [C14.3 — Missions: Stages, Objectives & Conditions](03-missions-stages-objectives.md): `SelectMission`, `AddStage`/`CloseStage`, `AddObjective`, `AddCondition`.
- [C14.4 — Gags & Collectibles](04-gags-and-collectibles.md): the `Gag…` verb set and `AddCollectible`.
- [C14.5 — Peds, NPCs, Traffic & Waypoints](05-peds-npcs-traffic.md): populating the world and routing it.
- [C14.6 — Cameras, Dialogue & Rewards](06-cameras-dialogue-rewards.md): staging conversations, HUD, and unlocks.

---

## 14.1 The language and the file roles

MFK shares `.con`'s surface — statements are `Name(args);`, comments are `//` — but adds *scale* and a
naming convention that encodes each file's job. Mission files come in variants distinguished by a suffix:

- **`…l.mfk`** — the **load** file: mostly `LoadP3DFile`/`LoadDisposableCar`, listing every asset the
  mission needs (verified: `m1l.mfk` is a pure load list).
- **`…i.mfk`** — the **instructions/logic** file: the mission's stages and objectives (verified:
  `bm1i.mfk` opens `SelectMission("bm1")` then a sequence of `AddStage…CloseStage`).
- **`…sd…`** — **showdown** variants (boss/finale missions).

Top-level `ss.mfk`/`ssi.mfk` and per-level `level.mfk`/`leveli.mfk` set up the level itself. This split —
loading separated from logic — is the organising principle of the whole `scripts/` tree.
[C14.1](01-the-mfk-language.md).

## 14.2 Loading a level (✅ verified vocabulary)

The most-used command in the game is `LoadP3DFile` (1,013 calls). Loading is explicit and total — a level's
`…l.mfk` names every Pure3D file it needs:

```c
LoadP3DFile("art\missions\level01\m1.p3d");
LoadDisposableCar("art\cars\skinn_v.p3d","skinn_v","AI");
LoadP3DFile("art\frontend\dynaload\images\msnicons\char\lisa.p3d");
```

These paths are the richest source of real names for hash recovery (C2.4). `SetDynaLoadData` (154 calls)
declares dynamically-streamed content. [C14.2](02-asset-loading.md).

## 14.3 A mission is a sequence of stages (✅ verified structure)

Mission logic is a flat sequence of stage blocks, read directly from `bm1i.mfk`:

```c
SelectMission("bm1");
  AddStage(0);
    SetStageMessageIndex(12);
    AddObjective("getin");
  CloseStage();
  AddStage(16);
    SetStageMessageIndex(145);
    AddObjective("delivery");
    AddCondition("timeout");
  CloseStage();
  ...
```

`AddStage`/`CloseStage` (670 each — perfectly balanced, ✅) bracket each stage; inside, `AddObjective`
(671) sets the goal, `AddCondition` (435) sets fail/complete conditions, `SetStageMessageIndex` (495)
points at the localized instruction text (C22). [C14.3](03-missions-stages-objectives.md).

## 14.4 The gag system (✅ verified)

SHAR's comedy set-pieces are "gags," and they have their own complete verb family — `GagBegin`/`GagEnd`
(419 each, balanced), `GagSetCycle`, `GagSetSound`, `GagSetTrigger`, `GagSetCoins`, `GagSetPosition`,
`GagSetSparkle`, and more. Collectibles use `AddCollectible` (689) and `SetCollectibleEffect` (337). This
is a whole scripting subsystem for interactive jokes. [C14.4](04-gags-and-collectibles.md).

## 14.5 Populating the world (✅ verified)

`AddPed` (444), `AddNPC` (318), `CreatePedGroup`/`ClosePedGroup` (116 each), `UsePedGroup` (134), and
`SetMaxTraffic` (136) place and budget the world's inhabitants; `AddSpawnPointByLocatorScript` (371),
`AddStageWaypoint` (442), and `AddAmbientNPCWaypoint` (473) route them using the locators baked into the
geometry (C8) and the paths (C13). [C14.5](05-peds-npcs-traffic.md).

## 14.6 Cameras, dialogue & rewards (✅ verified)

`SetConversationCam` (399), `SetAnimatedCameraName`, and `SetCamBestSide` stage cinematic moments;
`SetDialogueInfo`/`SetDialoguePositions`/`SetTalkToTarget` wire up spoken lines (from `dialog.rcf`, C19);
`SetHUDIcon` (429) and `SetPresentationBitmap` drive the HUD; `BindReward` (147) and `SelectMission`
connect a mission to its unlock. [C14.6](06-cameras-dialogue-rewards.md).

---

## Key takeaways

- **344 `.mfk` files, 172 commands** (✅ verified) build every level and mission in plain text.
- File **roles** are encoded in suffixes: `…l` loads assets, `…i` holds mission logic, `…sd` is showdown.
- A mission is a **balanced sequence of `AddStage…CloseStage` blocks**, each with objectives and
  conditions — the balanced call counts (670/670, 671, 419/419) are strong verification.
- Gags, collectibles, peds, traffic, waypoints, cameras, dialogue, and rewards each have their own
  verified verb family — MFK is really several small DSLs in one language.
- MFK paths are the best dictionary for hash recovery (C2.4).

**Next:** [Chapter 15 — CON Vehicle & Config Scripts](../C15-CON-Scripts/C15-CON-Scripts.md) (the cars these
scripts load), or [Chapter 16 — Missions & Objectives](../C16-Missions-Objectives/C16-Missions-Objectives.md).
