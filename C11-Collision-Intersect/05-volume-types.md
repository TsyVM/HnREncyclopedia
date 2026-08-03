# C11.5 — Volume Types: Boxes, Cylinders, Spheres

**What it is.** The concrete primitive shapes a collision volume is built from. Under a `0x00121001`
volume, the typed sub-chunks `0x00121004`/`0x00121101`/`0x00121104`/`0x00121105`/`0x00121108`/`0x00121109`
are the individual boxes, cylinders, and spheres, each described by the FourCC vectors of C11.3.

**How it works (✅ verified presence; 🟡 exact type per id).** The volume tree of `art/b00 - Copy.p3d`
contains a spread of these sub-chunk ids (verified counts: `0x00121101` ×2, `0x00121104` ×1, `0x00121105`
×1, `0x00121108` ×1, `0x00121109` ×1, plus the object-level `0x00121004` bbox). Each is a small chunk
carrying the tagged vectors that parameterise one primitive. The mapping id→primitive-type is the 🟡 part:
by the FourCC tags a sub-chunk carries you can tell what it is —

- A sub-volume whose tags are **three half-extents + a centre** is an **oriented box (OBB)**.
- One with a **radius + a height/axis** is a **cylinder** (the natural shape for lamp-posts, characters).
- One with just a **radius + centre** is a **sphere** (cheap bounding tests).

The `WDT` (width) tag verified in C11.3 is one such dimension; the full tag set per id is recovered by the
C4.4 workflow across many files.

**Why several primitive types.** Different objects collide best as different shapes: a crate is an OBB, a
barrel or a character is a cylinder, a coin's trigger is a sphere. Giving the format a small palette of
primitives — rather than only mesh-collision (C11.4) — lets the common cases be *one cheap test* instead of
a walk over a vector list. Cylinders in particular are why SHAR's characters and posts feel right to bump:
a capsule/cylinder is the classic character collision shape.

**Choosing a type when authoring.** For a new collidable, pick the cheapest primitive that fits: sphere <
cylinder < box < mesh, in ascending cost and descending forgiveness. Most props want a box or cylinder;
reserve mesh-collision (the vector lists of C11.4) for terrain and complex static geometry where the shape
genuinely matters.

**What happens if you bend it.**

- *Use mesh-collision where a box would do* — you pay narrow-phase cost (a vector-list walk) for every
  contact. Prefer a primitive when the shape allows.
- *Give a cylinder box tags (or vice versa)* — the volume is misinterpreted and collides wrongly. Match the
  tag set to the primitive type.
- *Omit a required dimension tag* — an under-specified volume has undefined extent and may be non-solid or
  infinite. Provide the full tag set for the type (C11.3).
