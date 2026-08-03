# C7.6 — Meshes at Runtime

**What it is.** How a decoded mesh becomes something the engine draws each frame — the link from the
geometry chunks of this chapter to the scene graph (C10) and the runtime drawable classes (C23).

**How it works.** At load, the Pure3D loader (C1.8) turns a `0x00010000` Mesh into a **drawable** object
and each `0x00010002` primitive group into a draw batch bound to the shader it names (C7.2 → C6 → C5). The
drawable is placed in the scene graph (`0x03F0xxxx`, C10), which owns its transform and decides when it is
visited. Each frame the renderer walks the graph, and for every visible drawable issues its batches: set
the shader's state and texture, bind the vertex/index streams, draw the strip.

**The runtime classes (✅ names / ⏳ offsets).** The objects a mesh becomes belong to the DSG ("Drawable
Scene Graph") family, all present in the RTTI set (`shar_dumps.csv`): `tDrawable`, `IEntityDSG`, and the
concrete entities `InstStatEntityDSG` (static instanced geometry), `CollisionEntityDSG`,
`AnimCollisionEntityDSG`, `DynaPhysDSG` (dynamic physical objects). Their **names and inheritance are
verified**; their **member offsets are ⏳** and recovered by diffing (C4.3). So we can say with confidence
*which class* a mesh becomes, and how those classes relate, without yet claiming the exact byte where its
vertex pointer lives.

**Why this chain matters.** The whole point of Part II is this hand-off: on disk a mesh is passive bytes
(C7.1–C7.4); at runtime it is a drawable in a graph, drawn with a material that samples a texture. Every
link is a **name** — mesh names its shader, shader names its texture — so the runtime graph mirrors the
readable on-disk graph. That correspondence is what lets you predict a mod's runtime effect from the file:
retexture the Image-Data (C5.5) and the same drawable, same batch, same draw call now shows your pixels.

**Static vs. dynamic.** A world prop that never moves becomes an `InstStatEntityDSG` (cheap, instanced); a
mesh that collides becomes a `CollisionEntityDSG` (C11); one driven by physics becomes a `DynaPhysDSG`
(C26). Which class a mesh becomes is decided by how the level/scene references it (C10/C12), not by the
mesh chunk itself — the same geometry can be static scenery in one place and a dynamic object in another.

**What happens if you bend it.**

- *Assume a fixed runtime class for a mesh* — the same mesh can become different DSG classes by context
  (C10/C12). Read the scene reference, not just the mesh.
- *Edit geometry expecting a collision change* — the drawable and the collision volume (C11) are separate;
  changing the mesh does not change collision. Edit both if you need both.
- *Rely on a member offset for a drawable* — those are ⏳; get one from a diff before you build on it
  (C4.5), and mark it user-supplied.

**Next:** [Chapter 8 — Skeletons, Skinning & Locators](../C8-Skeletons-Locators/C8-Skeletons-Locators.md).
