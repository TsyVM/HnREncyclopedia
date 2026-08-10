# C11.2 — The Collision Volume Tree (`0x00121001` / `0x00121002`)

**What it is.** The hierarchy inside a Collision Object: a named Collision Volume that nests sub-volumes
and the vectors describing them. It is a tree so the engine can reject most of an object with a few cheap
tests before checking detail.

**How it works (✅ verified).** `0x00121002` is the bounding-volume container; inside it a `0x00121001`
**Collision Volume** is itself named and holds the pieces. Verified from `art/b00 - Copy.p3d`:

```
0x00121002 (container, 2,215 B)     the bounding volume
  0x00121001 Collision Volume  name="flareShape"
     0x00121100 ×5   collision vectors (FourCC-tagged — C11.3)
     0x00121101 ×2   sub-volume
     0x00121104 ×1   sub-volume
     0x00121105 ×1   sub-volume
     0x00121108 ×1   sub-volume
     0x00121109 ×1   sub-volume
```

The volume carries a name (`flareShape`) and a child count, then its children: a mix of **vectors** (the
geometry primitives, C11.3) and **further sub-volumes** (`0x00121101`/`104`/`105`/`108`/`109`, the typed
shapes of C11.5). Because a volume can contain volumes, an object's collision is a nested set of shapes,
each with its own bounds.

**Why a tree.** Collision testing is the hottest loop in the physics engine — it runs for every moving
object every frame. A flat list of surfaces would force a test against every one; a tree lets the engine
test a parent's bounds first and skip its entire subtree on a miss. For a dense world (the census shows
hundreds of thousands of collision leaves), that pruning is the difference between playable and not. The
named volumes also let tools and scripts reference specific parts of an object's collision.

**Walking it.** Use the same recursive walker as everything else (C1.3): descend `0x00121002`/`0x00121001`
containers, collect `0x00121100` vectors and typed sub-volumes at the leaves. The volume tree is just a
Pure3D chunk subtree — no special parser, only knowledge of which ids are shapes vs. vectors.

**What happens if you bend it.**

- *Flatten the tree* (put every vector under one volume) — you lose the broad-phase pruning and collision
  gets slow. Preserve the nesting.
- *Add a sub-volume without updating the parent's child count* — the walk reads the wrong number of
  children and desyncs. Keep counts consistent (the C1.5 discipline, applied to volumes).
- *Leave a sub-volume outside the parent's bounds* — it may never be tested (pruned away). Ensure each
  parent volume's bounds enclose its children.
