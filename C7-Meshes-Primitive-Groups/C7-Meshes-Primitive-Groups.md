# Chapter 7 — Meshes & Geometry

> **Goal of this chapter:** decode the Mesh (`0x00010000`) and its primitive groups into vertex positions,
> UVs, colours, and indices — the actual triangles of the game — all verified from real bytes.

This chapter turns the container model (C1) into geometry you can read, export, and rebuild. **A
correction, verified from bytes:** the Mesh family is `0x0001**0**xxx` (not `0x00011xxx`, which is the
Shader family of C6). The whole geometry hierarchy below was decoded from `art/b00 - Copy.p3d` with
`tools/p3d_rcf_scan.py` — positions, colours, and indices all read out as sane values.

---

## Deep-dive pages

- [C7.1 — The Mesh Chunk (`0x00010000`)](01-mesh-chunk.md): the named mesh container and its header/counts.
- [C7.2 — The Primitive Group (`0x00010002`)](02-primitive-group.md): how a group binds a shader and declares vertex/index counts.
- [C7.3 — Vertex Streams: Positions, UVs, Colours](03-vertex-streams.md): `0x00010005`/`0x00010007`/`0x00010008`.
- [C7.4 — The Index Buffer (`0x0001000A`)](04-index-buffer.md): turning vertices into triangles.
- [C7.5 — Exporting & Rebuilding](05-export-rebuild.md): to OBJ and back, with the size-tree fix-up.
- [C7.6 — Meshes at Runtime](06-runtime.md): the mesh→shader→texture chain and the DSG drawable classes.

---

## 7.1 The Mesh (✅ verified)

A `0x00010000` Mesh carries a plaintext **name** (verified: `t2_bonus164Shape_001`) and a small header,
and it contains one or more **primitive groups** plus mesh-level data (`0x00010017` counts;
`0x00010003`/`0x00010004` float blocks that read as bounding-box/extent data — 🟡). Like textures and
shaders, meshes are **named in the clear**, so a mesh is identifiable straight from its bytes.
[C7.1](01-mesh-chunk.md).

## 7.2 The Primitive Group (✅ verified)

The `0x00010002` Primitive Group is where geometry meets material. Its own data, verified:

```
00 00 00 00                     (index / flags)
0C "steps_conc_m"               pstr: the SHADER this group draws with (C6)
01 00 00 00                     (1)
21 20 00 00                     primitive/vertex-format flags (0x2021)
0C 00 00 00                     vertexCount = 12
0E 00 00 00                     indexCount  = 14
00 00 00 00
```

So a primitive group names its **shader** (`steps_conc_m`), declares **12 vertices** and **14 indices**,
and carries a format word. Its children are the actual streams. This is the node that binds the
mesh→shader→texture chain (C5.6). [C7.2](02-primitive-group.md).

## 7.3 Vertex streams (✅ verified)

The group's children are typed, count-prefixed streams:

| Chunk | Stream | Verified layout |
|---|---|---|
| `0x00010005` | **Positions** | `u32 count=12`, then 12 × `(f32 x, y, z)` — values like `(-24.03, 9.66, 64.64)` |
| `0x00010007` | **UVs** | `u32 count`, then per-vertex UV floats (🟡) |
| `0x00010008` | **Colours** | `u32 count=12`, then 12 × RGBA byte quad (`FF`-alpha) |
| `0x00010011` | flag/tag | 1 byte |

Positions read as real world coordinates and colours as opaque RGBA — the C4.4 cross-check passes.
[C7.3](03-vertex-streams.md).

## 7.4 The Index Buffer (✅ verified)

`0x0001000A` is the index buffer: `u32 count=14`, then 14 `u32` indices (verified values `0, 6, 1, 7,
3, …` — a triangle strip). The indices reference the position/colour/UV arrays by position.
[C7.4](04-index-buffer.md).

## 7.5 & 7.6 Export and runtime

With positions, UVs, colours, and indices decoded, exporting to OBJ/glTF is mechanical (C7.5), and
rebuilding requires the C1.5 ancestor fix-up because vertex-count changes resize the streams. At runtime
the mesh becomes a drawable in the DSG family (C10/C23; names ✅ from RTTI, offsets ⏳), drawn with the
shader its primitive group names (C7.6).

---

## Key takeaways

- The geometry family is **`0x0001**0**xxx`**: Mesh `0x00010000` → Primitive Group `0x00010002` → streams.
- A **primitive group binds a shader by name** and declares vertex/index counts (✅ verified:
  `steps_conc_m`, 12 verts, 14 indices).
- Streams are **count-prefixed**: positions `0x00010005` (XYZ f32), colours `0x00010008` (RGBA), indices
  `0x0001000A` (u32); UVs `0x00010007` (🟡).
- Names in the clear make the **mesh → shader → texture** chain (C5.6) readable straight from bytes.

**Next:** [Chapter 8 — Skeletons, Skinning & Locators](../C8-Skeletons-Locators/C8-Skeletons-Locators.md).
