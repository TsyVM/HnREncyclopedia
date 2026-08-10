# C1.2 — Container vs. Leaf: a Size Comparison, Not a Flag

**What it is.** The rule that decides whether a chunk holds child chunks. In Pure3D it is not a bit and
not a lookup table — it is a comparison of the two size fields:

```c
int is_container(const P3DChunk* c) { return c->headerSize < c->chunkSize; }
```

**How it works.** A container reserves the span `[off+headerSize, off+chunkSize)` for children. If that
span is empty — `headerSize == chunkSize` — there are no children and the chunk is a leaf. There is no
third case: `headerSize` is never greater than `chunkSize` in a well-formed file (that would claim the
"own data" runs past the end of the whole chunk), and a walker should treat `headerSize > chunkSize` as
corruption and stop.

**Why it's built this way.** An alternative design would encode container-ness as a *flag bit* in the id
(so the same conceptual thing needs two ids — one flagged, one not), coupling *role* (container/leaf) to
*type* (the id). Pure3D instead **decouples** them: the id means only "what type," and the *structure*
(two sizes) means "does it have children." The pay-off is that the **same id can be a container in one
place and a leaf in another**, depending only on whether that particular instance was given children — the
reader never has to care, because it is only ever comparing sizes.

**Evidence (✅ verified).** The census tags every chunk instance as container or leaf by this exact
comparison, and it classifies all 2.1 million chunk instances in the retail tree without contradiction
— the same test that lets the parser finish all 1,941 files. Of the 179 distinct ids, 93 occur as
containers. A clear example is the Texture/Image nest in `art/cars/common.p3d`:

```
0x00019000 Texture      headerSize=61   chunkSize=1660   → container
  0x00019001 Image      headerSize=53   chunkSize=1599   → container
    0x00019002 ImageData headerSize=1546 chunkSize=1546  → leaf (raw pixels)
```

The Texture and Image carry a little of their own data *and* nest a child; the Image-Data at the bottom
is pure bytes. The tree bottoms out exactly where `headerSize == chunkSize`.

**Ids that are both.** Because role is structural, do not hard-code "id X is always a leaf." A locator
group (`0x00015800`) is a container when it holds locators and effectively a leaf when empty; a shader
param may or may not nest a texture reference. Always branch on the size comparison, never on a
remembered list. The one safe generalisation: a chunk whose `headerSize == 12` has *no own data*, so if
it is also a leaf (`chunkSize == 12`) it is an empty placeholder.

**What happens if you bend it.**

- *Assume a fixed leaf/container role per id* and you will either miss children (treating a container as
  a leaf) or walk garbage (treating a leaf's data as child headers). The size comparison costs one
  subtraction; use it every time.
- *Emit `headerSize > chunkSize`* when authoring a chunk and the engine's loader will read your "own
  data" past the chunk end into the next sibling — a guaranteed load corruption. Keep
  `12 ≤ headerSize ≤ chunkSize` as an invariant of everything you write.
