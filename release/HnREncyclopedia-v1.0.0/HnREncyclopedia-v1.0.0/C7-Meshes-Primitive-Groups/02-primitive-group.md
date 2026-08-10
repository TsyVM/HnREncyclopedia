# C7.2 — The Primitive Group (`0x00010002`)

**What it is.** The node where geometry meets material: one batch of triangles that all use the same
shader. It names the shader, declares how many vertices and indices it has, and contains the streams that
hold them.

**How it works (✅ verified).** The `0x00010002` own data, decoded from `art/b00 - Copy.p3d`:

```
00 00 00 00                (index / flags)
0C  "steps_conc_m"          pstr: the shader name (C6) this group draws with
01 00 00 00                (1)
21 20 00 00                format word 0x2021  (vertex-format / primitive flags)
0C 00 00 00                vertexCount = 12
0E 00 00 00                indexCount  = 14
00 00 00 00
```

Two facts drop straight out: the group **binds a shader by name** (`steps_conc_m` — resolved to a
`0x00011000` Shader, C6), and it **declares its counts** (12 vertices, 14 indices) so a reader can size the
streams before reading them. The `0x2021` format word encodes which streams are present and how vertices
are laid out (🟡 — a bitfield; the exact bits are the open part).

Its children are the streams and a texture-coordinate/material hint:

```
0x00010011  flag (1 byte)
0x00010005  positions   (count + XYZ)     — C7.3
0x00010007  UVs         (count + UV)       — C7.3
0x00010008  colours     (count + RGBA)     — C7.3
0x0001000A  indices     (count + u32)      — C7.4
```

**Why it's built this way.** Batching by material is the universal rule of real-time rendering: the GPU
draws fastest when it can set one material and blast many triangles. A primitive group *is* a draw call —
one shader, one vertex batch, one index batch. Declaring counts up front lets the loader allocate exact
buffers, and naming the shader (rather than embedding it) lets many groups share one material.

**What happens if you bend it.**

- *Change a stream's length without updating `vertexCount`/`indexCount`* — the loader reads the wrong number
  of elements. The counts here and the stream counts (C7.3) must agree.
- *Point the group at a shader that isn't loaded* — the geometry draws untextured or fails to bind (C5.6).
  Ensure the named shader exists in the loaded set.
- *Misread the format word as a count* — `0x2021` is flags, not a number of anything; the counts are the
  explicit `0x0C`/`0x0E` fields. Read the fields in order.
