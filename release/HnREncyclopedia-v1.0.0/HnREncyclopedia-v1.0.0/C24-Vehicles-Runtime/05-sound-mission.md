# C24.5 — Sound & Mission Integration

**What it is.** The two systems a `Vehicle` plugs into beyond driving: **audio** (engine and positional
sound) and **missions** (a car as a mission objective or condition). Both are verified classes that connect
the vehicle to the wider game.

**How it works — sound (✅ verified).** A car's audio runs through a positional sound-player hierarchy:

```
AIVehicleSoundPlayer     : VehiclePositionalSoundPlayer, PositionCarrier
AvatarVehiclePosnPlayer  : VehiclePositionalSoundPlayer, PositionCarrier, EventListener
```

These play the vehicle's engine and effect sounds — sourced from `carsound.rcf` (C19) — positioned in 3-D so
a passing car sounds like it's passing. `PositionCarrier` ties the sound to the car's world position; the
`AI` vs. `Avatar` split mirrors the controller split (C24.2): AI/traffic cars and the player's car get their
own sound players. This is how the streets *sound* alive, not just look it — every `TrafficVehicle` (C24.3)
carries a positional engine sound.

**How it works — missions (✅ verified).** Vehicles integrate with the mission system (C16) through dedicated
mission classes:

```
LoadVehicleObjective : MissionObjective, EventListener      — the runtime of "get in / load this car"
VehicleCarryingStateProp : MissionCondition, EventListener  — the "keepbarrel" condition (C16.4)
```

`LoadVehicleObjective` is the objective that loads and requires a specific vehicle — the runtime of
`LoadDisposableCar` (C14.2) plus the `getin` objective (C16.3). `VehicleCarryingStateProp` is a *condition*
that watches a car's carried cargo — the `keepbarrel` failure condition (C16.4). So the mission vocabulary you
decoded from scripts (C16) has verified runtime classes here, and they are `EventListener`s (C23.3) — they
react to vehicle events (entered, damaged, cargo lost) to advance or fail a stage.

**Why vehicles touch so many systems.** A car in SHAR is rarely *just* transport — it's a mission objective
(deliver, chase), a sound source, a physics body, and a collidable entity, often at once. The runtime reflects
that: the `Vehicle` (C24.1) is the physical core, and a web of companion classes (controllers C24.2, sound
players here, mission objectives/conditions here) attach the car to driving, audio, and gameplay. This is the
event-driven design of C23.3 in action — the car emits events, and listeners across subsystems react.

**The full runtime picture of a car.** Putting the chapter together: a `Vehicle` (C24.1) is built by
`VehicleCentral` (C24.3) from a mesh (C7) and a `.con` (C24.4), driven by a `HumanVehicleController` or
`AiVehicleController` (C24.2), simulated by `sim::` physics (C26), made solid by collision (C11), sounded by a
`VehiclePositionalSoundPlayer` (here), and — when a mission needs it — required by a `LoadVehicleObjective`
(here). Every one of those classes is ✅ verified; the offsets that wire them are ⏳.

**What happens if you bend it.**

- *Change a car's mesh but expect its sound to follow* — sound is a separate player from `carsound.rcf`
  (C19); edit the audio to change how it sounds.
- *Rely on a mission/sound class offset* — the classes are ✅, offsets ⏳. Diff (C4.3).
- *Assume a mission car is special* — it's a normal `Vehicle` (C24.1) with a `LoadVehicleObjective` attached.
  Edit the vehicle as usual; the mission integration is a separate class.

**Next:** [Chapter 25 — Characters & AI](../C25-Characters-AI/C25-Characters-AI.md).
