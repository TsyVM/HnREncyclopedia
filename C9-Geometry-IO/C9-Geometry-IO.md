# Chapter 9 — Geometry Import/Export

> **Goal of this chapter:** take the decoded meshes (C7), skins (C8), and collision (C11) *out* of the game
> into standard 3-D formats you can edit, and bring edited geometry back *in* so the game still loads it.
> This is the round-trip that turns "read the format" into "make new models."

Chapters 7, 8, and 11 decoded the game's geometry — vertex streams, skins, collision volumes. This chapter is
the bridge to the outside world: exporting that geometry to **OBJ/glTF** for a 3-D tool, and re-importing
edited geometry through the size-tree discipline (C1.5). It's the practical culmination of Part II.

**Key finding (recap, ✅ verified):** SHAR geometry is **parallel count-prefixed streams** (positions
`0x00010005`, UVs `0x00010007`, colours `0x00010008`, indices `0x0001000A`, C7.3–C7.4) under a primitive
group that names a shader (C7.2). Export reads the streams into a neutral representation; import rebuilds them
and re-balances the size tree.

---

## Deep-dive pages

- [C9.1 — The Neutral Representation](01-neutral-representation.md): a toolkit-agnostic vertex/index model.
- [C9.2 — The Coordinate Boundary](02-coordinate-boundary.md): where to convert axes, and where not to.
- [C9.3 — Exporting to OBJ & glTF](03-exporting.md): writing standard formats.
- [C9.4 — Re-Importing & Rebuilding](04-reimport-rebuild.md): edited geometry back into Pure3D.
- [C9.5 — Round-Trip Validation](05-validation.md): proving the pipeline is lossless.

---

## 9.1 The neutral representation (✅ from C7)

Export starts by reading a primitive group's streams (C7.3–C7.4) into a **format-agnostic** structure —
positions, UVs, colours, indices, and the shader name — that no 3-D format is baked into:

```python
Mesh = {
  'name': str, 'shader': str,          # from the primitive group (C7.2)
  'positions': [(x,y,z), …],           # 0x00010005
  'uvs':       [(u,v), …],             # 0x00010007
  'colours':   [(r,g,b,a), …],         # 0x00010008
  'indices':   [i, …],                 # 0x0001000A (triangle strip, C7.4)
}
```

From this neutral form you can write *any* target format, and *any* source format can be read into it. It's
the same fixed-substrate idea as the toolkit (C4.6). [C9.1](01-neutral-representation.md).

## 9.2 The coordinate boundary (🟡)

SHAR uses its own axis convention; most tools are Y-up. Convert **only at the export/import boundary**, never
in the parser (C7.5) — the on-disk data and reader stay faithful; only the exchanged file is converted. The
exact SHAR axis order is 🟡, confirmed by exporting a known-oriented mesh and checking it isn't mirrored.
[C9.2](02-coordinate-boundary.md).

## 9.3 Exporting to OBJ & glTF (✅ reproducible)

**OBJ** is the simplest target — text, `v`/`vt`/`f` lines — ideal for static geometry. **glTF** carries more
(materials, skins, animation) and suits skinned characters (C8). Both are written from the neutral
representation (C9.1), converting strips to triangle lists (C7.4) and axes at the boundary (C9.2).
[C9.3](03-exporting.md).

## 9.4 Re-importing & rebuilding (✅ via C1.5)

Bringing edited geometry back means writing new streams, updating the group's vertex/index counts (C7.2) and
the mesh counts (C7.1), and running the **ancestor size fix-up** (C1.5) — because changing vertex counts
resizes the streams. Use the tree-parse → edit → re-emit-bottom-up flow (C4.1) so every `chunkSize` is
recomputed. [C9.4](04-reimport-rebuild.md).

## 9.5 Round-trip validation (✅ the acid test)

Export a mesh, re-import it unchanged, and diff against the original (C4.3). A lossless identity round-trip
proves the stream decode, the topology handling, and the size fix-up are all correct — the strongest single
validation. Only then trust *edited* geometry to load. [C9.5](05-validation.md).

---

## Key takeaways

- Export via a **neutral representation** (positions/UVs/colours/indices + shader name) so no format is baked
  in — read any source into it, write any target from it.
- Convert **axes only at the boundary** (C9.2), never in the parser — the on-disk data stays faithful.
- **OBJ** for static geometry, **glTF** for skinned characters (C8); both from the neutral form.
- Re-import rebuilds the streams and runs the **C1.5 ancestor size fix-up** (vertex-count changes resize).
- **Round-trip identity** (export→import→diff) is the acid test that the pipeline is lossless.

**Next:** [Chapter 10 — The Scenegraph](../C10-Scenegraph/C10-Scenegraph.md).
