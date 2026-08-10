# Chapter 47 — Spawn Points, Waypoints & Behaviours

> **Goal of this chapter:** decode how the world *places and animates* its actors beyond the crowd
> and traffic pools — the locator-driven **spawn points** (including the wasps/bee cameras), the
> **waypoint** networks NPCs walk, and the **behaviours** attached to actors. This is the placement
> and "make it act" layer we referenced but never opened.

Peds come from pools (C45) and traffic from groups (C46), but a lot of the world is placed at
*specific* spots and given *specific* jobs: the wasps that patrol rooftops, an NPC that walks a
set route, an object that reacts. That's the **locator + behaviour** layer.

**Key finding (✅ verified):** actors are placed at named **locators** (C8) by
`AddSpawnPointByLocatorScript( locator, script, actor, …, range, … )` — level 1 uses it to place
the **wasp "bee cameras"** (the flying enemies) at world locators like `w_lemon`,
`w_schoolroof1`, `w_bonuscar`, `w_stonetemple` (the `w_` prefix = wasp), each with a trigger range.
NPC movement is authored with **`AddAmbientNPCWaypoint( actor, waypoint )`** (×55 in level 1) —
paths built from waypoint locators. Actors are given jobs with **`AddBehaviour( … )`** (×25 in
level 1) — attaching a behaviour (patrol, react, guard) to a spawned actor. Together these are the
"place it, route it, make it act" layer on top of the raw spawn pools.

---

## Deep-dive pages

- [C47.1 — Locators as Anchors](01-locators.md): why everything is placed by named locator (C8).
- [C47.2 — Spawn Points by Locator Script](02-spawn-points.md): `AddSpawnPointByLocatorScript` and the wasp spawns.
- [C47.3 — The Wasps / Bee Cameras](03-wasps.md): the `w_*` spawn points and the flying enemies (C31).
- [C47.4 — Waypoints & Routes](04-waypoints.md): `AddAmbientNPCWaypoint` and how paths are built.
- [C47.5 — Behaviours](05-behaviours.md): `AddBehaviour` — attaching jobs to actors.
- [C47.6 — Modding Placement & Behaviour](06-modding.md): moving spawns, new routes, new jobs.

---

## 47.1 Locators as anchors (✅ verified — C8)

Almost everything positioned in SHAR is placed at a **named locator** — a point (or group) baked
into the world (C8). Scripts refer to locators by name (`level1_carstart`, `w_lemon`,
`m0_apu_place`), never raw coordinates, so placement is data the artists set. [C47.1](01-locators.md).

## 47.2 Spawn points by locator script (✅ verified)

```
AddSpawnPointByLocatorScript("w_lemon","beecamera","Shelley","w_lemon","15.0","60");
```
Places an actor (here the wasp "Shelley"/`beecamera`) at a locator, with a trigger **range**
(`15.0`) and a parameter (`60`). This is the general "spawn X at locator Y when the player is
within R" primitive. [C47.2](02-spawn-points.md).

## 47.3 The wasps / bee cameras (✅ verified)

The `w_`-prefixed locators (`w_lemon`, `w_schoolroof1`, `w_bonuscar`, `w_stonetemple`,
`w_trailor1/2`, `w_cardguard`, `w_bridge1/2`, `w_barn`) are the **wasp** spawn points — the flying
"bee camera" enemies that attack you (tying to C31's wasp system and `ActorAnimationWasp`,
`AttackBehaviour`, C42). [C47.3](03-wasps.md).

## 47.4 Waypoints & routes (✅ verified)

`AddAmbientNPCWaypoint("eddie","eddie_walk1")` links an NPC to ordered waypoint locators; the NPC
walks the route. 55 such links in level 1 build the ambient foot-traffic. [C47.4](04-waypoints.md).

## 47.5 Behaviours (✅ verified)

`AddBehaviour( … )` (×25 in level 1) attaches a **behaviour** to an actor — the runtime
`AttackBehaviour`/`UFOAttackBehaviour`/AI-state machinery (C42/C25) — turning a placed actor into a
patrolling, reacting, or attacking one. [C47.5](05-behaviours.md).

## 47.6 Modding (✅ practical)

Move spawns to different locators, add waypoint routes, and attach behaviours — all in the level
script. [C47.6](06-modding.md).

---

## What this chapter established

- Specific actors are **placed at named locators** (C8) via `AddSpawnPointByLocatorScript`, with a
  trigger range — the mechanism behind the **wasps** (`w_*`).
- NPC movement is authored as **waypoint routes** (`AddAmbientNPCWaypoint`).
- Actors are given jobs with **`AddBehaviour`**, wiring them to the runtime behaviour/AI classes
  (C42/C25).

**Cross-references:** C8 (locators), C31 (wasps/police), C42 (behaviours/attacks/locomotion), C25
(AI), C45 (ped pools), C44 (level init), C14 (MFK).
