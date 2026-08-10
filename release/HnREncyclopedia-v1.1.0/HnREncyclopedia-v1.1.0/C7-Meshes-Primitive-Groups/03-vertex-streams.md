# C7.3 — Vertex Streams: Positions, UVs, Colours

**What it is.** The per-vertex data of a primitive group, split into separate count-prefixed streams — one
for positions, one for texture coordinates, one for colours. Keeping them in parallel arrays (rather than
interleaved) is a defining choice of this format.

**How it works (✅ verified).** Each stream begins with a `u32` element count, then that many fixed-size
records. Decoded from `art/b00 - Copy.p3d` (a 12-vertex group):

- **Positions — `0x00010005`.** `count = 12`, then 12 × `(f32 x, f32 y, f32 z)`. Verified values:
  `(-24.03, 9.66, 64.64)`, `(-23.99, 9.61, …)` — real world-space coordinates. Total `4 + 12*12 = 148`
  bytes, matching the chunk exactly.
- **UVs — `0x00010007`.** `count`, then per-vertex texture coordinates as floats in roughly `[0,1]`
  (verified as small floats like `0.52, 0.49`; the exact component count per vertex is 🟡).
- **Colours — `0x00010008`.** `count = 12`, then 12 × `RGBA` byte quads with `0xFF` alpha (verified). Total
  `4 + 12*4 = 52` bytes, matching. These are per-vertex tint/lighting colours.

The streams are **parallel**: vertex *i*'s position, UV, and colour are element *i* of each array, tied
together by the index buffer (C7.4).

**Why parallel streams.** Separate arrays let the exporter and the GPU treat each attribute independently —
you can have positions without colours, or add a colour stream without touching positions — and they map
cleanly onto the hardware's multiple vertex streams. It also makes editing surgical: recolour a mesh by
rewriting only `0x00010008`, leaving positions untouched. The cost is that all streams must stay the same
length (one entry per vertex), which the group's `vertexCount` (C7.2) enforces.

**Reading real geometry.** With positions decoded you can compute a mesh's bounding box yourself and check
it against the mesh-level bounds (C7.1) — a clean cross-check (C4.4). The 12 positions of this group
enclose a small step object (`steps_conc_m` = "steps concrete"), exactly what the name suggests.

**What happens if you bend it.**

- *Give the streams different lengths* — position/UV/colour arrays must all equal `vertexCount`; a mismatch
  reads garbage for the short one. Keep them equal.
- *Interleave the data* expecting the loader to cope — the format is parallel arrays; interleaving desyncs
  the stream. Write each attribute as its own count-prefixed block.
- *Forget to re-encode positions when changing the coordinate system* — SHAR uses its own axes; convert at
  the export boundary (C7.5), not inside the stream.
