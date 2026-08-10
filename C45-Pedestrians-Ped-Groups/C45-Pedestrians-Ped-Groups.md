# Chapter 45 — Pedestrians & Ped Groups

> **Goal of this chapter:** decode the crowd — how Springfield fills with wandering people, what a
> **ped group** actually is, how ambient named characters (Apu, Lisa) differ from the anonymous
> crowd, and how the whole population is authored in the level init. We referenced "PedGroups"
> before; this is what they are.

Springfield feels alive because the streets are full of pedestrians — nameless townsfolk plus
recognizable characters going about their business. That crowd is not hand-placed; it's a
**pool-and-spawn** system driven by the level init (C44).

**Key finding (✅ verified):** pedestrians come from numbered **ped groups** built in `leveli.mfk`:
`CreatePedGroup( N )` opens group N, a series of `AddPed( "model", weight )` adds pedestrian models
with a spawn weight, and `ClosePedGroup( )` finalizes it. The crowd system then spawns peds around
the player by drawing from these groups (weighted). **Named ambient characters** are separate:
`AddAmbientCharacter( "apu", "m0_apu_place", 1.8 )` places a specific NPC (often in an interior,
C41) with a spawn radius; their **wander paths** are `AddAmbientNPCWaypoint( "ped", "waypoint" )`
(×55 in level 1). At runtime peds are `Character`/`NPCharacter`/`Pedestrian` objects (C25) managed
by a `CharacterManager`; on-foot motion uses the locomotion sets of C42.4.

---

## Deep-dive pages

- [C45.1 — What a Ped Group Is](01-ped-groups.md): `CreatePedGroup`/`AddPed`/`ClosePedGroup` and the weighted pool.
- [C45.2 — The Crowd Spawn System](02-crowd-spawn.md): how peds appear around the player and recycle.
- [C45.3 — Ambient Named Characters](03-ambient-characters.md): `AddAmbientCharacter` — Apu, Lisa, and friends.
- [C45.4 — Wander Waypoints](04-waypoints.md): `AddAmbientNPCWaypoint` and how NPCs move.
- [C45.5 — Peds at Runtime](05-runtime.md): `Character`/`NPCharacter`/`CharacterManager`, locomotion, reactions.
- [C45.6 — Modding the Crowd](06-modding.md): changing who spawns, density, and behaviour.

---

## 45.1 What a ped group is (✅ verified)

```
CreatePedGroup( 0 );
AddPed( "male6", 2 );
AddPed( "girl4", 1 );
AddPed( "fem4",  2 );
AddPed( "boy3",  2 );
ClosePedGroup( );
```
A **ped group** is a numbered, weighted **pool of pedestrian models**. The second arg to `AddPed`
is the spawn weight (how often that model appears relative to others). Level 1 defines several
groups (0, 1, …), so different areas/moments draw different crowds. [C45.1](01-ped-groups.md).

## 45.2 The crowd spawn system (✅ mechanism)

The engine spawns a budgeted number of peds near the player from the active group, despawning ones
that fall behind, so the crowd density stays roughly constant as you move. Density is bounded by
the actor pool (C44.4/C39). [C45.2](02-crowd-spawn.md).

## 45.3 Ambient named characters (✅ verified)

```
AddAmbientCharacter("apu",  "m0_apu_place", 1.8);   // Kwik-E-Mart interior
AddAmbientCharacter("lisa", "m1_lisa_place", 1.3);  // school interior
```
Named NPCs placed at a locator with a radius — distinct from the anonymous crowd. Often bound to
interiors (C41). [C45.3](03-ambient-characters.md).

## 45.4 Wander waypoints (✅ verified)

`AddAmbientNPCWaypoint("eddie","eddie_walk1")` — 55 in level 1 — defines the paths ambient NPCs
walk between, giving them purposeful movement rather than random drift. [C45.4](04-waypoints.md).

## 45.5 Peds at runtime (✅ verified — C25)

Live peds are `Character`/`NPCharacter`/`Pedestrian` objects under a `CharacterManager`; they walk
via locomotion sets (C42.4) and react to the player (flee the car, get kicked, C42.2). [C45.5](05-runtime.md).

## 45.6 Modding (✅ practical)

Change which models populate a group, their weights, density (via the actor pool), and add/replace
named ambient NPCs — all in `leveli.mfk`. [C45.6](06-modding.md).

---

## What this chapter established

- The crowd is a **weighted pool system**: numbered **ped groups** of models built in level init,
  spawned around the player.
- **Named ambient characters** are placed individually (often in interiors) with wander waypoints.
- At runtime peds are `Character`/`NPCharacter` objects (C25) moving on locomotion sets (C42.4),
  bounded by the actor pool (C44.4/C39).

**Cross-references:** C44 (level init), C25 (characters/AI), C42.4 (locomotion), C41 (interior
NPCs), C47 (waypoints/behaviours), C39 (actor limits), C14 (MFK).
