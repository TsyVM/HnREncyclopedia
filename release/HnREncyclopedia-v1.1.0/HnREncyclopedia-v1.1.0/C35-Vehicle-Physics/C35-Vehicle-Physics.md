# Chapter 35 — Vehicle Physics, Drifting & Destruction

> **Goal of this chapter:** decode the *runtime* physics behind a car — the engine state machine that makes
> it idle, drive, drift, and fly; the skidmarks and suspension; the `sim::` rigid body underneath; and the
> breakable objects (glass, fences) it smashes through. Chapter 15 gave the CON *parameters*; this is the
> *machine* those parameters configure.

Chapter 15 documented the `.con` knobs (`SetTireGrip`, `SetSlipSteering`, `SetSpringK`…); Chapter 26 gave the
`sim::` base. This chapter is the vehicle-specific runtime *between* them — how a car actually drives, slides,
jumps, and crashes, decoded from the verified RTTI set (all classes with confirmed vtable addresses).

**Key finding (✅ verified):** a vehicle's dynamics run through an **engine state machine** — `IdleEngineState`,
`NormalEngineState`, **`SkidEngineState`** (drifting/sliding), **`InAirEngineState`** (jumping),
`ReverseEngineState`, and gear states (`Upshift`/`DownshiftEngineState`) — leaving **`Skidmark`s**, sprung by
`SuspensionJointDriver`, on a `sim::` rigid body. It smashes **`BreakableObjectDSG`** objects (glass, props)
managed by `BreakablesManager`.

---

## Deep-dive pages

- [C35.1 — The Engine State Machine](01-engine-state-machine.md): idle, drive, skid, air, reverse, gears.
- [C35.2 — Drifting & Skidmarks](02-drifting-skidmarks.md): `SkidEngineState`, `Skidmark`, the slip model (C15.3).
- [C35.3 — Jumps & Air Control](03-jumps-air.md): `InAirEngineState` — what happens when a car leaves the ground.
- [C35.4 — Suspension, Rigid Body & Gravity](04-suspension-rigidbody.md): `SuspensionJointDriver`, `sim::` physics.
- [C35.5 — Breakables & Destruction](05-breakables.md): `BreakableObjectDSG`, glass, and smashing through.

---

## 35.1 The engine state machine (✅ verified)

A vehicle's drive behaviour is a **finite state machine** of engine states — each a distinct driving regime:

```
IdleEngineState      (0x0060A5D0)  — stopped/idling
NormalEngineState    (0x0060A5A0)  — driving normally (gripping)
SkidEngineState      (0x0060A5B8)  — sliding/drifting (broken traction — C35.2)
InAirEngineState     (0x0060A600)  — airborne (a jump — C35.3)
ReverseEngineState   (0x0060A5E8)  — reversing
UpshiftEngineState   (0x0060A588) / DownshiftEngineState (0x0060A570)  — gear changes
```

The car is always in one engine state; transitions follow the driving: brake and turn hard → `SkidEngineState`
(you're drifting); hit a ramp → `InAirEngineState` (you're jumping); land and regain grip → `NormalEngineState`.
Each state applies different physics — grip vs. slide, ground vs. air — which is why a drift *feels* different
from normal driving. [C35.1](01-engine-state-machine.md).

## 35.2 Drifting & skidmarks (✅ verified)

Drifting is the **`SkidEngineState`** — entered when the tyres break traction (hard cornering, handbrake, the
`.con` slip model of C15.3). While skidding, the car slides, steers by the slip parameters (`SetSlipSteering`,
`SetEBrakeEffect`, C15.3), and lays down **`Skidmark`s** (0x00607730) — the black tyre marks on the road. So
the CON slip params (C15.3) *configure* the `SkidEngineState`. [C35.2](02-drifting-skidmarks.md).

## 35.3 Jumps & air control (✅ verified)

When a car leaves the ground (a ramp, a hill), it enters **`InAirEngineState`** (0x0060A600). Airborne, the
wheels have no grip, so the physics changes: no drive or steering from the tyres, gravity pulls it down, and
the `.con` weeble bias (`SetWeebleOffset`, C15.4) helps it land upright. This is also where the **jump camera
effect** (C36) triggers — the camera reacts to the car going airborne. [C35.3](03-jumps-air.md).

## 35.4 Suspension, rigid body & gravity (✅ verified)

Under the engine states sits the `sim::` rigid body (C26.5). The wheels connect to the body through
**`SuspensionJointDriver`** (0x006084BC) — a physics joint that springs and damps per the `.con`
(`SetSpringK`/`SetDamperC`/`SetSuspensionLimit`, C15.4). `sim::PhysicsObject`/`ArticulatedPhysicsObject`,
`sim::PhysicsJoint0D/1D/3D`, and `sim::SimEnvironment` (which holds gravity) are the substrate.
[C35.4](04-suspension-rigidbody.md).

## 35.5 Breakables & destruction (✅ verified)

When a car smashes through glass, a fence, or a prop, that object is a **`BreakableObjectDSG`** (0x0060C664),
managed by **`BreakablesManager`** (0x0060B758) and loaded by `BreakableObjectLoader`. On impact it breaks —
spawning debris (particles, C33.4) and often a camera shake (C36). This is the "smash through the window"
moment. [C35.5](05-breakables.md).

---

## Key takeaways

- A vehicle's dynamics are an **engine state machine**: `Idle`/`Normal`/`Skid`(drift)/`InAir`(jump)/`Reverse`
  + gear states — each applies different physics.
- **Drifting** is `SkidEngineState`, configured by the CON slip params (C15.3), leaving `Skidmark`s.
- **Jumping** is `InAirEngineState` — no tyre grip, gravity, weeble-assisted landing (C15.4); triggers the
  jump camera (C36).
- **Suspension** is `SuspensionJointDriver` (a physics joint) on the `sim::` rigid body (C26.5); gravity is in
  `sim::SimEnvironment`.
- **Smashing glass/props** is the `BreakableObjectDSG`/`BreakablesManager` system, with debris + camera shake.
- All classes ✅ verified with ✅ vtable addresses; member offsets ⏳ (the CON→member map, C24.4).

**Next:** [Chapter 36 — Cameras & Camera Effects](../C36-Cameras-Effects/C36-Cameras-Effects.md).
