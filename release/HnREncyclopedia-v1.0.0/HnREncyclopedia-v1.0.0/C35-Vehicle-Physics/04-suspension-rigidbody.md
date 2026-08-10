# C35.4 — Suspension, Rigid Body & Gravity

**What it is.** The physics substrate under the engine states (C35.1): the `sim::` rigid body the car *is*,
the suspension joint connecting its wheels to its body, and the environment (gravity) it falls through. This
is where the vehicle meets the general physics engine (C26.5).

**How it works (✅ verified).** A car is a `sim::` rigid body with sprung wheels:

```
SuspensionJointDriver (0x006084BC)  — springs/damps each wheel to the body (a physics joint driver)
sim::PhysicsObject / sim::ArticulatedPhysicsObject  — the rigid body (C26.5)
sim::PhysicsJoint0D / 1D / 3D       — joints/constraints (the suspension is a joint)
sim::PhysicsProperties (0x005F33B0) — mass, inertia, and the physical properties
sim::SimEnvironment (0x005F3670)    — the world's physics environment (gravity)
sim::SimUnitsManager                — the unit/scale system
```

The car's body is a `sim::PhysicsObject` (C26.5); its wheels connect through
**`SuspensionJointDriver`** — a driver that applies spring and damper forces (per the `.con`
`SetSpringK`/`SetDamperC`/`SetSuspensionLimit`, C15.4) to push the body up off the wheels and absorb bumps. So
the `.con` suspension params (C15.4) *tune* this joint driver. **`sim::PhysicsProperties`** holds the car's
mass (`SetMass`, C15.2) and inertia; **`sim::SimEnvironment`** holds gravity — the constant downward force
that makes cars fall (C35.3), settle on their suspension, and rest on the ground.

**The suspension as a joint.** SHAR models suspension as a **physics joint** (`SuspensionJointDriver` driving
a `sim::PhysicsJoint`) rather than ad-hoc ray-casts — the wheel is *constrained* to the body by a springy
joint that pushes them apart up to the travel limit. This is why cars lean in corners (weight transfers,
compressing the outer suspension), squat under acceleration, dive under braking, and bounce on landing
(C35.3): the joint transfers those forces between body and wheels. The `.con` values (C15.4) tune the joint —
stiffer `SetSpringK` = less lean, more `SetDamperC` = less bounce. The centre of mass (`SetCMOffset*`, C15.4)
sets where the body's weight sits, which the joints react against — a low CM resists tipping, a high one
rolls.

**Gravity and the environment.** Gravity lives in **`sim::SimEnvironment`** — a single global constant
pulling everything down. There's no per-object gravity or complex fields (the one exception is `PotentialField`
for special gameplay forces). This is why the whole world falls the same way: cars, characters (as physics
bodies, C25.1), debris (C35.5), and ragdolls all obey the one `SimEnvironment` gravity. It's the simplest
correct model — one gravity vector, applied to every `sim::` body each frame by the integrator (C26.5).

**Articulated bodies.** `sim::ArticulatedPhysicsObject` is for multi-part physics — a body with jointed parts
(a car with its sprung wheels is articulated; a trailer, a ragdoll character). The suspension joints make a
car an articulated system: a body plus four wheel sub-bodies connected by joints. This is the same machinery
that ragdolls a character (C25.1's `InSim` state) — jointed rigid bodies — which is why the one `sim::` engine
handles cars, characters, and props uniformly (C23.2).

**What happens if you bend it.**

- *Rely on a `sim::`/suspension member offset* — classes/vtables ✅, offsets ⏳ (the CON→member map, C24.4).
  Diff (C4.3).
- *Set extreme suspension `.con` values* — the joint can go unstable (jitter, launch). Change
  spring/damper/limit (C15.4) in small steps.
- *Raise the centre of mass* (`SetCMOffsetY`, C15.4) — the car rolls and tips easily. The CM feeds the joint
  reactions; keep it low for stability.
