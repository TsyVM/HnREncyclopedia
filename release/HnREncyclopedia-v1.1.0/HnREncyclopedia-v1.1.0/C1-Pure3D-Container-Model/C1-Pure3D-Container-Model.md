# Chapter 1 — The Pure3D Container Model

> **Goal of this chapter:** after reading it you can open *any* `.p3d` file in the game, walk its
> structure, and know whether a given block is "more structure" or "raw data" — without a parser
> written for that specific asset. You will also be able to edit one safely and write it back so the
> game still loads it. Everything else in this book builds on this one idea.

*The Simpsons: Hit & Run* stores almost all of its art — every texture, mesh, skeleton, animation,
collision volume, scene-graph node, and locator — as a **Pure3D chunk tree**. A `.p3d` file is not a
bespoke format with a hand-written header per asset type; it is a recursive sequence of
self-describing blocks called **chunks**. Master this single concept and the 264 MB of `art/` stops
being a wall of binary and becomes a navigable hierarchy you can dump, diff, edit, and rebuild with a
dozen lines of code that never change from one asset to the next.

This is verified ground, not received wisdom. The parser in [`tools/p3d_rcf_scan.py`](../tools/p3d_rcf_scan.py)
walks **all 1,941 plain `.p3d` files in the retail tree with zero parse failures**, using nothing but the
rules on this page — the strongest possible evidence that the model below is correct and complete for
the shipped data. The other **28** files carrying the `.p3d` extension are a *compressed* variant
(magic `P3DZ`) that must be decompressed first; they are the subject of [C1.9](09-compressed-p3dz.md),
and together the census is an honest **1,941 plain + 28 compressed = 1,969**.

---

## Deep-dive pages

The overview below is the map. Each core mechanism then gets a focused page covering **what it is, how
it works, why it's built that way, and what happens if you bend it** — the right way or the wrong way.

- [C1.1 — The 12-Byte Chunk Header](01-the-chunk-header.md): `id`, `headerSize`, `chunkSize`, and the three questions each answers.
- [C1.2 — Container vs. Leaf: a Size Comparison, Not a Flag](02-container-vs-leaf.md): why Pure3D decides recursion structurally, from a size comparison rather than a flag bit.
- [C1.3 — Walking the Tree](03-walking-the-tree.md): the iterative and recursive walkers, in C and Python, bounds-checked.
- [C1.4 — The File Header & the `P3D\xff` Magic](04-the-file-header.md): the 12-byte file preamble and the version byte.
- [C1.5 — The Size Tree in Practice: Editing & Repacking](05-editing-and-repacking.md): in-place edits, ancestor fixups, atomic writes.
- [C1.6 — A Universal Opener & Dumper](06-universal-opener.md): a complete, portable tool you reuse in every later chapter.
- [C1.7 — Failure Modes & Forensics](07-failure-modes.md): how to read a desynced walk and find the byte that broke it.
- [C1.8 — The Runtime View: How `radLoadObject` Walks the Same Tree](08-runtime-view.md): the loader, the handler dispatch, and streaming-in-place.
- [C1.9 — The Compressed Variant: `P3DZ`](09-compressed-p3dz.md): the compression boundary — 28 level-05 mission assets that must be decompressed before any chunk is visible.

---

## 1.1 The chunk header

Every chunk begins with a **12-byte, little-endian** header of three `uint32`:

```c
struct P3DChunk {
    uint32_t id;          // chunk type identifier
    uint32_t headerSize;  // bytes of THIS chunk's header + own data (where children begin)
    uint32_t chunkSize;   // TOTAL bytes of this chunk, including all children
};
```

The bytes from `off+12` up to `off+headerSize` are this chunk's **own data**. The bytes from
`off+headerSize` up to `off+chunkSize` are its **child chunks**, if any. Immediately after
`off+chunkSize` comes the next sibling. A file is therefore just a sequence of chunks, each of which
may contain more chunks — with the sizes telling you exactly where every boundary is.

This is verified: on `art/cars/common.p3d` (9,763 bytes, 130 chunks) the very first header reads
`id=0x00019000, headerSize=61, chunkSize=1660` — a Texture container whose 1,599 bytes of children
begin 61 bytes in. [C1.1](01-the-chunk-header.md) takes the three fields apart in full.

## 1.2 Container or leaf? Compare two sizes

The single most important rule in Pure3D:

> If `headerSize < chunkSize`, the chunk is a **container**: the region
> `[off+headerSize, off+chunkSize)` is itself a sequence of chunks. If `headerSize == chunkSize`, the
> chunk is a **leaf**: it has data but no children.

```c
static inline int is_container(const struct P3DChunk* c) { return c->headerSize < c->chunkSize; }
```

Pure3D makes container-ness a **structural** property: you compare the two sizes, rather than reading a
flag bit out of the id. You never have to guess whether to recurse — the header tells you,
and it tells you *exactly how far* the children run. The census bears this out: of 179 distinct chunk
IDs, **93 appear as containers** at least once. [C1.2](02-container-vs-leaf.md) explores the
consequences, including IDs that are containers in one file and leaves in another.

## 1.3 Sizes are inclusive — step `chunkSize`

The Pure3D `chunkSize` is the **total** length of the chunk, header included (note: *inclusive* — it
counts its own 12-byte header, not just the payload). To advance to the next sibling you step `chunkSize`
bytes — not `chunkSize + 12`, and not `headerSize`. Because a container's children live entirely inside
its `chunkSize`, the sizes form a strict accounting tree:

```
container.chunkSize  ==  headerSize  +  Σ over children ( child.chunkSize )
```

The consequence that bites every modder: **change the length of any chunk's data and every ancestor's
`chunkSize` is now wrong.** Fixing that from the edited chunk up to the root is the "ancestor-size
fixup" that governs all repacking — see [C1.5](05-editing-and-repacking.md).

## 1.4 Walking a chunk stream

The minimal correct walk, bounds-checked so a malformed file stops cleanly instead of crashing:

```python
import struct
def walk(buf, start, end):
    off = start
    while off + 12 <= end:
        cid, hlen, dlen = struct.unpack_from('<III', buf, off)
        if dlen < 12 or off + dlen > end:
            break                      # truncated or not a chunk boundary
        yield cid, off, hlen, dlen     # id, absolute offset, header size, total size
        off += dlen                    # step the TOTAL size
```

To traverse the whole tree, recurse into `[off+hlen, off+dlen)` whenever `hlen < dlen`. The full
recursive walker with absolute-offset bookkeeping (which you need for patching) is
[C1.3](03-walking-the-tree.md). A tree-printing dump built on it is the most useful twenty lines in
your toolbox: run it against an unknown file and the ids alone tell you what you are looking at (match
them against [the master table](../Glossary/chunk-ids.md)).

## 1.5 The file header comes first

A `.p3d` file opens with a 12-byte **file header** that is itself shaped like a chunk header:

```
50 33 44 FF   0C 00 00 00   21 09 00 00
"P3D\xff"     headerSize=12  fileSize=2337
```

The magic is `id = 0xFF443350` — the ASCII `"P3D"` followed by `0xFF`. `headerSize = 12` says the real
chunk stream begins at offset 12; `chunkSize` is the whole file length. So the file is, elegantly, one
outermost chunk. Always start your walk at offset **12**, and always test the magic first.
[C1.4](04-the-file-header.md) covers the version byte and the (rare) big-endian console variants.

## 1.6 Everything is little-endian

Every field in a PC-retail `.p3d` is little-endian: the three header `uint32`, the counts, the floats,
the matrices. (The GameCube and Xbox builds of the engine use big-endian and a different swizzle, but
those are not the retail PC data set this book documents.) When a "count" reads as an absurd number
like `0x0A000000`, you have almost certainly stepped by the wrong amount and are reading mid-chunk, not
misreading endianness — see the forensics in [C1.7](07-failure-modes.md).

## 1.7 Putting it together — a universal opener

```python
def open_pure3d(path):
    buf = open(path, 'rb').read()
    if buf[:4] != b'P3D\xff':
        raise ValueError('not a Pure3D file')
    _, hsize, fsize = struct.unpack_from('<III', buf, 0)
    return list(walk(buf, hsize, min(fsize, len(buf))))
```

From here, each later chapter takes a specific chunk id (or family) and tells you how to read its
data. The complete, hardened version — with a recursive dumper, a hex fallback, and error handling —
is built step by step in [C1.6](06-universal-opener.md), and you carry it into every other chapter.

## 1.8 The same tree, seen by the engine

Everything above is how *your* tools read the file. The engine reads it almost identically: RadCore's
loader (`radLoadObject` and the Pure3D chunk-handler registry) walks the chunk stream, compares
`headerSize` against `chunkSize` to decide whether to descend, and dispatches each recognised id to a
registered handler that builds a live object. Unknown ids are skipped harmlessly by stepping
`chunkSize`. Understanding that the game and your dumper run the *same* walk is what makes reverse
engineering tractable: a file the game loads is a file your correct walker can also parse. The runtime
side is [C1.8](08-runtime-view.md).

---

## Key takeaways

- A chunk is `{ id, headerSize, chunkSize }` (12 bytes) + data + children; step **`chunkSize`**.
- `headerSize < chunkSize` ⇒ container (recurse into `[off+headerSize, off+chunkSize)`); equal ⇒ leaf.
- Sizes are **inclusive** of the header (`chunkSize` counts its own 12 bytes). The size tree must balance:
  `container.chunkSize == headerSize + Σ(child.chunkSize)`. Fix ancestors after any length change.
- A file begins with a 12-byte header; magic `50 33 44 FF` (`"P3D\xff"`); real chunks start at offset 12.
- Little-endian throughout on PC retail.
- **Decompress first:** a file may be the compressed variant (`P3DZ`); test for it before walking (C1.9).
- Your dumper and the engine's loader run the same walk — which is what makes the format learnable.

**Next:** [Chapter 2 — Identifiers & Radical Hashing](../C2-Identifiers-And-Hashing/C2-Identifiers-And-Hashing.md),
because the names inside these chunks — and the keys of the archives that hold them — are stored as
32-bit numbers, not text.
