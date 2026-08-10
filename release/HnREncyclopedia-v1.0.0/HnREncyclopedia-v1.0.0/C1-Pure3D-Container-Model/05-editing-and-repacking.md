# C1.5 — The Size Tree in Practice: Editing & Repacking

**What it is.** The discipline that keeps a `.p3d` loadable after you change it. Because `chunkSize` is
inclusive and containers nest, the size fields form a **balanced accounting tree**. Edit any leaf and
you owe a fix-up to every chunk above it, all the way to the file header.

**The invariant.** For every container:

```
container.chunkSize  ==  container.headerSize  +  Σ over direct children ( child.chunkSize )
```

and for the file as a whole, `fileHeader.chunkSize == len(file)`. A file that violates either is
malformed; the engine's loader will desync exactly where your walker would.

**How it works — the three edit classes.**

1. **In-place, same length.** Retune a float, recolour a pixel, swap a matrix — anything that keeps a
   chunk's byte length identical. No size changes, no fix-ups. This is the safe 90% of modding: a car's
   `.con` handling values (Chapter 15) never touch `.p3d` sizes at all, and many texture edits (a DXT
   block for a same-format DXT block) are length-preserving.

2. **Grow or shrink a leaf.** Replace a 1,546-byte image with a 2,000-byte one and that leaf's
   `chunkSize` rises by 454 — and so must every ancestor's, by the same 454. You walk from the edited
   chunk up its parent chain adding the delta to each `chunkSize` (leaf headers have no children to
   worry about; only ancestors change).

3. **Add or remove a chunk.** Splice a new child into a container and its `chunkSize` grows by the new
   child's full `chunkSize`; every ancestor grows by the same amount. Removing is the mirror image.

**The ancestor fix-up, in code.**

```python
def rebuild(chunks):
    """chunks: nested dicts {id, header_bytes, children:[...]}. Return serialised bytes with
    every chunkSize recomputed bottom-up so the size tree balances."""
    def emit(c):
        body = b''.join(emit(ch) for ch in c['children'])
        header_size = 12 + len(c['header_bytes'])
        chunk_size  = header_size + len(body)
        return (struct.pack('<III', c['id'], header_size, chunk_size)
                + c['header_bytes'] + body)
    return b''.join(emit(c) for c in chunks)
```

Recomputing sizes **bottom-up** — children first, then the parent that contains them — is the whole
technique. You never hand-maintain a `chunkSize`; you serialise children, measure, and write the total.
This is also why parsing into a tree and re-emitting is safer than in-place byte-poking for anything
that changes length: the rebuild *cannot* leave a stale ancestor size.

**Atomic writes.** Serialise to a temporary file, `fsync`, then rename over the original. A half-written
`.p3d` is worse than an unmodified one — the game may load part of it and crash mid-level. The rename is
the commit.

**Worked example (✅ grounded in the verified tree).** In `art/cars/common.p3d`, growing the
`0x00019002` Image-Data leaf (`chunkSize 1546`) by 100 bytes forces:

```
0x00019002 ImageData  1546 → 1646   (+100, the edit)
0x00019001 Image       1599 → 1699   (+100, ancestor)
0x00019000 Texture     1660 → 1760   (+100, ancestor)
file header            (whole file)  +100
```

Four numbers change for one edit; miss any one and the walk desyncs at the first chunk after the short
count.

**What happens if you bend it.**

- *Grow a leaf but forget an ancestor* and the parent's `chunkSize` now ends *before* the real data
  ends; the next-sibling step lands mid-data and every later chunk is garbage. The game usually fails to
  load the file or drops the asset.
- *Fix ancestors but not the file header* and standalone tools that trust the header total will truncate
  or over-read. Include the file header in the chain.
- *Edit bytes in place across a length change* (e.g. a hex editor insert) without rebuilding and you
  will almost certainly leave a stale size somewhere. For any length change, parse → edit tree →
  `rebuild()` → atomic write. Reserve in-place poking for strictly same-length edits.
