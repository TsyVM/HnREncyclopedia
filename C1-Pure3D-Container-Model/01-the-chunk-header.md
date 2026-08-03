# C1.1 — The 12-Byte Chunk Header

**What it is.** The single structure the entire Pure3D format is built from. Three little-endian
`uint32`, twelve bytes, at the start of every chunk in every `.p3d` file:

```c
struct P3DChunk {
    uint32_t id;          // +0  chunk type
    uint32_t headerSize;  // +4  header + own data length
    uint32_t chunkSize;   // +8  total length incl. children
};
```

**How it works.** The three fields answer three separate questions, and keeping them separate is the
whole trick.

- `id` — *what is this?* A 32-bit type code. `0x00019000` is a Texture, `0x00011000` a primitive
  group, `0x03F00003` a scene-graph transform. The complete list of the 179 ids that actually occur is
  the [master table](../Glossary/chunk-ids.md). Ids are not ASCII (contrast EA's FourCCs); they are
  opaque numbers organised into families (Chapter 2).
- `headerSize` — *where does my own data end?* Everything from `off+12` to `off+headerSize` is this
  chunk's private payload: its counts, floats, name, matrix. If `headerSize == 12` the chunk has a
  type but no payload of its own — it exists purely to group children.
- `chunkSize` — *where does the next sibling start?* Total bytes, header included. `off + chunkSize`
  is the next chunk. Nothing else advances the cursor correctly.

**Why it's built this way.** Two sizes instead of one buys the format its most useful property: a chunk
can carry *both* its own data *and* children, and a reader can find both without knowing the chunk's
type. `headerSize` splits "my data" from "my children"; `chunkSize` bounds the whole thing. A generic
loader (yours or the engine's) can therefore skip a chunk it doesn't recognise — step `chunkSize` — or
descend into one it does — start at `off+headerSize`, stop at `off+chunkSize` — with no per-type
knowledge at all. That is exactly why unknown ids never crash the engine: it steps over them.

**Worked example (✅ verified).** The first header of `art/cars/common.p3d`:

```
19 00 01 00   3D 00 00 00   7C 06 00 00
id=0x00019000 headerSize=61  chunkSize=1660
```

`headerSize (61) < chunkSize (1660)`, so this Texture is a container: 61 bytes of its own data
(dimensions, format, mip count — Chapter 5), then `1660 − 61 = 1599` bytes of child chunks (its Image,
`0x00019001`, and the Image's data, `0x00019002`). The next sibling texture begins at offset
`12 + 1660 = 1672`.

**What happens if you bend it.**

- *Read `chunkSize` where you meant `headerSize`* and you will treat a container's children as opaque
  payload — you'll "see" the texture but never find its image. Harmless, but you get nothing.
- *Step `headerSize` instead of `chunkSize`* and you land **inside** the first child, read a child's
  bytes as a sibling header, and desync for the rest of the file. This is the number-one beginner bug;
  the forensic signature is in [C1.7](07-failure-modes.md).
- *Step `chunkSize + 12`* overshoots every chunk by 12 (double-counting the header) and desyncs immediately.
  Pure3D `chunkSize` is **inclusive** of the header — step exactly `chunkSize`, no more.

**The rule to memorise:** own data is `[off+12, off+headerSize)`; children are
`[off+headerSize, off+chunkSize)`; the next sibling is `off+chunkSize`.
