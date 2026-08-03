# C10.6 — The Scenegraph at Runtime

**What it is.** How the on-disk graph (C10.1–C10.5) becomes the live tree the engine walks every frame to
draw and update the world. It is the runtime hub that ties together drawables (C7), collision (C11),
transforms, and ordering.

**How it works.** At load, each scene-graph node becomes a **DSG entity** (Drawable Scene Graph), and the
tree of nodes becomes a tree of entities. Each frame the engine:

1. **Walks the tree** from the root (the same recursion as your parser, C1.3).
2. **Composes transforms** (C10.3) down each branch to get world-space placements.
3. **Culls** subtrees whose bounds are off-screen (grouped by branch, C10.2).
4. **Draws** each visible drawable (C10.4) in **sort order** (C10.5), binding its shader (C6) and texture
   (C5).

Collision entities (C11) live in the *same* tree, so the one walk services both rendering and the spatial
queries physics makes — which is the whole reason collision and the scene graph share a structure (C11.6).

**The runtime classes (✅ names / ⏳ offsets).** The RTTI set names the entity family: `IEntityDSG` (the
base), `InstStatEntityDSG` (static instanced drawables — the common world prop), `CollisionEntityDSG` /
`AnimCollisionEntityDSG` (collision, C11), `DynaPhysDSG` (dynamic physical objects, C26), and the
`tDrawable` hierarchy they draw. Names and inheritance are **verified**; member offsets are **⏳**. So the
book can say exactly *which* class a node becomes and how the classes relate, and marks the byte offsets as
the open frontier.

**Why one graph for everything.** Draw, collide, cull, and animate all need the same information: where each
object is, and how objects group. One hierarchy that answers all four is cheaper than four parallel
structures and guarantees they never disagree — a door's mesh, its collision, and its animation are sibling
entities that move as one because they share a parent transform. This unification is the architectural
centre of the runtime, and it is why Chapters 7 (meshes), 10 (this), and 11 (collision) are three views of a
single world tree.

**The modding consequence.** To place something in the world you add a node; to move it you edit a transform
(C10.3); to change what it looks like you edit the referenced mesh/shader/texture (C5–C7); to change what's
solid you edit the referenced collision (C11). Each concern is a different chunk in the same tree, which is
why understanding the graph is what lets you predict where an edit has to go.

**What happens if you bend it.**

- *Add a drawable node but no transform* — it may render at the origin or inherit the wrong placement. Give
  new nodes a transform (C10.3).
- *Rely on a DSG member offset* — it's ⏳; get it from a diff (C4.3) first. Names are safe to use; offsets
  are not until verified.
- *Edit the graph without the size fix-up* — it's a chunk tree; the C1.5 discipline applies on re-emit.

**Next:** [Chapter 12 — Level Composition](../C12-Level-Composition/C12-Level-Composition.md).
