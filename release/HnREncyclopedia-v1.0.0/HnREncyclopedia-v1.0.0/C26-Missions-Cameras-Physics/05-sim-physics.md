# C26.5 — The `sim::` Physics System

**What it is.** The physics engine — the `sim::` namespace (39 classes) that moves every dynamic object:
cars, characters, ragdolls, and debris. It is what turns the handling numbers of a `.con` (C15/C24.4) and the
forces of a collision (C11) into motion.

**How it works (✅ verified).** The `sim::` base spine, from `shar_dumps.csv`:

```
sim::SimState : tRefCounted, radLoadObject, IRefCount
  └ sim::ManualSimState : sim::SimState
sim::SimulatedObject : tEntity, tRefCounted, …            — an object physics simulates
  └ sim::PhysicsObject
       └ sim::ArticulatedPhysicsObject                    — multi-part / jointed bodies
sim::PhysicsJoint
  └ sim::PhysicsJoint0D                                    — a joint/constraint
sim::VirtualCM / sim::JointVirtualCM                       — virtual centre-of-mass
```

`sim::SimState` is the physics state of a simulated thing (its position, velocity, and the rest of what the
integrator advances each frame). `sim::SimulatedObject` is something the physics moves; `sim::PhysicsObject`
and `sim::ArticulatedPhysicsObject` are rigid and jointed bodies. The `sim::PhysicsJoint` family are the
constraints (a hinge, a ragdoll joint). Notably, the RTTI proves `sim::SimState`'s `tRefCounted` sub-object
sits at **offset 0** (C23.1) — a verified layout fact, in contrast to the ⏳ data-member offsets.

**How vehicles and characters plug in.** `Vehicle` and `Character` are `DynaPhysDSG` (C24.1/C25.1), and
`DynaPhysDSG` is the scene-graph face of a `sim::` physics body. So driving a car is: the controller (C24.2)
sets drive/steer inputs → the `.con`-tuned handling (C24.4) turns them into forces → the `sim::` physics body
integrates them into motion → the `DynaPhysDSG` entity moves in the scene graph (C10). A character ragdoll
(`CharacterAi::InSim`, C25.2) is the character's `sim::` body taking over from animation. One physics engine
serves both, because both are `DynaPhysDSG` on the same spine (C23.2).

**Why a general physics engine.** SHAR needs believable cars, tumbling ragdolls, jointed objects (articulated
props, the "weeble" self-righting of C15.4), and debris — all interacting. A general `sim::` engine with
rigid bodies, joints, and a shared state representation handles all of it with one integrator and one solver
(C26.6), rather than special-case code per object type. The `.con` (C15) and the character rig (C8) are
*configurations* of this one engine — which is why tuning a car's suspension (C15.4) and a character's balance
(C8.1) both ultimately feed `sim::`.

**What happens if you bend it.**

- *Rely on a `sim::` data-member offset* — the class hierarchy and base sub-object offsets are ✅, but data
  members (velocity, mass) are ⏳. Diff (C4.3).
- *Set physics-affecting `.con` values to extremes* — the `sim::` integrator can go unstable (cars launching,
  jittering). Change mass/spring/damper (C15.4) in small steps.
- *Expect animation and physics to be the same system* — animation poses the skeleton (C8/C25.4); `sim::`
  moves the body. Ragdoll (`InSim`) is the hand-off between them.
