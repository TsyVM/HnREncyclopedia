# C1.3 — Walking the Tree

**What it is.** The two algorithms every Pure3D tool is built on: a **flat** walk of one level of
siblings, and a **recursive** walk of the whole tree. Both are a dozen lines; both are the same dozen
lines you will reuse in every chapter.

**How it works — the flat walk.** Read a header, yield it, step `chunkSize`, repeat until the region is
consumed. Bounds-check every step so a truncated or misaligned file stops cleanly instead of running
off the end.

```python
import struct

def walk(buf, start, end):
    """Yield (id, off, headerSize, chunkSize) for each chunk in [start, end)."""
    off = start
    while off + 12 <= end:
        cid, hlen, dlen = struct.unpack_from('<III', buf, off)
        if dlen < 12 or hlen < 12 or hlen > dlen or off + dlen > end:
            break                          # not a valid chunk boundary — stop
        yield cid, off, hlen, dlen
        off += dlen
```

**How it works — the recursive walk.** Descend into `[off+hlen, off+dlen)` whenever `hlen < dlen`. Carry
the absolute offset and depth so callers can patch and pretty-print.

```python
def walk_tree(buf, start, end, depth=0):
    for cid, off, hlen, dlen in walk(buf, start, end):
        yield cid, off, hlen, dlen, depth
        if hlen < dlen:                     # container
            yield from walk_tree(buf, off + hlen, off + dlen, depth + 1)
```

The same in C, for the tools that need to be fast or embeddable:

```c
void walk_tree(const uint8_t* buf, uint32_t off, uint32_t end, int depth,
               void (*visit)(uint32_t id, uint32_t off, uint32_t h, uint32_t d, int depth)) {
    while (off + 12 <= end) {
        uint32_t id, h, d;
        memcpy(&id, buf+off, 4); memcpy(&h, buf+off+4, 4); memcpy(&d, buf+off+8, 4);
        if (d < 12 || h < 12 || h > d || off + d > end) break;
        visit(id, off, h, d, depth);
        if (h < d) walk_tree(buf, off + h, off + d, depth + 1, visit);
        off += d;
    }
}
```

**Why it's built this way.** The walk needs no schema. It carries no table of "which ids have children"
because the size comparison answers that per instance (C1.2). That is what makes one walker correct for
all 179 ids and all 1,941 files — the property the census demonstrates.

**A dumper you will reuse (✅ reproduces the verified trees).**

```python
def dump(path):
    buf = open(path, 'rb').read()
    assert buf[:4] == b'P3D\xff'
    _, hs, fs = struct.unpack_from('<III', buf, 0)
    for cid, off, h, d, depth in walk_tree(buf, hs, min(fs, len(buf))):
        kind = 'C' if h < d else 'L'
        print(f"{'  '*depth}0x{cid:08X} [{kind}] h={h} d={d} @{off}")
```

Run it on `art/cars/common.p3d` and you get exactly the Texture→Image→ImageData nesting and the
primitive-group families shown in [C1.2](02-container-vs-leaf.md) — matching the census byte for byte.

**What happens if you bend it.**

- *Drop the `hlen > dlen` guard* and one corrupt chunk sends the recursion into a region that isn't a
  chunk stream; you either raise deep in the stack or print megabytes of noise. The four-part guard
  (`d<12 || h<12 || h>d || off+d>end`) is the minimum that keeps a bad file from becoming a bad day.
- *Recurse without a depth cap on hostile input* and a crafted file can blow the stack. For untrusted
  files add a `depth < 64` guard; the retail data never nests past the teens.
- *Forget to clamp `end` to the file length* (`min(fsize, len(buf))`) and a file whose header claims
  more than it contains will read past the buffer. Always clamp.
