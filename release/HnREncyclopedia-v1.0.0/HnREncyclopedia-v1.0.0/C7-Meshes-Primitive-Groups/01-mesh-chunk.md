# C7.1 — The Mesh Chunk (`0x00010000`)

**What it is.** The top of the geometry hierarchy: a named container that holds one or more primitive
groups (C7.2) and some mesh-level data. It is the object a level or model references when it wants to draw
a shape.

**How it works (✅ verified).** The `0x00010000` own data starts with a plaintext **name** (verified:
`t2_bonus164Shape_001` in `art/b00 - Copy.p3d`) and a short numeric header, then the chunk contains:

- **`0x00010002` Primitive Group(s)** — the drawable geometry, each bound to a shader (C7.2).
- **`0x00010017`** — a mesh header/counts leaf (values like `numPrims`, totals — 🟡).
- **`0x00010003` / `0x00010004`** — float blocks whose values sit in the mesh's coordinate range
  (e.g. `-24, 9.5, 61.8`), consistent with **bounding-box / extent** data (🟡 — decoded as floats, meaning
  inferred).

The Maya-style name (`…Shape_001`) is a tell: SHAR's art was authored in Maya and exported, so mesh names
carry their DCC-tool provenance — useful when matching a mesh back to source art.

**Why it's built this way.** A mesh groups geometry that shares a transform and a purpose but may use
several materials — hence multiple primitive groups, one per shader. Keeping bounds and counts at the mesh
level lets the renderer cull or budget the whole mesh cheaply (test the bbox) before descending into its
groups. The plaintext name makes the mesh addressable by the scene graph (C10) and by scripts.

**What happens if you bend it.**

- *Assume one primitive group per mesh* — a multi-material mesh has several; walk them all (C7.2).
- *Edit vertex data but not the mesh-level counts (`0x00010017`)* — the renderer may read the wrong totals.
  Keep mesh-level counts consistent with the sum of the groups.
- *Treat `0x00010003`/`0x00010004` as vertices* — they read as floats but sit at the mesh level, not in a
  group's stream; they are bounds/extents (🟡). Decode group streams from `0x00010005`+ inside the
  primitive group, not from these.
