# Chapter 26 — Missions, Cameras & Physics at Runtime

> **Goal of this chapter:** close the runtime part of the book by decoding the three remaining pillars — the
> `Mission` class family (the runtime of C16), the `SuperCam` camera system, and the `sim::` physics engine
> — all from the verified RTTI set.

This chapter ties three subsystems to their disk-side chapters: missions (C16) become the `Mission` family,
the mission camera verbs (C14.6) become `SuperCam` subclasses, and the collision data (C11) plus vehicle/
character motion (C24/C25) run on the `sim::` physics engine. Every class is ✅ from `shar_dumps.csv`; offsets
are ⏳.

**Key finding (✅ verified) — a cross-validation.** The **20 objective types** extracted from the mission
scripts (C16.3) correspond to **21 `MissionObjective` subclasses** in the RTTI — the script vocabulary and the
runtime class set independently agree. The camera system is `SuperCam` with **18 subclasses** (bumper, chase,
follow, conversation, comedy, …); physics is the `sim::` namespace (**39 classes**) built on `sim::SimState`.

---

## Deep-dive pages

- [C26.1 — The `Mission` Runtime Family](01-mission-runtime.md): `Mission`, `MissionObjective`, `MissionCondition`.
- [C26.2 — Objectives & Conditions as Classes](02-objectives-as-classes.md): the 21/13 subclasses vs. the C16 vocabulary.
- [C26.3 — The `SuperCam` Family](03-supercam-family.md): the 18 camera types.
- [C26.4 — Camera Central & Switching](04-camera-central.md): `SuperCamCentral`, controllers, and the `*Data` split.
- [C26.5 — The `sim::` Physics System](05-sim-physics.md): `SimState`, physics objects, joints.
- [C26.6 — `sim::` Collision & the Frame](06-sim-collision-frame.md): volumes, the solver, and the per-frame loop.

---

## 26.1 The `Mission` runtime family (✅ verified)

The mission scripts (C16) build a verified class family:

```
Mission : EventListener                          — the running mission (an event listener, C23.3)
MissionObjective : EventListener                 — base objective (21 subclasses)
  ├ LoadVehicleObjective  (the getin/load-car objective, C24.5)
  └ … 20 more (one family per objective type, C16.3)
MissionCondition                                 — base condition (13 subclasses)
  └ VehicleCarryingStateProp  (the keepbarrel condition, C16.4)
```

A `Mission` is an `EventListener`: it reacts to game events to advance its stages (C16.2). [C26.1](01-mission-runtime.md).

## 26.2 Objectives & conditions as classes (✅ cross-validated)

The script-side vocabulary (C16) and the runtime class set independently agree:

| Script side (C16) | Count | Runtime side (RTTI) | Count |
|---|--:|---|--:|
| `AddObjective` types | 20 | `MissionObjective` subclasses | 21 |
| `AddCondition` types | 7 | `MissionCondition` subclasses | 13 |

The near-exact objective match (20 vs. 21) is strong mutual confirmation — the scripts and the executable
describe the same system from two independent evidence bases. [C26.2](02-objectives-as-classes.md).

## 26.3 The `SuperCam` family (✅ verified)

Every camera is a `SuperCam` subclass — 18 of them, verified:

```
SuperCam : tRefCounted, radLoadObject, IRefCount
  ├ BumperCam        — bumper/hood view
  ├ ChaseCam         — the default follow-behind driving camera
  ├ FollowCam        — follows the target
  ├ ConversationCam  — frames dialogue (SetConversationCam, C14.6)
  ├ AnimatedCam      — scripted keyframed camera (SetAnimatedCameraName, C14.6)
  ├ ComedyCam : WalkerCam — comedic framing
  └ DebugCam, WalkerCam, …
```

The mission camera verbs (C14.6) select and drive these. [C26.3](03-supercam-family.md).

## 26.4 Camera central & switching (✅ verified)

`SuperCamCentral` (`EventListener, GameDataHandler`) manages the active camera and switches between the
`SuperCam` subclasses; `SuperCamController` maps input to camera control. Each camera type has a `*Data`
companion (`ChaseCamData`, `ConversationCamData`, `BumperCamData`) carrying its tuning. [C26.4](04-camera-central.md).

## 26.5 The `sim::` physics system (✅ verified)

Physics lives in the `sim::` namespace (39 classes) on a verified base spine:

```
sim::SimState : tRefCounted, radLoadObject, IRefCount     (its tRefCounted subobject at offset 0 — RTTI ✅)
  sim::ManualSimState : sim::SimState
sim::SimulatedObject : tEntity                            — a thing physics moves
  sim::PhysicsObject → sim::ArticulatedPhysicsObject      — rigid & articulated bodies
sim::PhysicsJoint → sim::PhysicsJoint0D                   — joints/constraints
```

`Vehicle` and `Character` (C24/C25), as `DynaPhysDSG`, are simulated through this system. [C26.5](05-sim-physics.md).

## 26.6 `sim::` collision & the frame (✅ verified)

The collision data (C11) becomes `sim::` collision objects:

```
sim::CollisionObject : tEntity                            (the runtime of the 0x00121000 chunk, C11)
sim::CollisionVolume → BBoxVolume / OBBoxVolume / CylinderVolume   (the volume types of C11.5)
sim::CollisionManager, sim::CollisionDetector, sim::CollisionSolverAgent, sim::ImpulseBasedCollisionSolver
```

Each frame the manager runs broad- then narrow-phase, and the impulse solver resolves contacts.
[C26.6](06-sim-collision-frame.md).

---

## Key takeaways

- Missions run as `Mission : EventListener` with **21 `MissionObjective`** and **13 `MissionCondition`**
  subclasses — the 20/7 script vocabulary (C16) and the class set independently agree.
- Cameras are the **`SuperCam`** family (**18** subclasses), managed by `SuperCamCentral`, each with a
  `*Data` tuning companion; selected by the mission camera verbs (C14.6).
- Physics is the **`sim::`** namespace (**39** classes) on `sim::SimState`; `Vehicle`/`Character` are
  simulated as `DynaPhysDSG` bodies.
- The collision data of C11 becomes `sim::CollisionObject`/`CollisionVolume`, resolved each frame by the
  `sim::` collision manager and impulse solver.
- All classes ✅ from RTTI; offsets ⏳.

**This closes Part VII.** Next: [Chapter 27 — Save Data & `simpsons.ini`](../C27-Save-Config/C27-Save-Config.md).
