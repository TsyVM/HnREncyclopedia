# C9.1 — The Neutral Representation

**What it is.** The format-agnostic in-memory model that sits between Pure3D geometry (C7) and any external
format. Export reads Pure3D *into* it; import writes Pure3D *from* it; and OBJ/glTF/anything reads and writes
it. It's the hub that keeps the pipeline from being N×M format converters.

**How it works.** Read a primitive group's streams (C7.2–C7.4) into a plain structure with no target format
assumed:

```python
def read_mesh(buf, group):
    return {
      'name':      group_name(group),          # C7.1
      'shader':    group_shader(group),         # C7.2 — the material name (C6)
      'positions': read_stream(group, 0x00010005),  # [(x,y,z), …]
      'uvs':       read_stream(group, 0x00010007),  # [(u,v), …]
      'colours':   read_stream(group, 0x00010008),  # [(r,g,b,a), …]
      'indices':   read_indices(group, 0x0001000A),  # triangle strip (C7.4)
      'topology':  'strip',                     # from the format word (C7.2)
    }
```

Everything a mesh *is* — geometry, attributes, material reference, topology — lives here in a neutral form.
Crucially it keeps the **shader name** (C6): geometry without its material reference is only half a mesh, and
a re-import needs to re-bind the same shader.

**Why a neutral hub.** Without it, every source format needs a converter to every target format — Pure3D→OBJ,
Pure3D→glTF, OBJ→Pure3D, and so on, N×M converters. With a neutral representation, each format needs only a
*reader* (format→neutral) and a *writer* (neutral→format) — N+M, and any source can reach any target through
the hub. This is the standard interchange-format architecture (glTF itself plays this role industry-wide),
applied to SHAR geometry. It's also the C4.6 "fixed substrate" idea: the neutral model is stable, and format
readers/writers accumulate around it.

**What it deliberately drops and keeps.** The neutral form is *geometry-level* — it keeps what defines the
shape and its material binding, and drops Pure3D container mechanics (chunk headers, sizes) that are the
*format's* concern, not the *geometry's*. On import, those mechanics are regenerated (C9.4). This separation —
geometry in the neutral model, container mechanics in the Pure3D reader/writer — is why export/import can be
lossless (C9.5) without the neutral model knowing anything about chunk sizes.

**Extending it for skins and collision.** A skinned character (C8) adds joint weights and a skeleton
reference to the neutral model; collision (C11) is its own neutral form (volumes + tags). The same hub idea
scales: add fields for the extra data, add readers/writers that handle them. glTF (C9.3) can carry skins, so
the extended neutral model exports cleanly to it.

**What happens if you bend it.**

- *Drop the shader name* — the re-imported mesh has no material and renders untextured (C6.5). Keep the
  reference.
- *Bake a target format into the model* (e.g. store OBJ 1-based indices) — you lose the neutral hub's
  generality. Keep it format-agnostic (0-based, engine axes).
- *Forget the topology* — a strip read as a list scrambles triangles (C7.4). Carry the topology from the
  format word (C7.2).
