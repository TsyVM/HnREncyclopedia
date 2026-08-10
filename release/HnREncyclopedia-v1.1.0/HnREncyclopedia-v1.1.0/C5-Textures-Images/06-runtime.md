# C5.6 — Textures at Runtime

**What it is.** How a texture stops being bytes on disk and becomes a picture on a triangle. A texture is
inert until a **shader** (Chapter 6) names it and a **mesh** (Chapter 7) uses that shader — this page is
the seam between the three.

**How it works.** The chain has three links, each verified in its own chapter:

1. **Texture** (`0x00019000`, C5.1) — carries the picture and its plaintext name, e.g. `flarebase2.bmp`.
2. **Shader** (`0x00011000`, C6) — a shader's texture parameter `0x00011002` stores a FourCC `TEX` tag and
   the **name** of the texture it wants (verified: a `0x00011002` param in `art/cars/common.p3d` reads
   `TEX` + `flarebase2.bmp`). The loader resolves that name to the loaded Texture object.
3. **Mesh** (`0x00010000`, C7) — a mesh's primitive group (`0x00010002`) names the **shader** it draws
   with (verified: `steps_conc_m`). So the mesh points at a shader, and the shader points at a texture.

The result is a name-resolved graph: **mesh → shader → texture**, wired by strings the loader looks up as
it builds each object. Because textures and shaders both carry plaintext names, this graph is readable
directly from the bytes — you can trace a triangle to its picture without running the game.

**Why it's built this way.** Indirection through the shader means many meshes can share one shader, and one
shader can be re-pointed at a different texture, without touching geometry. It is the standard material
system: geometry references materials, materials reference textures. SHAR's contribution is to keep the
references as **names**, not hashes (C2), inside these families — which is a gift to modders, because the
whole material graph is legible and re-wireable by editing strings.

**The runtime object.** At load the texture becomes an engine texture object (the RTTI class set includes
the Pure3D drawable/texture families; names ✅ from RTTI, offsets ⏳ — C23). Binding is by the name lookup
above; the GPU upload uses the descriptor's dimensions and format (C5.1/C5.3).

**What happens if you bend it.**

- *Rename a texture but not the shader that references it* — the shader's `TEX` name no longer resolves and
  the surface loses its texture (often shows as untextured/white). Rename both ends together.
- *Replace a texture a shared shader points at* — every mesh using that shader changes. If you wanted to
  change one surface only, give it its own shader first.
- *Reference a texture that isn't loaded* — the bind fails at runtime. Ensure the texture's `.p3d` is loaded
  (C14.2) before the shader that needs it.

**Next:** [Chapter 6 — Shaders & Materials](../C6-Shaders-Materials/C6-Shaders-Materials.md).
