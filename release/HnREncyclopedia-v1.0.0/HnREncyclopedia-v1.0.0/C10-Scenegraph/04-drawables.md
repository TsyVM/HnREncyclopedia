# C10.4 — Drawables (`0x03F00005` / `0x03F00006`)

**What it is.** The leaf that connects the scene graph to actual geometry: a drawable node references the
mesh/skin (C7) it renders. It is the point where "where and how" (the graph) meets "what" (the asset).

**How it works (✅ verified).** A `0x03F00005` Drawable's own data begins with a reference handle. Verified
from `art/b00 - Copy.p3d`: the own data starts `2A 01 00 00` — index `0x12A`, the handle of the drawable
this node draws. The node does **not** contain the geometry; it names/indexes it, and the loader resolves
the reference to the loaded mesh object (the same name/handle resolution as C5.6). `0x03F00006` carries the
drawable's associated data (bounds/params — 🟡).

**Why reference, not embed.** Referencing is the whole point of a scene graph: it separates *instances* from
*assets*. One mesh (heavy — vertices, indices, C7) is loaded once; each place it appears is a lightweight
drawable node pointing at it. This is memory that a 2003 console did not have to spare: fifty on-screen
crates cost one mesh plus fifty small nodes, not fifty meshes. It also means retexturing or editing the mesh
(C5.5, C7.5) updates every instance at once, because they all reference the same asset.

**Following the chain.** A drawable node → a mesh (C7) → its primitive groups → their shaders (C6) → their
textures (C5). The whole visible pipeline is a chain of references, each resolved by index or name, and each
readable from the bytes. Starting at a scene-graph drawable and following the references is how you answer
"what does this node actually look like?" without running the game.

**What happens if you bend it.**

- *Point a drawable at a handle that isn't loaded* — the node draws nothing (or crashes on an invalid
  handle). Ensure the referenced mesh is loaded (C14.2) before the node needs it.
- *Duplicate a drawable node to duplicate an object* — correct and cheap (that's instancing); just give each
  its own transform (C10.3) so they don't overlap.
- *Embed geometry in the node* expecting the engine to draw it — the node references, it doesn't contain.
  Put geometry in a mesh (C7) and reference it.
