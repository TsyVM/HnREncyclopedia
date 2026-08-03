# Chapter 6 — Shaders & Materials

> **Goal of this chapter:** decode the Shader (`0x00011000`) and its FourCC-tagged parameter system — the
> material layer that binds textures (C5) to geometry (C7) and sets render state.

**A correction this edition makes.** Public Pure3D convention often labels `0x00010000` "Shader"; the
byte-level decode of the retail SHAR data shows otherwise, and this chapter uses the **verified** mapping:
**`0x00011000` is the Shader**, and `0x00010000` is the **Mesh** (Chapter 7). The distinction is proven
below from real bytes and is exactly why the [master table](../Glossary/chunk-ids.md) carries confidence
markers.

---

## The Shader, decoded (✅ verified)

A `0x00011000` Shader chunk's own data is a **plaintext name** and a **method name**, and its children are
typed parameters. Verified from `art/cars/common.p3d`:

```
0x00011000 Shader   name="flarebase2_m"   method="simple"
  0x00011002  Shader texture param   "TEX" + pstr "flarebase2.bmp"   → names the Texture (C5)
  0x00011003  Shader int param       FourCC + int32    (appears ~16× per shader)
  0x00011004  Shader float param     FourCC + float32
  0x00011005  Shader colour param    FourCC + RGBA byte quad
```

(Note — verified: Pure3D length-prefixed strings are **null-padded to alignment**, so the method stores
`"simple\0\0"` with a length byte of 8; strip the trailing nulls. The same applies to any `pstr` name.)

Each parameter is a **four-character tag** plus one typed value — a compact, self-describing key/value
material model. Verified tags read straight from the file:

| Tag | Chunk | Value (example) | Meaning (🟡) |
|---|---|---|---|
| `TEX ` | `0x00011002` | `flarebase2.bmp` | texture to sample (C5) |
| `LIT ` | `0x00011003` | 0 | lit/unlit flag |
| `2SID` | `0x00011003` | 0 | two-sided |
| `BLMD` | `0x00011003` | 2 | blend mode |
| `ACMP` | `0x00011003` | 4 | alpha-compare function |
| `SHIN` | `0x00011004` | 10.0 | shininess |
| `ACTH` | `0x00011004` | 0.5 | alpha threshold |
| `DIFF` | `0x00011005` | `FF FF FF FF` | diffuse colour |
| `SPEC` | `0x00011005` | `FF 00 00 00` | specular colour |
| `AMBI` | `0x00011005` | `FF FF FF FF` | ambient colour |
| `EMIS` | `0x00011005` | `FF 00 00 00` | emissive colour |

The **tags and value types are ✅ verified** (read from bytes); the **human meanings are 🟡** (inferred
from the tag mnemonics and values, e.g. `SHIN`=10.0 as shininess). This FourCC model is why `0x00011003`
is the single most common chunk in the game (224,971 — every shader carries many int params).

---

## Deep-dive pages

- [C6.1 — The Shader Chunk & Method Name](01-shader-chunk.md): `0x00011000` own data; the `"simple"` and other shader methods.
- [C6.2 — Integer Parameters (`0x00011003`)](02-int-params.md): the full FourCC vocabulary (`SHMD`,`FIMD`,`BLMD`,`ACMP`,`UVMD`,`2SID`,`MMIN`,`MMAX`…).
- [C6.3 — Float Parameters (`0x00011004`)](03-float-params.md): `SHIN`, `ACTH`, `MSHP`.
- [C6.4 — Colour Parameters (`0x00011005`)](04-colour-params.md): `DIFF`/`SPEC`/`AMBI`/`EMIS` and the RGBA byte order.
- [C6.5 — Texture Binding (`0x00011002`)](05-texture-binding.md): the `TEX`/`REFL`/`ENVB` slots and name resolution to a Texture (C5).
- [C6.6 — Editing Materials](06-editing-materials.md): recolour, retexture, retune — all length-preserving (C1.5).

---

## Key takeaways

- **`0x00011000` is the Shader** (name + method + params); `0x00010000` is the Mesh (C7). This corrects the
  common public label and is verified from bytes.
- Parameters are **FourCC tag + typed value**: texture (`0x00011002`), int (`0x00011003`), float
  (`0x00011004`), colour (`0x00011005`).
- Tag names and value *types* are ✅ verified; their *meanings* are 🟡 from the mnemonics.
- The `TEX` param binds the texture by **name** (C5.6); meshes bind the shader by name (C7).

**Next:** [Chapter 7 — Meshes & Geometry](../C7-Meshes-Primitive-Groups/C7-Meshes-Primitive-Groups.md).
