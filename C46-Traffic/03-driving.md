# C46.3 — Driving: `TrafficVehicle` & `TrafficLocomotion`

> How a traffic car actually moves: as a dedicated AI vehicle following the road, not a
> player-style car.

## The classes (✅ verified)
- **`TrafficVehicle`** — the live traffic car object. It was caught live by the bundled diagnostic
  (its vtable pointer identified real instances on the heap), confirming the class drives the
  on-road cars.
- **`TrafficLocomotion`** — the locomotion variant (C42.4) that moves a traffic vehicle along its
  lane/path, distinct from player `VehicleLocomotion` and on-foot `PhysicsLocomotion`.
- **`RoadManager` / `PathManager`** — own the road/path network the traffic follows (C13); both
  were live in the diagnostic capture.

## How it drives
A `TrafficVehicle` is assigned a lane/path from the network and advances along it via
`TrafficLocomotion`, obeying intersections and stopping/yielding as the simple traffic AI dictates.
It is *not* simulated with the full player-vehicle physics (C35) — traffic uses a lighter,
path-following model, which is why traffic cars handle differently from the player's car.

## Why a separate, lighter model
Dozens of cars can't each run the full vehicle sim affordably. A path-following locomotion is cheap
and good enough for background traffic, reserving the heavy physics (C35) for the player and
mission vehicles.

## What happens if you bend it
Hook `TrafficVehicle`/`TrafficLocomotion` (confirmed vtables) to change traffic behaviour (speed,
aggression). Read live instances via the diagnostic/`shar::identify` (C28.7).

## Cross-references
C42.4 (locomotion), C13 (road/path network), C35 (the heavier player-vehicle sim), C28.7 (live identify).
