# Chapter 46 — Traffic

> **Goal of this chapter:** decode the moving traffic — the AI cars that drive Springfield's
> roads. What a **traffic group** is, how cars are spawned onto the road network and driven, how
> the cap works, and how to change the mix. We named traffic before; this is the system.

The streets aren't empty: minivans, pickups, school buses, and glass trucks drive the roads,
giving you something to dodge (and smash for Hit & Run, C31). Like the crowd (C45), traffic is a
**pool-and-spawn** system set up in the level init (C44) and driven along the road network.

**Key finding (✅ verified):** traffic comes from **traffic groups** built in `leveli.mfk`:
`CreateTrafficGroup( N )` opens group N, `AddTrafficModel( "model", weight[, flag] )` adds a vehicle
model with a spawn weight (and an optional flag, e.g. `AddTrafficModel("glastruc",1,1)`), and
`CloseTrafficGroup( )` finalizes it. `SetMaxTraffic( N )` caps how many traffic cars exist at once
(lowered during missions/races, e.g. `SetMaxTraffic(2)`). At runtime these are `TrafficVehicle`
objects driven by `TrafficLocomotion` along the road/path network (`RoadManager`/`PathManager`,
C13) — all confirmed classes, and `TrafficVehicle` was caught live by the bundled diagnostic.

---

## Deep-dive pages

- [C46.1 — What a Traffic Group Is](01-traffic-groups.md): `CreateTrafficGroup`/`AddTrafficModel`/`CloseTrafficGroup`.
- [C46.2 — Spawning onto the Road Network](02-spawning.md): how cars appear on roads and recycle (C13).
- [C46.3 — Driving: `TrafficVehicle` & `TrafficLocomotion`](03-driving.md): how a traffic car follows the road.
- [C46.4 — The Traffic Cap (`SetMaxTraffic`)](04-cap.md): the limit, and why missions lower it (C39).
- [C46.5 — Traffic & Hit & Run](05-hit-and-run.md): smashing traffic, the police interaction (C31).
- [C46.6 — Modding Traffic](06-modding.md): changing the vehicle mix, density, and behaviour.

---

## 46.1 What a traffic group is (✅ verified)

```
CreateTrafficGroup( 0 );
AddTrafficModel( "minivanA", 2 );
AddTrafficModel( "glastruc", 1, 1 );
AddTrafficModel( "schoolbu", 1, 1 );
AddTrafficModel( "pickupA",  1 );
CloseTrafficGroup( );
```
A **traffic group** is a weighted pool of *vehicle* models (the road analogue of a ped group,
C45). The weight biases how often each model spawns; the optional third arg is a flag (🟡 — likely
a size/lane or special-handling marker, e.g. for large vehicles like the glass truck and bus).
[C46.1](01-traffic-groups.md).

## 46.2 Spawning onto the road network (✅ mechanism)

Traffic spawns on the **road/path network** (C13) ahead of and around the player, drawing from the
active group, and despawns when far behind — the same moving-bubble idea as the crowd (C45.2), but
constrained to roads. [C46.2](02-spawning.md).

## 46.3 Driving (✅ verified classes)

A live traffic car is a `TrafficVehicle` driven by `TrafficLocomotion` — it follows the road
network's lanes/paths (`RoadManager`/`PathManager`) rather than being player-controlled.
`TrafficVehicle` was observed live in the diagnostic capture. [C46.3](03-driving.md).

## 46.4 The cap (✅ verified)

`SetMaxTraffic( N )` bounds concurrent traffic. The init sets a base (e.g. 4); missions and races
**lower** it (`SetMaxTraffic(2)`) so traffic doesn't interfere. This is the script-tier limit of
C39.2. [C46.4](04-cap.md).

## 46.5 Traffic & Hit & Run (✅ verified — C31)

Smashing traffic and causing chaos feeds the Hit & Run meter and the police response (C31).
Traffic is both obstacle and target. [C46.5](05-hit-and-run.md).

## 46.6 Modding (✅ practical)

Change the model mix and weights per group, raise/lower `SetMaxTraffic`, or hook `TrafficVehicle`
to alter behaviour. [C46.6](06-modding.md).

---

## What this chapter established

- Traffic is a **weighted pool** (traffic groups) set up in level init, spawned onto the **road
  network** (C13), and driven by `TrafficVehicle`/`TrafficLocomotion`.
- `SetMaxTraffic` is the concurrent cap (script-tier, lowered for missions/races).
- Traffic ties into Hit & Run and the police (C31), and into the engine's vehicle/actor limits (C39).

**Cross-references:** C44 (level init), C13 (roads/paths), C24/C35 (vehicles), C31 (Hit & Run/
police), C39 (`SetMaxTraffic` limit), C45 (the crowd analogue), C14 (MFK).
