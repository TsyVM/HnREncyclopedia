# C10.5 — Sort Order (`0x03F00007`)

**What it is.** The chunk that records **draw order** — the sequence in which a node's drawables are
rendered. It is the single most common scene-graph chunk in the game (**10,311 instances**, ✅ verified),
which tells you how pervasively SHAR depends on getting draw order right.

**How it works.** `0x03F00007` encodes the order in which sibling drawables (C10.4) should be drawn. In a
real-time renderer, order matters in two big cases:

- **Transparency.** Semi-transparent surfaces (glass, water, the blob shadow of C15.6, particle-like decals)
  must draw *after* and *back-to-front* relative to what's behind them, or they blend against the wrong
  pixels. There is no depth trick that fixes transparency ordering for free; the geometry must be sequenced.
- **Layering.** Decals, ground markings, and coincident surfaces (a poster on a wall) must draw in a fixed
  order to avoid z-fighting.

The sort-order chunk is where the exported scene records that sequence so the runtime doesn't have to
rediscover it every frame.

**Why record it in data.** Sorting transparent geometry per-frame by distance is possible but expensive, and
for *static* scenery the order rarely changes — so baking it at export time (into these 10,311 chunks) trades
a one-time authoring cost for zero per-frame sorting of the static world. The count is high precisely because
almost every node with layered or transparent content carries one. That the *most common* scene-graph chunk
is about ordering, not geometry, is a quiet lesson: in a shipped renderer, *correct compositing* is as much
of the data as the shapes themselves.

**Reading and respecting it.** When you dump a scene (C4.2), treat sort-order chunks as the node's rendering
recipe. If you add transparent geometry to a node, it needs a place in the order; if you reorder or remove
drawables, the sort order must be updated to match, or transparency will render wrong even though every mesh
and texture is correct.

**What happens if you bend it.**

- *Add a transparent surface without sorting it* — it blends against whatever happened to draw first;
  windows go opaque or haloed. Insert it into the sort order.
- *Ignore sort order when merging nodes* — combining two nodes' drawables without merging their orders
  scrambles compositing. Rebuild the order for the merged set.
- *Assume z-buffering handles transparency* — it doesn't; that's why this chunk exists. Order transparent
  draws explicitly.
