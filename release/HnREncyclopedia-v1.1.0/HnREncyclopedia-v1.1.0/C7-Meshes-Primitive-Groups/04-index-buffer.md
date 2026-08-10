# C7.4 — The Index Buffer (`0x0001000A`)

**What it is.** The list that turns the vertex arrays (C7.3) into actual triangles. Instead of repeating
vertices, the geometry stores each vertex once and references it many times by position — the index
buffer is those references.

**How it works (✅ verified).** `0x0001000A` is `u32 count`, then `count` × `u32` indices. Verified from
`art/b00 - Copy.p3d`: `count = 14`, then indices `0, 6, 1, 7, 3, …`. Each index selects an element of the
parallel streams (C7.3): index `6` means "use position[6], UV[6], colour[6]." Fourteen indices for twelve
vertices, forming a connected surface — the pattern (0,6,1,7,3…) is a **triangle strip**, where each new
index adds a triangle using the previous two vertices.

```python
def triangles_from_strip(indices):
    for i in range(len(indices) - 2):
        a, b, c = indices[i], indices[i+1], indices[i+2]
        # every other triangle is wound the opposite way in a strip
        yield (a, c, b) if (i & 1) else (a, b, c)
```

**Why indices, and why strips.** Indexing decouples the *number of vertices* from the *number of triangle
corners*: a cube has 8 vertices but 36 triangle corners, and indexing stores the 8 once. Triangle **strips**
go further — after the first triangle (3 indices), each additional index adds a whole triangle, so `n`
triangles need `n+2` indices instead of `3n`. On 2003 hardware that saved both memory and vertex-transform
work. The verified 14-index/12-vertex group is a strip precisely because the format favours them.

**Bounds and safety.** Every index must be `< vertexCount` (C7.2). An index out of range points past the
stream — the classic way a hand-edited mesh crashes the renderer. A correct reader validates
`max(indices) < vertexCount` before trusting the buffer (a C4.1 bounds check applied to geometry).

**What happens if you bend it.**

- *Emit an index ≥ `vertexCount`* — the renderer reads past a stream; at best a stray vertex, at worst a
  crash. Validate the range.
- *Assume a triangle **list** when it's a **strip*** (or vice versa) — you get scrambled or degenerate
  triangles. The format word (C7.2, `0x2021`) and the index/vertex ratio indicate the topology; strips are
  the common case here.
- *Reorder vertices without remapping indices* — the surface tears, because indices reference by position.
  If you rebuild the streams, rebuild the indices to match (C7.5).
