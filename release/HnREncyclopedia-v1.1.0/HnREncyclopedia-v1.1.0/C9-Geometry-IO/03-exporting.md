# C9.3 — Exporting to OBJ & glTF

**What it is.** Writing the neutral representation (C9.1) out to a standard 3-D file — **OBJ** for simple
static geometry, **glTF** for richer content including skinned characters (C8). This is the "get it into
Blender" step.

**Exporting to OBJ (✅ reproducible).** OBJ is plain text: vertices (`v`), texture coords (`vt`), and faces
(`f`). From the neutral model (C9.1), converting the strip to a triangle list (C7.4) and axes at the boundary
(C9.2):

```python
def export_obj(mesh):
    out = [f"# {mesh['name']}  shader={mesh['shader']}"]
    for x, y, z in mesh['positions']:
        X, Y, Z = to_tool_space(x, y, z)          # C9.2
        out.append(f"v {X} {Y} {Z}")
    for u, v in mesh['uvs']:
        out.append(f"vt {u} {v}")
    for a, b, c in triangles_from_strip(mesh['indices']):   # C7.4
        out.append(f"f {a+1}/{a+1} {b+1}/{b+1} {c+1}/{c+1}")  # OBJ is 1-based
    return "\n".join(out)
```

OBJ is ideal for world props and static meshes — it's universally supported and trivial to write. Its limits:
no skinning, no per-vertex colour (the `0x00010008` colours, C7.3, are dropped or written as an extension),
one material reference via a companion `.mtl`. For static geometry, none of that matters.

**Exporting to glTF (for richer content).** glTF carries what OBJ can't: **per-vertex colours**, **materials**
(mapping the shader, C6, to a glTF material), **skinning** (joint weights + skeleton, C8), and **animation**.
For a skinned character (C8) you export glTF: the mesh, its skin weights, the skeleton hierarchy (C8.1), and
optionally the animation clips (C8.2). glTF is the right target whenever the geometry is more than a static
shape — which is most characters and animated props.

**Materials on export.** Both formats reference materials by name (the shader name from C9.1). For OBJ, write
a `.mtl` naming the shader and its diffuse texture (C6.5) so the tool shows the textured mesh. For glTF, map
the shader's params (C6.2–C6.5) to a glTF PBR/unlit material — `DIFF` colour, the `TEX` texture, etc. This
keeps the material binding through the round-trip (C9.5), so a re-import can re-bind the same shader (C9.4).

**Why two targets.** OBJ and glTF span the need: OBJ is the lowest-friction way to get static geometry into
any tool; glTF is the modern interchange that preserves skinning and materials for characters. Supporting
both from the neutral hub (C9.1) is two writers, and the modder picks per asset — OBJ to tweak a world prop,
glTF to edit a character rig.

**What happens if you bend it.**

- *Forget OBJ is 1-based* — off-by-one indices scramble faces. Add 1 to indices for OBJ.
- *Export a strip as a list without converting* — wrong triangles (C7.4). Convert topology.
- *Lose the material reference* — the mesh exports untextured. Write the `.mtl`/glTF material from the shader
  name (C6).
