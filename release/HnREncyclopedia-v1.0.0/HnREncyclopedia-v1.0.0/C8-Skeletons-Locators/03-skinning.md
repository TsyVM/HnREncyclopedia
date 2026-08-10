# C8.3 — Skinning (`0x00017002` / `0x00017001`)

**What it is.** The binary chunk that binds a mesh to a skeleton so the mesh **deforms** as the joints move
— the difference between a rigid prop and a character whose body bends. `0x00017002` is the Skin;
`0x00017001` is its skin data.

**How it works (✅ verified).** A `0x00017002` Skin, decoded from `art/chars/apu_electrocuted.p3d`, names a
**shape** and a **shader** and carries skin data:

```
00 00 00 00
10 "homercute1Shape\0"     pstr: the mesh this skin deforms
0C "apucuted_m\0"          pstr: the shader (C6) it draws with
… flags …
  0x00017001  skin data (weights / joint bindings)
```

So a Skin ties three things together: the **mesh** (C7) whose vertices deform, the **shader** (C6) it draws
with, and the **skin data** (`0x00017001`) that says, per vertex, which joints influence it and by how much.
When the skeleton (C8.1) poses, each vertex is transformed by a weighted blend of its influencing joints —
classic skeletal skinning. The 1:1 pairing of `0x00017002`/`0x00017001` (verified: 48 of each in one level
block) is one skin-data block per skin.

**Why skinning is separate from the mesh.** A plain mesh (C7) is drawn with one transform (C10.3); a *skin*
needs a *per-vertex* blend of *many* joint transforms. Keeping the skin as its own chunk — referencing the
mesh rather than replacing it — lets the same mesh format serve both rigid props and deforming characters,
and keeps the heavy per-vertex weight data out of the plain-mesh path. It also means a character's mesh,
shader, and skeleton are independently editable: reskin without re-rigging, retexture without re-skinning.

**The full character stack.** A character is therefore: a **skeleton** (joints), a **mesh** (C7, the body
geometry), a **skin** (`0x00017002`, binding mesh vertices to joints), a **shader/texture** (C6/C5, the
look), a **`.cho` rig** (C8.1, the roles and IK), and an **animation-state graph** (C8.2, the behaviour).
Six layers, each in its own chunk or file, each independently moddable — which is why Simpsons characters
could be given so many costumes and animations.

**What happens if you bend it.**

- *Edit the mesh's vertex count without updating the skin data* — weights no longer line up with vertices
  and the character deforms into spikes. Keep skin data in step with the mesh (the C7.5 rebuild, extended
  to weights).
- *Bind to a skeleton with different joint names* — weights reference joints that don't exist. Match the
  skin's joints to the skeleton (C8.1).
- *Treat a skinned mesh as rigid* — drawing it with one transform ignores the deformation; it must go
  through the skin path. Read `0x00017002`, not just the mesh.
