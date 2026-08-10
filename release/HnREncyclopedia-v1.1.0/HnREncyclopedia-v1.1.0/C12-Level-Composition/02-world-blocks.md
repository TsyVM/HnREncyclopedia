# C12.2 — World Blocks & LODs (`b**.p3d`)

**What it is.** The chunks of a level's world geometry, split into **blocks** so the game can load only what's
near the player, with **level-of-detail (LOD)** variants so distant geometry is cheaper.

**How it works (✅ verified).** The block set is `b00.p3d`, `b01.p3d`, … (11 base blocks verified in `art/`),
each paired with a **`b0Ndata.p3d`** companion (the block's data/collision split from its drawables), and some
blocks carry **LOD variants**:

```
b02.p3d      full-detail block 02
b02data.p3d  its data/collision
b02l.p3d     large / far LOD
b02m.p3d     medium LOD
b02s.p3d     small / near LOD
b02st.p3d    street LOD
```

The `l`/`m`/`s`/`st` suffixes are detail tiers: the game shows the high-detail block up close and swaps to
`m`/`l` versions as it recedes, with `st` (street) a specialised tier. Splitting each block's *drawables*
(`b02.p3d`) from its *data* (`b02data.p3d`) lets the two be streamed and managed separately — you can keep a
block's collision resident while swapping its visual LOD.

**Why blocks and LODs.** Two independent problems, two solutions. **Blocks** solve *spatial* budgeting: the
world is too big to load whole, so it's cut into regions and only nearby ones are resident (C12.3). **LODs**
solve *detail* budgeting: even a resident block shouldn't draw full detail when it's far away, so cheaper
versions stand in at distance. Together they keep both memory and rendering cost bounded no matter how large
the world or how far you can see — the two classic open-world scaling techniques, both visible in the file
naming.

**Reading the block set.** A level's blocks tell you its spatial layout: dump the `b**.p3d` set (C4.2) and you
see the world's regions. The `data` companions carry the collision (C11) and the invisible road/fence data
(C13); the LOD variants carry progressively simpler drawables (C7). Which blocks are resident where is decided
by the streaming system (C12.3), driven by the level script.

**What happens if you bend it.**

- *Edit `b02.p3d` but not its LOD variants* — your change appears up close but the old geometry shows at
  distance. Edit every LOD tier for a consistent result.
- *Edit the drawable block but not its `data` companion* — visuals change but collision/roads don't (C11/C13).
  Edit both halves.
- *Assume all blocks are always loaded* — they stream by proximity (C12.3). A change to a distant block won't
  show until it's resident.
