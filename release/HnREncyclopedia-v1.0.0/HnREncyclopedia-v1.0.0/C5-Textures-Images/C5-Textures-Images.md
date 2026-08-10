# Chapter 5 — Textures & Images

> **Goal of this chapter:** decode the Texture → Image → Image-Data hierarchy, read a texture's
> dimensions and format straight from its bytes, and extract or replace the pixels — all verified
> against the shipped files.

Textures are where Part II applies the container model (C1) to real art. In Pure3D a texture is a small
three-level nest: a **Texture** chunk (`0x00019000`) describing the image, an **Image** chunk
(`0x00019001`) that is the encoded picture, and an **Image-Data** leaf (`0x00019002`) that is the raw
bytes. This chapter decodes all three from actual files — every field below was read out of the retail
data with `tools/p3d_rcf_scan.py`, not taken from convention.

A key, useful fact established immediately: **texture names are stored in the clear**. Unlike the hashed
asset references of Chapter 2, a Texture chunk begins with a length-prefixed string — `flag.bmp`,
`flarebase2.bmp` — so textures are searchable and self-identifying inside the binary.

---

## Deep-dive pages

- [C5.1 — The Texture Chunk (`0x00019000`)](01-texture-chunk.md): the verified nine-field header — name, version, width, height, bpp, alpha, mips, type, usage.
- [C5.2 — Image & Image-Data (`0x00019001`/`0x00019002`)](02-image-and-data.md): the encoded picture and the raw payload.
- [C5.3 — Formats: BMP, PNG & Palettes](03-formats.md): what the payload actually contains and the 930 loose `.png` sources.
- [C5.4 — Extracting Textures](04-extracting.md): pulling Image-Data out to standalone image files.
- [C5.5 — Replacing Textures](05-replacing.md): length-preserving vs. resizing edits and the C1.5 fix-up.
- [C5.6 — Textures at Runtime](06-runtime.md): how a shader (C6) binds a texture by name.

---

## 5.1 The Texture chunk, decoded (✅ verified)

The `0x00019000` chunk's own data is a length-prefixed name followed by a fixed nine-`uint32` header. Read
from `flag.bmp` in `art/b00 - Copy.p3d`:

```
08 "flag.bmp"                 pstr: 1-byte length (8) + name
36 B0 00 00   version   = 0x000036B0 (14000)
40 00 00 00   width     = 64
40 00 00 00   height    = 64
04 00 00 00   bpp        = 4
00 00 00 00   alphaDepth = 0
01 00 00 00   numMips    = 1
01 00 00 00   textureType = 1
00 00 00 00   usage      = 0
00 00 00 00   (priority/pad) = 0
```

Width `64`, height `64`, one mip — a 64×64 texture named `flag.bmp`. The `version` `14000` is the Pure3D
format-version stamp that recurs across chunk types. [C5.1](01-texture-chunk.md) walks every field and
what it controls.

## 5.2 Image and Image-Data (✅ verified)

Inside the Texture sits an **Image** (`0x00019001`) whose own data repeats the name and dimensions, and
inside *that* is the **Image-Data** leaf (`0x00019002`) — the encoded picture bytes (in
`art/cars/common.p3d`, a 1,546-byte payload). The Texture describes; the Image encodes; the Image-Data
*is* the pixels. [C5.2](02-image-and-data.md).

## 5.3 What the payload is

The name extensions are honest: `flag.bmp`, `flarebase2.bmp` are BMP-derived, and the game ships **930
loose `.png` files** in `art/` as the pipeline's source images (28.5 MB). The Image-Data payload is the
encoded image in the format the header's `bpp`/`type` select — true-colour or paletted.
[C5.3](03-formats.md) covers identifying and decoding it.

## 5.4 & 5.5 Extract and replace

Extraction is a tree-walk to the `0x00019002` leaf and a slice (C4). Replacement is either
**length-preserving** (swap same-size pixels — no size-tree work) or **resizing** (grow/shrink the leaf
and run the C1.5 ancestor fix-up up through Image, Texture, and the file header). [C5.4](04-extracting.md),
[C5.5](05-replacing.md).

## 5.6 Runtime binding

A texture does nothing until a **shader** references it. A shader's texture parameter (`0x00011002`,
Chapter 6) names the texture — e.g. `flarebase2.bmp` — and the loader binds them by that name. The
Texture→Shader→Mesh chain is what puts a picture on a triangle. [C5.6](06-runtime.md).

---

## Key takeaways

- A texture is a three-level nest: **Texture `0x00019000` → Image `0x00019001` → Image-Data `0x00019002`**.
- The Texture header is a **plaintext name + nine `uint32`** (version, width, height, bpp, alpha, mips,
  type, usage, priority) — all ✅ verified from bytes.
- **Texture names are stored in the clear** — textures are searchable inside the binary (contrast the
  hashed references of C2).
- Extract by slicing the Image-Data leaf; replace length-preserving for free, or resize with the C1.5
  ancestor fix-up.
- A texture reaches the screen only when a shader (C6) binds it by name.

**Next:** [Chapter 6 — Shaders & Materials](../C6-Shaders-Materials/C6-Shaders-Materials.md).
