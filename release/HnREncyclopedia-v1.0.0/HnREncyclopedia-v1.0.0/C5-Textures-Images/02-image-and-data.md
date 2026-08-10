# C5.2 — Image & Image-Data (`0x00019001` / `0x00019002`)

**What it is.** The two chunks beneath a Texture: the **Image** (`0x00019001`), which is one encoded
picture, and the **Image-Data** (`0x00019002`) leaf inside it, which is the raw encoded bytes. The
Texture describes; the Image is the picture; the Image-Data *is* the file.

**How it works (✅ verified).** The Image's own data repeats the identifying header — name and dimensions —
so an Image is self-describing even lifted out of its Texture. Verified: in `art/cars/common.p3d` the
Image own-data begins with the same `flag.bmp`/dimensions pattern as its parent Texture, and its child
`0x00019002` leaf is 1,546 bytes of payload (`headerSize == chunkSize`, a pure leaf — C1.2).

The nesting exists because a Texture can, in principle, hold more than one Image (for multi-image
textures/mip chains): the Texture is the collection, each Image is one picture, and each Image's
Image-Data is that picture's bytes. In the common single-image case it is a straight three-level chain:

```
0x00019000 Texture      (name, w, h, bpp, mips…)
  0x00019001 Image      (name, w, h…)
    0x00019002 ImageData (raw encoded bytes)   ← leaf
```

**Why it's built this way.** The split lets the format carry mips and alternates uniformly: more Images
(or more Image-Data) simply nest under the Texture without a special case, and a decoder always finds the
pixels at the same place — the innermost leaf. It also keeps the raw bytes in a single contiguous leaf,
which is exactly what you want for a fast load (read the leaf straight into a GPU buffer) and for
extraction (slice one range — C5.4).

**What happens if you bend it.**

- *Edit the Image-Data length without fixing the Image and Texture sizes* — the classic size-tree break
  (C1.5); the walk desyncs at the next sibling. Always fix ancestors.
- *Assume exactly one Image per Texture* — usually true, but a mip chain or multi-image texture nests
  several. Walk to *every* `0x00019002` under the Texture, don't grab the first and stop.
- *Treat Image-Data as a specific format blindly* — its encoding is what the Texture header's `bpp`/`type`
  say (C5.3); read the descriptor before decoding the leaf.
