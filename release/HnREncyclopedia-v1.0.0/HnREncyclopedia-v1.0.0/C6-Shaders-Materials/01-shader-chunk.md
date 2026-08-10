# C6.1 — The Shader Chunk & Method Name

**What it is.** The `0x00011000` Shader chunk itself — a named material with a **method** (the shading
technique) and a set of typed parameters (C6.2–C6.5). It's the material a mesh binds to (C7.2) and the thing
that decides how a surface looks.

**How it works (✅ verified).** The own data is two length-prefixed strings, then the parameters as child
chunks. Decoded from `art/cars/common.p3d`:

```
0C "flarebase2_m"      pstr: the shader's NAME (the _m suffix = "material")
00 00 00 00            a u32 (0)
08 "simple\0\0"        pstr: the METHOD name (null-padded to 8 — C6 note)
… then child param chunks (0x00011002–0x00011005) …
```

The **name** (`flarebase2_m`) is how meshes reference the shader (C7.2 — a primitive group names its shader).
The **method** (`simple`) selects the shading technique — how the parameters are interpreted and the surface
drawn. `simple` is the basic textured/lit method; other methods drive reflection, environment mapping, and
special effects (the `REFL`/`ENVB` texture slots, C6.5, imply reflective methods exist).

**Why a named method.** A shader isn't arbitrary code here — it names one of a fixed set of engine **methods**
(shading techniques), and the parameters (C6.2–C6.5) configure that method. This is the same "pick a
technique, parameterise it" model as the mission objectives (choose a type, set its params, C16.3) and the
collision volumes (choose a shape via its FourCC tags, C11.3). The method is the *what to do*; the parameters
are the *with these values*. A `simple` shader with a diffuse texture and colours draws a basic lit surface; a
reflective method with an environment texture draws a shiny one.

**Why names, not hashes.** Shader names are stored **in the clear** (like textures, C5, and meshes, C7) —
`flarebase2_m` is readable in the bytes. This is what makes the material graph legible (C5.6): a mesh names
its shader, a shader names its textures, all as strings you can read and re-wire. The `_m` naming convention
(material) makes shaders easy to spot in a dump.

**The parameter children.** A shader's children are its parameters, one chunk per typed value (C6.2–C6.5):
`0x00011002` texture slots, `0x00011003` integers, `0x00011004` floats, `0x00011005` colours. A typical
`simple` shader carries ~16 integer params, a few floats, and four colours — the counts are remarkably
uniform across the ~11,000 shaders in the game (C6.2), because they're all the same material model with
different values.

**What happens if you bend it.**

- *Rename a shader without updating the meshes that reference it* — the meshes' shader references break
  (C7.2); surfaces lose their material. Rename both ends (C5.6).
- *Set a method the engine doesn't implement* — the shader has no technique to run. Use a known method
  (`simple` and the reflective/environment methods).
- *Corrupt a pstr length* — the name/method read shifts into the parameters. Preserve the length bytes and
  the null-padding (C6 note).
