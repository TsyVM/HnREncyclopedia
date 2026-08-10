# C11.6 — Collision at Runtime (`0x00121200` Intersect DSG)

**What it is.** How the on-disk collision (C11.1–C11.5) becomes the live system that stops the player
walking through walls. The bridge is the `0x00121200` **Intersect DSG** chunk and the RTTI collision entity
classes it builds.

**How it works.** At load, a collision object (C11.1) becomes a **collision entity** in the Drawable Scene
Graph (DSG) family, placed in the world alongside its visible drawable (C7.6). The `0x00121200`
**Intersect DSG** chunk (1,741 instances, verified) is the scene-graph node that carries collision into the
world — it is to collision what the scenegraph drawable (C10) is to visible geometry. Each frame, the
physics system (C26) queries these entities: broad-phase against the BVH (C11.4) and object bboxes (C11.1),
then narrow-phase against the volumes (C11.2–C11.5) for the survivors.

**The runtime classes (✅ names / ⏳ offsets).** The RTTI set (`shar_dumps.csv`) confirms the collision
entity family by name and inheritance:

- **`CollisionEntityDSG`** — a static collidable in the scene graph.
- **`AnimCollisionEntityDSG`** — collision that animates (moving platforms, doors).
- **`IntersectDSG`** — the intersect/query entity (the `0x00121200` chunk's runtime form).
- **`DynaPhysDSG`** — a dynamically-simulated physical object (C26), which both collides and moves.

These names and their base classes are **verified**; their member offsets are **⏳** and recovered by
diffing (C4.3). So we can state with confidence *which* classes collision becomes and how they relate,
without yet claiming the byte where a volume pointer sits.

**Why the DSG design.** Putting collision entities in the *same* scene graph as drawables means the engine
walks one hierarchy to both draw and collide the world, sharing transforms and culling. A door's visible
mesh and its animated collision move together because they are sibling entities under one node. This is why
Chapter 10 (the scene graph) and this chapter are two halves of one story: the graph arranges *everything*
in the world, visible and solid alike.

**The modding consequence.** Because collision is separate data (C11.1) referenced by name, you can change
what's solid without touching what's seen — widen a doorway's collision while leaving its mesh, or make a
decorative object non-solid by removing its collision object. And because the runtime classes are
RTTI-verified, a native mod (DonutsSDK) can *identify* a live collision entity by its vtable even though the
exact field offsets are still ⏳.

**What happens if you bend it.**

- *Change the mesh expecting collision to follow* — they're separate entities; edit the collision object
  too (C11.1). This is the most common collision-modding mistake.
- *Rely on a `CollisionEntityDSG` member offset* — it's ⏳; get it from a diff (C4.3) and mark it
  user-supplied before building on it.
- *Add collision without a scene-graph node to carry it* — an orphan collision object may never be tested;
  it needs its `0x00121200`/DSG placement to enter the world.

**Next:** [Chapter 12 — Level Composition](../C12-Level-Composition/C12-Level-Composition.md).
