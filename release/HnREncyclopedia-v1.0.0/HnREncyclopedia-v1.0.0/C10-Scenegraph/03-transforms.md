# C10.3 — Transforms (`0x03F00003`)

**What it is.** The node that positions, rotates, and scales its subtree: a transform carries a matrix (and
some structure) and applies it to everything beneath it. It is how one mesh becomes many placed instances.

**How it works (✅ verified).** A `0x03F00003` transform's own data begins with a structured header of
counts/indices and carries a transform matrix. Verified header start from `art/b00 - Copy.p3d`:
`0F 00 00 00 02 00 00 00 01 00 00 00 03 …` — a run of small integers (child count, indices) followed by the
matrix floats. Pure3D matrices are read **straight, with no transpose** (the same rule as the whole engine):
a sequential 16-float read is already the correct matrix, and the world is arranged in the engine's own axis
convention.

**Why transforms live in the graph.** Putting the transform on a node — rather than baking it into the mesh
— is what makes instancing possible: the mesh's vertices (C7.3) stay in a canonical local space, and each
transform node places a copy of it. Fifty crates are fifty transform nodes over one mesh. It is also what
makes hierarchy meaningful (C10.2): a child's world position is its own transform composed with all its
ancestors', so moving a parent moves the whole subtree. This composition is the core operation the runtime
performs each frame as it walks the graph (C10.6).

**Reading a placement.** To find where an instance actually is, compose the transforms from the root down to
its drawable node. The matrix at each node is local; the product is world-space. For a static prop you can
often read just its own node's matrix; for an articulated object you must compose the chain.

**The coordinate boundary.** As with meshes (C7.5), if you export placements to another tool, convert axes at
the boundary, not in the parser. The on-disk matrix is faithful to the engine; only the exchanged data is
converted.

**What happens if you bend it.**

- *Transpose the matrix on read* — every placement is wrong (rotated/mirrored). Read the 16 floats straight.
- *Edit a child's transform expecting world-space* — it's local, composed with ancestors. To move an
  instance in the world, account for the parent chain.
- *Change a shared parent's transform* — every descendant moves. If you meant to move one instance, edit its
  own node, not an ancestor.
