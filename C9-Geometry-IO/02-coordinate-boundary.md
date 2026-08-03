# C9.2 — The Coordinate Boundary

**What it is.** The single rule that keeps geometry from coming out mirrored, rotated, or inside-out: convert
between SHAR's coordinate system and your tool's **only at the export/import boundary**, never inside the
parser. It's the geometry analogue of the endianness and matrix rules (C1).

**How it works.** SHAR stores positions and matrices in the engine's own axis convention (C10.3 — read
straight, no transpose). Most DCC tools (Blender, Maya) and glTF use Y-up, right-handed; the engine's
convention may differ in axis order and/or handedness. The conversion is a fixed transform applied to every
position and normal:

```python
def to_tool_space(x, y, z):   # apply ONCE, at export
    return (x, z, -y)         # example Z-up → Y-up (🟡 — confirm for SHAR, below)

def to_engine_space(x, y, z): # the inverse, at import
    return (x, -z, y)
```

The exact mapping is 🟡 — it must be *confirmed*, not assumed (below) — but the *principle* is firm: the
conversion lives in the export writer and the import reader, and nowhere else.

**Why only at the boundary.** If you convert inside the parser (C7.3), every tool that reads the parser now
disagrees with the file — the dumper (C4.2) prints converted coordinates, the collision (C11) and the mesh
no longer match, and a re-export double-converts. Keeping the parser *faithful to the file* (engine
coordinates) and converting only in the interchange writer/reader means: the on-disk data, the dumper, and
all internal tools agree with each other and with the game; only the *exchanged* OBJ/glTF is in tool space.
This is the same discipline as decompressing at the boundary (C1.9) — transform where you cross a boundary,
not before.

**Confirming the mapping.** Don't guess the axis order — *measure* it (C4.4). Export a mesh whose real-world
orientation you know (a car, which has an obvious front/up), open it in your tool, and check: is it upright?
facing the right way? not mirrored? If it's on its side, your axis swap is wrong; if it's mirrored, your
handedness is wrong. Adjust the boundary transform until a known mesh comes out correct, then it's right for
all meshes. This is a one-time calibration that fixes the whole pipeline.

**Handedness and winding.** A coordinate conversion that flips handedness also flips triangle **winding** —
front faces become back faces, and the mesh looks inside-out (backface-culled surfaces vanish). If your
export flips handedness, reverse the triangle winding too (swap two indices per triangle). The tell is a mesh
that's oriented right but has holes where you can see through it — that's inverted winding, not bad geometry.

**What happens if you bend it.**

- *Convert in the parser* — everything internal disagrees with the file. Convert only at the boundary.
- *Guess the axis order* — you get mirrored/rotated meshes. Calibrate against a known mesh (C4.4).
- *Flip handedness without fixing winding* — the mesh renders inside-out. Reverse winding when you flip
  handedness.
