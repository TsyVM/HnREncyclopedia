# C11.4 — Vector Lists & the BVH (`0x00121110` / `0x00121111`)

**What it is.** The two bulk leaves of the collision system: the **vector list** (`0x00121110`) — the
single most common collision chunk and the second-most-common chunk in the entire game — and the
**bounding-volume hierarchy** (`0x00121111`), the spatial tree that makes collision fast.

**How it works (✅ verified for structure).** `0x00121110` is a **count-prefixed list of vectors**:

```
00 00 00 00        (flags)
01 00 00 00        count
… vectors …        `count` × vector data (positions/normals of the surface)
```

Verified: the leaf is small and count-prefixed; across the game it occurs **147,655 times**, because every
collidable surface contributes one. These lists hold the vertices/planes that make up a mesh-collision
volume — the fine geometry the narrow-phase tests once the broad-phase has narrowed the candidates.

`0x00121111` (**26,382 instances**) is the **BVH**: a tree of bounding volumes over those vectors. The
engine descends it to turn "which of thousands of surfaces might I be touching?" into a handful of
candidates in log time. It is the same idea as the volume tree (C11.2) but applied *within* a
mesh-collision to its many faces.

**Why these dominate the census.** A world is mostly *surfaces you can touch*: every wall, road, kerb, and
prop face is collision. Each is a small vector list, and each mesh-collision carries a BVH over its faces.
So the two leaves that describe "a surface" and "how to find it fast" are, unsurprisingly, the most
numerous chunks in the game after the shader parameters (C6) that describe how everything looks. The census
ranking — shader params, then collision vector lists — is a fingerprint of what the game *is*: a dense,
touchable, richly-shaded world.

**Working with them.** For extraction or analysis, treat `0x00121110` as a vertex/plane array (count then
data) and `0x00121111` as an acceleration structure you can often ignore when *reading* (it's derived from
the vectors) but must *rebuild* when you change the geometry it indexes. That rebuild is the collision
equivalent of the size-tree fix-up (C1.5): change the surface, regenerate its BVH.

**What happens if you bend it.**

- *Edit a vector list but not its BVH* — the broad-phase points at stale bounds and can miss or falsely
  report collisions. Regenerate the BVH after changing surfaces.
- *Miscount the list* — a wrong count reads past the vectors or truncates the surface. The count prefix is
  load-bearing; keep it exact.
- *Delete "redundant" vector lists to save space* — each is a real surface; removing one makes that face
  non-solid. They are numerous because the world is, not by waste.
