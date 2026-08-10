# C49.1 — What a Manager Is

> One sentence: a **manager** is a long-lived **singleton** that owns and drives exactly one
> subsystem of the game. Learn this once and all 43 make sense.

## The definition (✅ verified)
A manager is an object with three defining properties:
1. **Singleton** — there is exactly *one* of it, reached through a global accessor. There is one
   `RoadManager`, one `ChaseManager`, one `PedestrianManager`.
2. **Owner** — it *owns* its subsystem's objects: the `PedestrianManager` owns the live pedestrians,
   the `CoinManager` owns the coins, the `MissionManager` owns the active mission. It allocates them
   (usually from a pool, C39) and frees them.
3. **Driver** — it *updates* its subsystem every frame (spawn, move, retire, react).

If a class name ends in `Manager` (and a few that don't — `VehicleCentral`, `SuperCamCentral`,
`CGuiSystem`), it is one of these.

## What it is *not*
- Not the objects themselves. `PedestrianManager` is not a pedestrian; it *owns* the
  `Pedestrian`/`Character` objects (C25/C45).
- Not per-instance. There's one manager, many managed objects.

## The mental model
Think of each manager as the **department head** for its domain: the traffic department
(`TrafficManager`), the police department (`ChaseManager`), the roads department (`RoadManager`).
Ask the department head about anything in its domain; it knows because it owns it.

## Why this matters for you
Because a manager is *the* access point and *the* owner, it is where you go to read or change
anything in a subsystem — and where the SDK's `shar::identify` will point you when you find one live
(C28.7). Understanding "it's a manager" tells you how to find it, what it holds, and how to hook it.

## Cross-references
C49.2 (how it works), C49.4 (the catalogue), C25/C45 (managed objects), C28.7 (finding one live).
