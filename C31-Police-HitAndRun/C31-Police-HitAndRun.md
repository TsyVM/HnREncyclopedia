# Chapter 31 — Police, Hit & Run & Wasps

> **Goal of this chapter:** decode the game's enforcement systems — the **Hit & Run meter** that summons the
> police, the **chase** that pursues you, and the **wasp cameras** that watch you. These are what make SHAR's
> open world have consequences.

The game is named for it: cause enough mayhem and you trigger a **Hit & Run** pursuit. This chapter decodes
that system from the verified RTTI set (all classes now with confirmed vtable addresses): the meter, the
manager that spawns police, the AI that chases you, and the wasp surveillance cameras — the closest thing
SHAR has to a "wanted level."

**Key finding (✅ verified):** the pursuit system is a small set of dedicated classes — **`HitnRunManager`**
(the meter), **`ChaseManager`** (spawns police, a `SpawnManager`), **`ChaseAI`** (the pursuit driver, a
`VehicleAI`), **`ChaseCam`** (the pursuit camera), **`HudHitNRun`** (the meter HUD), and
**`NoCopBonusObjective`** (a "stay clean" bonus) — plus the **wasp cameras** (`ActorAnimationWasp`,
`WaspSoundPlayer`, `HudWaspDestroyed`). The `SetHitNRun` script command (78 uses, C14) tunes it per mission.

---

## Deep-dive pages

- [C31.1 — The Hit & Run Meter](01-the-meter.md): `HitnRunManager`, `HudHitNRun`, how the meter fills.
- [C31.2 — The Chase](02-the-chase.md): `ChaseManager`, `ChaseAI`, `ChaseCam`, and the police cars.
- [C31.3 — The Wasp Cameras](03-the-wasps.md): `ActorAnimationWasp`, the surveillance drones.
- [C31.4 — Scripting Pursuit](04-scripting-pursuit.md): `SetHitNRun`, `NoCopBonusObjective`, per-mission control.
- [C31.5 — Modding the Police](05-modding-police.md): tuning aggression, the chase car, and the meter.

---

## 31.1 The Hit & Run meter (✅ verified)

The **Hit & Run meter** is the game's "heat." Its runtime:

```
HitnRunManager : EventListener   (0x00608D3C)  — tracks your mayhem, fills the meter, triggers the chase
HudHitNRun : HudEventHandler     (0x0060DBDC)  — the on-screen meter
```

As you commit "hit and run" acts — smashing traffic, property, and pedestrians — `HitnRunManager` fills the
meter (shown by `HudHitNRun`). When it maxes, the police are summoned (C31.2). Stop causing mayhem and it
cools down. [C31.1](01-the-meter.md).

## 31.2 The chase (✅ verified)

When the meter triggers, the pursuit spawns:

```
ChaseManager : SpawnManager  (0x006077FC)  — spawns police/chase vehicles
ChaseAI : VehicleAI          (0x00615F60)  — drives them in pursuit (C24.2)
ChaseCam : SuperCam          (0x006154B4)  — frames the chase (C26.3)
```

`ChaseManager` spawns police cars — e.g. the verified roster entry **`cBlbart` "Black Ferrini (Chase)"** —
driven by `ChaseAI` (a `VehicleAI`, C24.2) that hunts the player over the road network (C13). `ChaseCam`
frames the pursuit. Ram them or outrun them to lose the chase. [C31.2](02-the-chase.md).

## 31.3 The wasp cameras (✅ verified)

The **wasps** are Springfield's surveillance drones — flying camera robots scattered across each level:

```
ActorAnimationWasp : ActorAnimation   (0x00615D0C)  — the wasp actor
WaspSoundPlayer : ActorPlayer         (0x00608D94)  — its sound
HudWaspDestroyed : HudEventHandler    (0x0060DB40)  — the "wasp destroyed" HUD feedback
```

Wasps are collectible *targets* — destroy all of a level's wasps for a reward, tracked by `HudWaspDestroyed`.
They are the map's `harascar`/surveillance markers (C29.3). [C31.3](03-the-wasps.md).

## 31.4 Scripting pursuit (✅ verified)

Missions control the pursuit through script: **`SetHitNRun(...)`** (78 uses, C14) tunes whether and how the
meter operates in a mission, and **`NoCopBonusObjective`** (0x00611958, a `BonusObjective`) rewards
completing a mission without triggering the cops. [C31.4](04-scripting-pursuit.md).

## 31.5 Modding the police (✅ path)

Because the police are a `Vehicle` (the chase car, C24.1) driven by `ChaseAI` and spawned by `ChaseManager`,
you can tune pursuit: edit the chase car's `.con` (C15) for its handling, adjust `SetHitNRun` (C14) per
mission, and — natively — identify `ChaseAI`/`HitnRunManager` by their now-verified vtables (C23.5) to reach
their state. [C31.5](05-modding-police.md).

---

## Key takeaways

- SHAR's "wanted level" is the **Hit & Run meter** (`HitnRunManager` + `HudHitNRun`): mayhem fills it,
  triggering a police chase.
- The **chase** is `ChaseManager` (spawns police, a `SpawnManager`) + `ChaseAI` (a `VehicleAI` pursuit
  driver) + `ChaseCam`; the police car is a normal `Vehicle` (e.g. `cBlbart` "Black Ferrini (Chase)").
- **Wasps** (`ActorAnimationWasp`) are destroyable surveillance drones with their own HUD tracking.
- Missions tune it via **`SetHitNRun`** (78 uses) and reward avoidance via **`NoCopBonusObjective`**.
- All classes ✅ verified with ✅ vtable addresses; member offsets ⏳.

**Next:** the [Legend](../Legend/README.md) — the named vehicles, characters, missions, and levels.
