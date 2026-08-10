# C7.5 — Exporting & Rebuilding

**What it is.** Getting geometry out of a `.p3d` into a standard format (OBJ/glTF) you can edit in a 3-D
tool, and getting edited geometry back in so the game loads it. Export is a read; rebuild is a size-tree
problem (C1.5).

**Exporting (✅ from the verified streams).** Walk to each primitive group (C7.2), read its parallel
streams (C7.3) and index buffer (C7.4), and emit:

```python
def export_obj(group):
    verts   = read_positions(group)     # 0x00010005  -> [(x,y,z), ...]
    uvs     = read_uvs(group)           # 0x00010007
    indices = read_indices(group)       # 0x0001000A
    out = []
    for x, y, z in verts:               # convert axes at THIS boundary (below)
        out.append(f"v {x} {y} {z}")
    for u, v in uvs:
        out.append(f"vt {u} {v}")
    for a, b, c in triangles_from_strip(indices):   # C7.4
        out.append(f"f {a+1}/{a+1} {b+1}/{b+1} {c+1}/{c+1}")   # OBJ is 1-based
    return "\n".join(out)
```

**The coordinate boundary.** SHAR uses its own axis convention; most DCC tools are Y-up. Do the axis swap
*here*, at the export/import boundary, never inside the parser (the coordinate-boundary rule, C9.2).
Keeping the conversion in the bridge means the on-disk data and your reader
stay faithful to the file, and only the exchanged file is converted. The exact SHAR axis order is 🟡 —
confirm by exporting a known-oriented mesh and checking it isn't mirrored or rotated.

**Rebuilding.** Re-importing edited geometry means writing new streams and indices, updating the primitive
group's `vertexCount`/`indexCount` (C7.2) and the mesh-level counts (C7.1), and running the **ancestor size
fix-up** (C1.5) because the stream lengths changed. Use the tree-parse → edit → re-emit-bottom-up flow
(C4.1) so every `chunkSize` is recomputed and none is left stale.

**Why round-tripping is the acid test.** Export a mesh, re-import it unchanged, and diff against the
original (C4.3). A lossless round-trip proves your stream decode, your index topology, and your size fix-up
are all correct — the strongest single validation of this chapter. Only once the identity round-trip is
clean should you trust *edited* geometry to load.

**What happens if you bend it.**

- *Convert axes inside the parser* — every downstream tool now disagrees with the file. Convert only at the
  bridge.
- *Change vertex count but not the group/mesh counts* — the loader reads the wrong element count (C7.2).
  Update every count and the size tree.
- *Skip the round-trip test* — you ship geometry that "looks right" in your tool but desyncs in-game. Prove
  the identity round-trip first.
