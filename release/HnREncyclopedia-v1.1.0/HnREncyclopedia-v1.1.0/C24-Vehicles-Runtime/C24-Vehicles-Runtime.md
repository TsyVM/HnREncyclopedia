# Chapter 24 — Vehicles at Runtime

> **Goal of this chapter:** connect the `.con` handling values (C15) to the live vehicle they configure —
> the verified `Vehicle` class, its controllers, and its manager — and show how a car goes from a text file
> and a mesh to a driven, colliding, sounding object.

Vehicles are where the disk-side chapters converge: a mesh (C7), a `.con` handling script (C15), a driver
(C25), collision (C11), physics (C26), and sound (C19) all meet in one runtime object. This chapter reads
that object from the verified RTTI set — every class name and inheritance chain below is ✅ from
`shar_dumps.csv`; member offsets are ⏳.

**Key finding (✅ verified):** `Vehicle : DynaPhysDSG, StaticPhysDSG, CollisionEntityDSG, IEntityDSG` — a
car is a dynamic, physical, collidable, drawable scene entity (the DSG spine of C23.2). Driving is factored
into a **controller** hierarchy: one `VehicleController` base with **human** and **AI** subclasses, so the
same `Vehicle` is driven by the player or the AI depending only on which controller is attached.

---

## Deep-dive pages

- [C24.1 — The `Vehicle` Class](01-the-vehicle-class.md): the DSG/physics base and what a car *is* at runtime.
- [C24.2 — Controllers: Human vs. AI](02-controllers.md): `VehicleController`, `HumanVehicleController`, `AiVehicleController`, `VehicleAI`.
- [C24.3 — `VehicleCentral` & Traffic](03-central-traffic.md): the manager and `TrafficVehicle`.
- [C24.4 — From CON to the Live Car](04-con-to-runtime.md): how C15 values reach the object (offsets ⏳).
- [C24.5 — Sound & Mission Integration](05-sound-mission.md): `AIVehicleSoundPlayer`, `LoadVehicleObjective`.

---

## 24.1 The `Vehicle` class (✅ verified)

A car's runtime type, with its verified bases:

```
Vehicle : DynaPhysDSG, StaticPhysDSG, CollisionEntityDSG, IEntityDSG
```

Every base is a link in the DSG spine (C23.2): `IEntityDSG` (in the scene graph, C10), `CollisionEntityDSG`
(solid, C11), `DynaPhysDSG` (physically simulated, C26). So a `Vehicle` is drawn, collides, and is pushed by
physics through the *same* machinery as every other world entity — it just adds vehicle-specific behaviour on
top. This shared base is why a car and a character (which has the identical bases, C25) interact so
naturally. [C24.1](01-the-vehicle-class.md).

## 24.2 Controllers: human vs. AI (✅ verified)

Driving is a separate hierarchy from the vehicle itself:

```
VehicleController (base)
  ├ HumanVehicleController      — the player
  └ AiVehicleController
        └ VehicleAI             — full AI driver
```

The `Vehicle` holds a controller; swapping the controller swaps *who drives* without changing the car. This
is why `SuppressDriver` (C12.5) and `LoadDisposableCar(..., "AI")` (C14.2) work — they decide which
controller a car gets. [C24.2](02-controllers.md).

## 24.3 `VehicleCentral` & traffic (✅ verified)

`VehicleCentral` (a `LoadingManager::ProcessRequestsCallback`) is the vehicle **manager** — it loads and
tracks cars. `TrafficVehicle` is the ambient-traffic vehicle type that fills the roads (C13, via
`SetMaxTraffic`, C14.5). Together they run the population of cars the road network drives. [C24.3](03-central-traffic.md).

## 24.4 From CON to the live car (✅ path / ⏳ offsets)

The `.con` handling values (C15 — `SetMass`, `SetTopSpeedKmh`, `SetTireGrip`, …) are loaded into the
`Vehicle`'s handling/physics members at construction. The **class is verified**; the **exact member offset**
each `Set…` writes is ⏳, recovered by the diff method (C4.3): change one `.con` value, watch which member of
the live `Vehicle` moves. [C24.4](04-con-to-runtime.md).

## 24.5 Sound & mission integration (✅ verified)

A car's audio runs through `AIVehicleSoundPlayer` / `AvatarVehiclePosnPlayer` (positional vehicle sound,
from `carsound.rcf`, C19). Missions integrate vehicles via `LoadVehicleObjective : MissionObjective` (the
runtime of `LoadDisposableCar` + the `getin` objective, C16) and `VehicleCarryingStateProp : MissionCondition`
(the `keepbarrel` condition, C16.4). [C24.5](05-sound-mission.md).

---

## Key takeaways

- `Vehicle : DynaPhysDSG, StaticPhysDSG, CollisionEntityDSG, IEntityDSG` — a car is a physical, collidable,
  drawable scene entity on the DSG spine (C23.2), sharing its base with `Character` (C25).
- Driving is a separate **controller** hierarchy: `HumanVehicleController` (player) vs.
  `AiVehicleController`/`VehicleAI` — swap the controller to swap the driver.
- `VehicleCentral` manages cars; `TrafficVehicle` is ambient traffic.
- `.con` values (C15) load into `Vehicle` members — class ✅, offsets ⏳ (diff to find them, C4.3).
- Vehicles integrate with sound (C19) and missions (`LoadVehicleObjective`, C16) through verified classes.

**Next:** [Chapter 25 — Characters & AI](../C25-Characters-AI/C25-Characters-AI.md).
