# Chapter 11 — Collision & Intersect

> **Goal of this chapter:** decode the collision family — the second-largest chunk family in the game by
> count — into named collision objects, their volume trees, and the FourCC-tagged vectors that describe
> each volume. After this chapter you can read the collision of any object and understand how the game
> decides what the player, cars, and NPCs can touch.

Collision is enormous in SHAR: the vector-list leaf `0x00121110` alone occurs **147,655 times** (the
second-most-common chunk in the whole game), and the `0x0012xxxx` family accounts for a large fraction of
all chunk instances. This is the invisible geometry — separate from the visible mesh (C7) — that the
physics and gameplay systems test against. Everything below was decoded from `art/b00 - Copy.p3d` with
`tools/p3d_rcf_scan.py`.

**Key finding (✅ verified):** collision is a **named, hierarchical** system built on a **FourCC parameter**
model, structurally similar to the shader system (C6). A Collision Object carries a name
(`BQG_flareShape`), holds a Collision Volume tree, and each volume is described by tagged vectors like
`WDT` (width) — self-describing key/value geometry.

---

## Deep-dive pages

- [C11.1 — The Collision Object (`0x00121000`)](01-collision-object.md): the named root and its bbox.
- [C11.2 — The Collision Volume Tree (`0x00121001`/`0x00121002`)](02-volume-tree.md): named volumes and their nesting.
- [C11.3 — Collision Vectors & the FourCC Model (`0x00121100`)](03-vectors-fourcc.md): `WDT`-tagged params describing each volume.
- [C11.4 — Vector Lists & the BVH (`0x00121110`/`0x00121111`)](04-vector-lists-bvh.md): the game's most common leaf and the broad-phase tree.
- [C11.5 — Volume Types: Boxes, Cylinders, Spheres](05-volume-types.md): the `0x00121004`/`101`/`104`/`105`/`108`/`109` sub-chunks.
- [C11.6 — Collision at Runtime (`0x00121200` Intersect DSG)](06-runtime.md): the DSG collision entities and how they're tested.

---

## 11.1 The Collision Object (✅ verified)

A `0x00121000` Collision Object is **named** and holds the collision for one thing. Verified own data from
`art/b00 - Copy.p3d`:

```
00 00 00 00                 (index/flags)
10 "BQG_flareShape\0\0"     pstr (len 16, null-padded): the object name
42 51 47 …                  "BQG" type tag + floats (extents)
```

Its children are a **bounding volume** (`0x00121002`, a container 2,215 bytes deep) and a **bbox/count leaf**
(`0x00121004`). The name ties this collision to the drawable of the same base name (`…flareShape` — the
mesh of C7), so collision and geometry are matched by name. [C11.1](01-collision-object.md).

## 11.2 The Collision Volume tree (✅ verified)

Inside sits a `0x00121001` **Collision Volume**, itself **named** (`flareShape`), which holds the actual
sub-volumes and vectors:

```
0x00121001 Collision Volume  name="flareShape"
  0x00121100 ×5   Collision Vector  (FourCC-tagged — C11.3)
  0x00121101 ×2   sub-volume
  0x00121104 ×1   sub-volume
  0x00121105 ×1   sub-volume
  0x00121108 ×1   sub-volume
  0x00121109 ×1   sub-volume
```

The volume nests further volumes and vectors — a **tree**, which is what lets the broad-phase (C11.4)
reject most of an object cheaply before testing detail. [C11.2](02-volume-tree.md).

## 11.3 The FourCC vector model (✅ verified)

The leaf that describes a volume's geometry is `0x00121100`, and it uses the **same FourCC trick as
shaders (C6)**: a four-char tag plus typed data. Verified: a `0x00121100` reads tag `WDT` (width) followed
by its value. So a volume is a set of tagged scalars/vectors — `WDT` width, and (🟡, by analogy) radius,
half-extents, axes — a self-describing description of a box, cylinder, or sphere. [C11.3](03-vectors-fourcc.md).

## 11.4 The most common leaf, and the BVH (✅ verified)

`0x00121110` is the **vector list** — 147,655 instances, the game's second-most-common chunk — a compact
count-prefixed list of vectors that make up a volume's surface. `0x00121111` (26,382) is the **bounding
-volume hierarchy**: the spatial tree the engine descends to find candidate volumes fast. Together they are
why collision is so numerous: every collidable surface in every level is a small pile of these leaves.
[C11.4](04-vector-lists-bvh.md).

## 11.5 & 11.6 Volume types and runtime

The `0x00121004`/`101`/`104`/`105`/`108`/`109` sub-chunks are the concrete primitive types — boxes,
cylinders, spheres — each a few tagged vectors (C11.5). At runtime a collision object becomes a
`CollisionEntityDSG` / `AnimCollisionEntityDSG` / `IntersectDSG` (`0x00121200`) — RTTI-verified classes
(names ✅, offsets ⏳) — tested by the physics system (C26). [C11.6](06-runtime.md).

---

## Key takeaways

- Collision is the **second-largest** chunk family: `0x00121110` alone occurs **147,655** times (✅).
- It is **named and hierarchical**: Collision Object (`0x00121000`, named) → Collision Volume
  (`0x00121001`, named) → sub-volumes + vectors, matched to geometry by name.
- Volumes use a **FourCC parameter model** (`0x00121100`, tag `WDT`=width) like shaders (C6).
- The **vector list** (`0x00121110`) and **BVH** (`0x00121111`) are the bulk leaves and the broad-phase.
- At runtime these become `CollisionEntityDSG`/`IntersectDSG` (names ✅, offsets ⏳; C26).

**Next:** [Chapter 12 — Level Composition](../C12-Level-Composition/C12-Level-Composition.md).
