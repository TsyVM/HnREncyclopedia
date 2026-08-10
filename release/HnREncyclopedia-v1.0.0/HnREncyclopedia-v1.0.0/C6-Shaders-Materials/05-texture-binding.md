# C6.5 — Texture Binding (`0x00011002`)

**What it is.** The parameter that binds a texture to a shader — the link that puts a picture (C5) on a
material. A `0x00011002` names a texture and the *slot* it fills (diffuse, reflection, environment).

**How it works (✅ verified).** A `0x00011002` texture param is a **slot FourCC + a texture name** (a pstr).
Verified: in `art/cars/common.p3d`, a texture param reads `TEX` + `flarebase2.bmp` — slot `TEX` (the base
diffuse texture), bound to the texture named `flarebase2.bmp` (C5.1). Across the corpus other slots appear:

| Slot tag | Binds | Used by |
|---|---|---|
| `TEX ` | the base / diffuse texture | most shaders |
| `REFL` | a reflection texture | reflective methods |
| `ENVB` | an environment-map texture | environment-mapped methods |

The slot tag says *what role* the texture plays; the name resolves to a loaded Texture object (C5.6) by the
same name-lookup as the whole material graph. So a `simple` shader has a `TEX` slot (its diffuse map); a
shiny car shader adds a `REFL`/`ENVB` slot for its reflection. The **slot tags and the binding-by-name are
✅**; the exact per-slot semantics 🟡.

**Why slots.** A material may sample more than one texture — a diffuse map for colour and a reflection map
for shine. Naming each texture param with a *slot* (rather than assuming one texture) lets a shader bind
several, each to its role, and lets the method know which is which. This is standard multi-texture material
design: the diffuse in `TEX`, the reflection in `REFL`. The `simple` method uses just `TEX`; reflective
methods (C6.1) use `TEX` + `REFL`/`ENVB`. The slot is how the method finds the texture it needs.

**The full material graph.** This chunk is the middle link of the chain the book has traced since C5.6:

```
Mesh (C7) ──names──► Shader (C6.1) ──0x00011002 slot──► Texture (C5) ──► Image ──► pixels
```

A primitive group (C7.2) names a shader; the shader's `0x00011002` param names a texture; the texture holds
the image. Every link is a **name** stored in the clear, so the whole graph — what geometry uses what
material with what texture — is readable straight from the bytes. This is the payoff of SHAR keeping these
references as strings (C2, C5.6): the material system is legible and re-wireable by editing names.

**What happens if you bend it.**

- *Bind a texture name that isn't loaded* — the slot resolves to nothing; the surface renders untextured
  (often white). Ensure the texture's `.p3d` is loaded (C5.6, C14.2).
- *Use the wrong slot* — a reflection map in the `TEX` slot draws as the base texture. Match texture to slot.
- *Rename a texture without updating the shader's binding* — the link breaks (C5.6). Rename both ends.
