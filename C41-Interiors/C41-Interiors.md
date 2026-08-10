# Chapter 41 — Interiors

> **Goal of this chapter:** document the interior system — the enterable buildings (Kwik-E-Mart,
> Moe's, the Simpsons house…), the classes that swap you in and out, the entrance/exit locators,
> the per-interior gag and lighting setup, and how Hit & Run behaves inside. This is the
> interior **list** and the interior **mechanism** the book was missing.

Springfield isn't only the drivable streets — the player walks into **interiors**: shops,
houses, and landmarks that are separate spaces you enter on foot. These are a first-class,
confirmed subsystem, not set dressing.

**Key finding (✅ verified):** interiors are managed by **`InteriorManager`** (`0x00613C48`),
entered via an **`InteriorEntranceLocator`** (`0x006070D4`) through the
**`ActionButton::EnterInterior`** action (`0x0061723C`), and left via an **`InteriorExit`**
(`0x00613C54`) governed by a **`LeaveInteriorCondition`** (`0x00611348`); missions can require
being inside via **`InteriorObjective`** (`0x006115E8`). The enter/exit is wrapped by the
black-box fade of C40 (`EVENT_ENTER_INTERIOR_TRANSITION_*`). Interior gag/lighting content is
declared in the level's main script **`level.mfk`** (and `demo.mfk`) via `GagSetInterior("<id>")`
+ `InteriorLightGroup`/`InteriorOrigin`; the level's persistent setup (peds, ambient characters,
traffic, chase, player vehicle, Hit & Run decay) lives in the level **init** script
**`leveli.mfk`** — the `i` is *init*, not "interior". Level 1's verified interiors are:
**Kwik-E-Mart, Simpsons
House, Bart's Room, Springfield Elementary, Moe's Tavern, The Android's Dungeon, the DMV, and
the Observatory** (from `GagSetInterior` in the retail scripts).

---

## Deep-dive pages

- [C41.1 — The Interior System](01-the-system.md): `InteriorManager`, entrance/exit locators, the swap.
- [C41.2 — Entering & Leaving](02-enter-leave.md): `ActionButton::EnterInterior`, `LeaveInteriorCondition`, the flow (with the C40 fade).
- [C41.3 — The Interior List](03-interior-list.md): the verified named interiors and where they're defined.
- [C41.4 — Where Interiors Are Declared (`level.mfk`)](04-leveli-scripts.md): the `GagSetInterior`/`InteriorLightGroup`/`InteriorOrigin` vocabulary in `level.mfk`, and how it differs from the `leveli.mfk` level-init script.
- [C41.5 — Interiors in Missions](05-missions.md): `InteriorObjective`, `GetOutOfCarCondition`, interior-bound objectives.
- [C41.6 — Modding Interiors](06-modding.md): adding/altering an interior, moving an entrance, custom interior content.

---

## 41.1 The system (✅ verified)

`InteriorManager` owns the active interior and performs the world↔interior swap. Entrances and
exits are **locators** (C8) placed in the world: `InteriorEntranceLocator` marks where (and into
which interior) you enter; `InteriorExit` marks the way back. [C41.1](01-the-system.md).

## 41.2 Entering & leaving (✅ verified)

Walking onto an entrance locator offers `ActionButton::EnterInterior`; confirming raises the
C40 fade (`EVENT_ENTER_INTERIOR_TRANSITION_START`), the manager swaps in the interior at its
`InteriorOrigin`, and the fade lifts on `..._END`. Leaving is gated by `LeaveInteriorCondition`
and mirrored by `EVENT_EXIT_INTERIOR_START/END`. [C41.2](02-enter-leave.md).

## 41.3 The interior list (✅ verified, level 1)

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

Recovered from `GagSetInterior("<id>", …)` in the retail mission scripts. Later levels define
their own (the system is identical). Full list + counts in [C41.3](03-interior-list.md) and
`DonutsSDK/data/interiors.csv`.

## 41.4 Where interiors are declared (✅ verified vocabulary)

Interior gag/lighting content is declared in the level's **main script `level.mfk`** (and
`demo.mfk`), via `GagSetInterior("<id>")` to scope the following gag bindings to a named
interior, plus `InteriorLightGroup` / `InteriorOrigin`. This is **distinct** from the level
**init** script `leveli.mfk`, which handles the whole level's persistent setup — `AddPed`,
`AddAmbientCharacter`, `CreateChaseManager`, `AddTrafficModel`, `InitLevelPlayerVehicle`,
`SetHitAndRunDecay`, ped/traffic groups — and does *not* contain interior commands. Don't
confuse the two: `level.mfk` = level content (incl. interiors/gags); `leveli.mfk` = level init.
[C41.4](04-leveli-scripts.md).

## 41.5 Interiors in missions (✅ verified)

`InteriorObjective` requires the player to be inside a named interior;
`GetOutOfCarCondition`/`LeaveInteriorCondition` gate leaving. Some story beats happen inside
(talk to Apu, etc.). [C41.5](05-missions.md).

## 41.6 Modding (✅ practical)

Because interiors are script-defined (`leveli.mfk`) with confirmed manager classes, mods can
retexture an interior, move an entrance locator, change the gag/ambient set, or add a new
interior by defining its origin/lighting/entrance and registering it. [C41.6](06-modding.md).

---

## What this chapter established

- Interiors are a confirmed subsystem: **`InteriorManager`** + entrance/exit **locators** +
  the `ActionButton::EnterInterior` action, wrapped by the C40 fade.
- Each interior is **script-defined** in `leveli.mfk` (origin, lighting, gags, ambient NPCs,
  Hit & Run decay).
- Level 1's **eight named interiors** are verified from the retail scripts; the system repeats
  per level.

**Cross-references:** C40 (the enter/exit black-box fade), C8 (locators), C14 (MFK scripts),
C16 (missions/objectives), C31 (Hit & Run decay), C25 (ambient characters), C12 (level composition).
