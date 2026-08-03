# Chapter 16 — Mission Structure & Objectives

> **Goal of this chapter:** read and author a complete mission. Building on the MFK language (C14), this
> chapter decodes the mission state machine — its stages, the **20 verified objective types**, the **7
> verified condition types** — plus showdowns, bonus missions, and the reward system that ties missions to
> the cars they unlock.

Missions are what turn Springfield (C12) into a game. Chapter 14 established that a mission is a balanced
sequence of `AddStage…CloseStage` blocks; this chapter fills in the *vocabulary* those blocks draw on, all
extracted and counted from the retail `scripts/missions/` tree. Every objective and condition type below is
verified — it is the complete set the shipped missions use, not a sample.

**Key finding (✅ verified):** the mission system is a small, closed **domain language**. Objectives come in
**20 types** (`goto`, `dialogue`, `talkto`, `getin`, `race`, `destroy`, `delivery`, `destroyboss`, …);
conditions in **7** (`timeout`, `damage`, `outofvehicle`, `position`, `followdistance`, `race`,
`keepbarrel`). A mission is assembled from these like sentences from a fixed vocabulary.

---

## Deep-dive pages

- [C16.1 — Mission File Anatomy & the Roster](01-mission-anatomy.md): the `i`/`l`/`sd` split and the per-level line-up.
- [C16.2 — Stages: the Mission State Machine](02-stages.md): `AddStage`, message index, timing, waypoints.
- [C16.3 — The 20 Objective Types](03-objective-types.md): every verified `AddObjective` kind and what it does.
- [C16.4 — The 7 Condition Types](04-condition-types.md): every verified `AddCondition` kind and its parameters.
- [C16.5 — Showdowns & Bonus Missions](05-showdowns-bonus.md): boss finales, street races, and bonus content.
- [C16.6 — Rewards & the Runtime Mission System](06-rewards-runtime.md): `BindReward`, unlock economy, and the RTTI `Mission*` classes.

---

## 16.1 A mission's files and the roster (✅ verified)

Each mission is split by role (C14.1): `m{N}l.mfk` **loads** its assets, `m{N}i.mfk` holds its **logic**,
`m{N}sd{i,l}.mfk` is its **showdown**. A level's `level.mfk` (C12.4) lists the roster — verified for Level 1:

```
AddMission("m0")…AddMission("m7")          // 8 story missions
AddBonusMission("sr1"/"sr2"/"sr3")         // street races
AddBonusMission("gr1")  AddBonusMission("bm1")   // gag race, bonus mission
```

Every level runs the same shape: **7–8 story missions + 5 bonus missions**. [C16.1](01-mission-anatomy.md).

## 16.2 Stages: the state machine (✅ verified)

A mission runs its stages in order (C14.3). Each `AddStage(flags)` opens a stage; inside,
`SetStageMessageIndex(n)` sets the instruction text (C22), `AddStageTime`/`AddStageWaypoint`/
`AddStageVehicle` add timing, route, and vehicles, and one or more objectives and conditions define
success and failure. `CloseStage()` ends it. The engine advances stage-by-stage until the mission is won or
a condition fails it. [C16.2](02-stages.md).

## 16.3 The 20 objective types (✅ verified)

Extracted and counted across all missions, `AddObjective` uses exactly 20 types:

| Objective | Uses | Objective | Uses | Objective | Uses |
|---|--:|---|--:|---|--:|
| `goto` | 191 | `destroy` | 15 | `coins` | 7 |
| `dialogue` | 139 | `delivery` | 15 | `fmv` | 6 |
| `talkto` | 99 | `dump` | 13 | `buycar` | 6 |
| `getin` | 48 | `interior` | 19 | `pickupitem` | 4 |
| `race` | 44 | `losetail` | 17 | `gooutside` | 4 |
| `timer` | 27 | `follow` | 7 | `destroyboss` | 4 |
| — | | `buyskin` | 4 | `dummy` | 2 |

`goto`, `dialogue`, and `talkto` dominate — SHAR is a game of driving somewhere and talking to someone.
[C16.3](03-objective-types.md) documents each.

## 16.4 The 7 condition types (✅ verified)

Conditions decide *failure*. The complete set: `timeout` (169), `damage` (117), `outofvehicle` (100),
`position` (17), `followdistance` (12), `race` (10), `keepbarrel` (10). Parameters come from `SetCond…`
setters (`SetCondTime`, `SetCondMinHealth`, `SetCondTargetVehicle`, C14.3). [C16.4](04-condition-types.md).

## 16.5 Showdowns & bonus missions (✅ verified)

The `m{N}sd` files are **showdowns** — boss finales that use the `destroyboss` objective (4 uses across the
game, one per level's boss). Bonus content is the **street races** (`sr*` — time trial, circuit, waypoint),
the **gag race** (`gr1`), and **bonus missions** (`bm1`), plus level-specific extras like Level 3's
`ismovie`. [C16.5](05-showdowns-bonus.md).

## 16.6 Rewards & runtime (✅ verified)

`BindReward` connects a mission to what it unlocks — almost always a **car**. Verified syntax and types:

```
BindReward("famil_v","art\cars\famil_v.p3d","car","defaultcar",1)
BindReward("cletu_v","art\cars\cletu_v.p3d","car","bonusmission",1)
BindReward("elect_v","art\cars\elect_v.p3d","car","streetrace",1)
BindReward("plowk_v","art\cars\plowk_v.p3d","car","forsale",1,40,"simpson")   // cost + seller
```

Cars are unlocked by finishing story missions, bonus missions, and street races, or **bought** from a
seller for coins. At runtime a mission is the RTTI `Mission`/`MissionStage`/`MissionObjective` family (names
✅, offsets ⏳). [C16.6](06-rewards-runtime.md).

---

## Key takeaways

- A mission is a **balanced stage sequence** drawing on a **closed vocabulary**: **20 objective types**, **7
  condition types** (both ✅ verified as the complete shipped set).
- Files split by role: `…l` load, `…i` logic, `…sd` showdown. Every level: **7–8 story + 5 bonus** missions.
- `goto`/`dialogue`/`talkto` dominate objectives; `timeout`/`damage`/`outofvehicle` dominate conditions.
- **Rewards** (`BindReward`) unlock **cars** via `defaultcar`/`bonusmission`/`streetrace`/`forsale` — the
  game's progression economy.
- Runtime is the RTTI `Mission*` family (names ✅, offsets ⏳; C26).

**Next:** [Chapter 17 — Choreography & Characters](../C17-Choreography-Characters/C17-Choreography-Characters.md).
