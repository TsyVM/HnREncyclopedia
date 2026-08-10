# Chapter 10 — The Scenegraph

> **Goal of this chapter:** decode the `0x03F0xxxx` scene-graph family — the hierarchy that arranges every
> drawable and collision entity in the world, applies transforms, and orders drawing. After this chapter
> you can read how a level is assembled from nodes, transforms, and references to geometry.

The scene graph is the spine of the rendered world. Where Chapters 5–9 decode *assets* (textures, shaders,
meshes, skeletons), the scene graph decides *where they go* and *in what order they draw*. It is the
`0x03F0xxxx` family, and it is numerous — `0x03F00007` (sort order) alone occurs 10,311 times, `0x03F00003`
(transform) 8,755 times. Everything below was decoded from `art/b00 - Copy.p3d`.

**Key finding (✅ verified):** scene-graph nodes are **named** (`t2_bonus164Shape_001`), carry **transforms**
as structured data, and reference drawables by index/name — so a level's spatial structure is readable
straight from the bytes, and matches the collision hierarchy (C11) it parallels.

---

## Deep-dive pages

- [C10.1 — The Scenegraph & its Root (`0x03F00000`/`0x03F00001`)](01-scenegraph-root.md): the named top of the world hierarchy.
- [C10.2 — Branches & Nodes (`0x03F00002`)](02-branches-nodes.md): how the tree fans out.
- [C10.3 — Transforms (`0x03F00003`)](03-transforms.md): per-node matrices and the coordinate system.
- [C10.4 — Drawables (`0x03F00005`/`0x03F00006`)](04-drawables.md): how a node references the geometry it draws.
- [C10.5 — Sort Order (`0x03F00007`)](05-sort-order.md): the game's most common scenegraph chunk and why draw order matters.
- [C10.6 — The Scenegraph at Runtime](06-runtime.md): the DSG entities and the per-frame walk.

---

## 10.1 The Scenegraph and its root (✅ verified)

A `0x03F00000` **Scenegraph** is named after the object it arranges (verified: `t2_bonus164Shape_001`), and
a `0x03F00001` **Root/Branch** (verified name `t2_bonus116Shape`) begins the node hierarchy beneath it. The
Maya-style names (`…Shape_001`) again reveal the art pipeline (C7.1). The graph is a normal Pure3D chunk
tree, so you walk it with the same recursive walker (C1.3). [C10.1](01-scenegraph-root.md).

## 10.2 & 10.3 Nodes and transforms (✅ verified)

Beneath the root, branches (`0x03F00002`) fan the tree out, and **transforms** (`0x03F00003`) place each
node. A verified `0x03F00003` carries a structured header (counts/indices `0x0F, 2, 1, 3, 3, 1, 4…`) and a
matrix — read straight, no transpose, as with all Pure3D matrices. The transform is what turns a shared
mesh into many placed instances: one `common.p3d` car mesh, many transformed nodes. [C10.2](02-branches-nodes.md),
[C10.3](03-transforms.md).

## 10.4 Drawables (✅ verified)

A `0x03F00005` **Drawable** node references the geometry to draw. Verified own data begins with an index
(`0x12A`), the handle of the drawable (mesh/skin, C7) this node renders. So the graph does not embed
geometry — it **references** it by index/name, letting many nodes share one mesh. [C10.4](04-drawables.md).

## 10.5 Sort order (✅ verified)

`0x03F00007` — the **most common** scene-graph chunk (10,311) — encodes **draw order**. Transparent
surfaces, decals, and layered geometry must draw in a specific sequence to look right; the sort-order chunk
is how the graph records it. That it is the most numerous scene-graph chunk shows how much of the world
depends on correct ordering. [C10.5](05-sort-order.md).

## 10.6 Runtime

At load the graph becomes a tree of DSG entities (`IEntityDSG`, `InstStatEntityDSG`, `CollisionEntityDSG`,
`DynaPhysDSG` — names ✅ from RTTI, offsets ⏳). Each frame the renderer walks it, applies transforms,
culls, and draws in sort order — the same walk your parser does, one step further. [C10.6](06-runtime.md).

---

## Key takeaways

- The scene graph (`0x03F0xxxx`) arranges the world: named nodes, transforms, and references to geometry.
- Nodes are **named** (`t2_bonus164Shape_001`); transforms (`0x03F00003`) place them; drawables
  (`0x03F00005`) **reference** meshes by index — sharing one mesh across many placements.
- **Sort order** (`0x03F00007`) is the most common node — draw order is pervasive.
- It parallels the collision hierarchy (C11): one world tree carries both visible and solid entities.
- Runtime is the DSG entity family (names ✅, offsets ⏳; C11.6/C23).

**Next:** [Chapter 11 — Collision & Intersect](../C11-Collision-Intersect/C11-Collision-Intersect.md) (already written), or [Chapter 12 — Level Composition](../C12-Level-Composition/C12-Level-Composition.md).
