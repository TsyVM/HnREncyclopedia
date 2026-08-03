# C26.6 — `sim::` Collision & the Frame

**What it is.** The runtime of the collision data decoded in C11, and the per-frame loop that ties physics
(C26.5) and collision together. This is where "the world is solid" actually happens, every frame.

**How it works (✅ verified).** The collision chunks of C11 become `sim::` collision objects:

```
sim::CollisionObject : tEntity                        — runtime of the 0x00121000 chunk (C11.1)
sim::CollisionVolume : tRefCounted, …                 — a volume (C11.2)
  ├ sim::BBoxVolume          — box (C11.5)
  ├ sim::OBBoxVolume         — oriented box
  └ sim::CylinderVolume      — cylinder
sim::CollisionManager                                 — owns the collision world
sim::CollisionDetector / sim::SubCollisionDetector    — finds contacts
sim::CollisionSolverAgent / sim::ImpulseBasedCollisionSolver   — resolves contacts
```

The volume types (`BBoxVolume`, `OBBoxVolume`, `CylinderVolume`) are exactly the primitives you decoded from
the FourCC volume data (C11.5) — the on-disk `WDT`/extent parameters (C11.3) become these runtime volumes.
`sim::CollisionObject` is the runtime of the named `0x00121000` collision object (C11.1).

**The per-frame loop.** Each frame the physics/collision systems run, in order:

1. **Integrate** — `sim::` (C26.5) advances every `SimulatedObject`'s `SimState` by the frame's forces (drive,
   gravity), producing tentative new positions.
2. **Detect** — `sim::CollisionDetector` runs broad-phase (against the BVH and object bboxes, C11.1/C11.4) then
   narrow-phase (against the volumes, C11.5) to find contacts between moving bodies and the world.
3. **Solve** — `sim::ImpulseBasedCollisionSolver` applies impulses at each contact so bodies don't
   interpenetrate — the "push apart" that makes a car bounce off a wall and a character stop at a fence
   (C13.1).
4. **Commit** — the resolved positions become the frame's final state; the `DynaPhysDSG` entities (C24/C25)
   move in the scene graph (C10), and the renderer draws them (C10.6).

So a frame is: integrate → detect → solve → draw, with `sim::` owning the first three and the scene graph the
last. This is the loop that makes the world simultaneously moving and solid.

**Why impulse-based collision.** An impulse solver resolves contacts by applying instantaneous velocity
changes — the standard technique for arcade-plausible, stable vehicle and ragdoll physics. It's forgiving
(objects rarely explode or sink), fast (a few iterations per frame), and produces the bouncy, punchy feel SHAR
wants from car crashes and pedestrian knock-downs. Pairing it with the simple collision primitives (boxes,
cylinders — C11.5) rather than full mesh collision everywhere keeps the whole loop cheap enough for 2003
hardware while feeling solid.

**Closing the runtime.** This page completes the disk→runtime bridge the book has built: collision *data*
(C11) → `sim::CollisionObject`/`CollisionVolume` (here) → contacts resolved each frame against physics bodies
(C26.5) that are the runtime of vehicles (C24) and characters (C25), drawn by the scene graph (C10) built from
meshes (C7), shaders (C6), and textures (C5). Every arrow in that chain is a verified class or a decoded
chunk; the only ⏳ left are the member offsets, recoverable by diffing (C4.3).

**What happens if you bend it.**

- *Edit visible geometry expecting collision to change* — collision is separate `sim::CollisionObject` data
  (C11); edit it too.
- *Rely on a `sim::` collision offset* — classes ✅, offsets ⏳. Diff (C4.3).
- *Give the solver degenerate volumes* (zero-size, inverted) — contacts resolve wrongly and objects jitter or
  pass through. Keep volumes well-formed (C11.5).

**This closes Part VII — the runtime class system.** Next: [Chapter 27 — Save Data & `simpsons.ini`](../C27-Save-Config/C27-Save-Config.md).
