# C11.3 — Collision Vectors & the FourCC Model (`0x00121100`)

**What it is.** The leaf that actually describes a volume's geometry, and the reason collision is legible:
it uses a **FourCC tag + typed value** model, exactly like the shader parameters of C6. A volume is a set
of tagged scalars and vectors.

**How it works (✅ verified).** A `0x00121100` Collision Vector's own data, decoded from
`art/b00 - Copy.p3d`:

```
00 00 00 00        (flags/index)
57 44 54 00        "WDT\0"  — the tag: WiDTh
01 00 00 00        (count/type)
… value bytes …    the width value
```

The tag `WDT` (width) is a four-character key; the bytes after it are that parameter's value. By direct
analogy with the shader model (C6) and the volume types (C11.5), the tag vocabulary describes the primitive
— width, and (🟡) radius, half-extents, centre, and axis vectors. So reading a volume is: collect its
`0x00121100` children, decode each tag, and you have the box/cylinder/sphere it defines.

**Why FourCC again.** SHAR reuses the self-describing tag model across unrelated subsystems — shaders (C6),
collision here — because it is *robust to change*: a tool can add or skip a parameter it doesn't recognise
without breaking the format, and a reader never needs a fixed struct layout, only a tag→meaning table. For
collision, where different volume types need different parameters (a sphere needs a radius, a box needs
extents), tagged parameters avoid a separate struct per type — every volume is the same "bag of tagged
vectors," and the tags present tell you which type it is.

**Reading a volume, concretely.** Gather the `0x00121100` tags under a `0x00121001` volume; a volume with a
radius tag is a sphere/cylinder, one with three half-extent tags is a box. The `WDT` verified here is one
such dimension. Build a `tag → (type, meaning)` table as you decode more files (the C4.4 workflow), and the
whole collision system becomes readable key/value geometry.

**What happens if you bend it.**

- *Assume a fixed field order instead of reading tags* — the model is tag-addressed; a volume may carry its
  parameters in any order. Read by tag, not by position.
- *Change `WDT` (or a radius) without matching the visible object* — the solid shape no longer matches what
  the player sees, causing invisible walls or clipping. Keep collision dimensions consistent with the mesh.
- *Invent a tag the engine doesn't know* — it will be ignored (like an unknown shader param), so a typo'd
  tag silently drops that dimension. Use verified tags.
