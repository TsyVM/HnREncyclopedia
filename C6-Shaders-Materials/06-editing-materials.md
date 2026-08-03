# C6.6 — Editing Materials

**What it is.** How to change how a surface looks by editing its shader — recolour it, retexture it, make it
shiny or matte, two-sided or one-sided. Because shader params are small tagged values (C6.2–C6.5), most
material edits are length-preserving and safe.

**How it works.** Material edits map onto the parameter families:

- **Recolour** → edit a `0x00011005` colour param (C6.4). Tint the surface with `DIFF`, make it glow with
  `EMIS`, change the highlight colour with `SPEC`. Each is a 4-byte RGBA swap — length-preserving (C1.5), no
  repack.
- **Retexture** → edit the `0x00011002` texture binding (C6.5) to name a different texture, or replace the
  texture the shader points at (C5.5). The former re-wires the material; the latter changes the picture every
  user of that shader shows.
- **Change shininess** → edit the `SHIN` float (C6.3). Higher = shinier, tighter highlight; lower = matte.
- **Change render state** → edit a `0x00011003` integer flag (C6.2): flip `2SID` to make a surface
  two-sided (visible from behind), change `BLMD` for transparency, adjust `ACTH`/`ATST` for alpha cut-outs.

All of these are edits to fixed-size tagged params — the shader's byte length doesn't change, so there's no
size-tree fix-up (C1.5) and no repack. This is why material tweaks are among the safest mods (alongside
`.con` handling, C15, and UI XML, C21): change a value, save, done.

**The two edit scopes.** A material edit's *reach* depends on what you touch:

- **Edit the shader** → affects every mesh that uses that shader. If many surfaces share `steps_conc_m`,
  editing it changes all of them.
- **Give a mesh its own shader** → to change *one* surface, first duplicate its shader under a new name and
  point the mesh at the copy (C7.2), then edit the copy. Now the edit is isolated.

This is the same shared-resource caution as textures (C5.6) and drawables (C10.4): the material is shared by
reference, so editing it is a broadcast unless you first make a private copy.

**A worked example.** To make a car's body shiny: find its body shader (by name, e.g. in a dump, C4.2), set
its `SHIN` float (C6.3) higher, ensure `SPEC` (C6.4) is a non-black colour (so there's a highlight to
sharpen), and — for a reflection — add a `REFL` texture slot (C6.5) if the method supports it. Four tagged
values, all length-preserving. To make a fence two-sided so you see it from both sides: flip its shader's
`2SID` (C6.2) to 1.

**What happens if you bend it.**

- *Edit a shared shader expecting a local change* — every user changes. Copy the shader first for a local
  edit.
- *Turn on reflection without a reflective method* — the `simple` method (C6.1) may ignore a `REFL` slot.
  Use a method that supports it.
- *Change a param's length* — params are fixed-size; don't add bytes. Edit values in place (length
  -preserving) and the size tree stays valid (C1.5).

**Next:** [Chapter 7 — Meshes & Geometry](../C7-Meshes-Primitive-Groups/C7-Meshes-Primitive-Groups.md).
