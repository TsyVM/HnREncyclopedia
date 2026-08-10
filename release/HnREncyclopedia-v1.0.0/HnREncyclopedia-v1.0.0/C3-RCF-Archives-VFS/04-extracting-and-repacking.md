# C3.4 — Extracting & Repacking

**What it is.** The two operations you actually perform on an archive: pull a member out (read-only, easy
and safe) and put one back (a rewrite, with rules). Extraction is a slice; repacking is a size-tree
problem exactly like Pure3D's (C1.5), one level up.

**Extracting one member (✅ reproducible).** Hash the path, binary-search the sorted directory, slice:

```python
import struct
def extract(buf, path):
    key = radical_hash(path)                         # C2.2 (normalise first!)
    dir_off, = struct.unpack_from('<I', buf, 0x24)
    count,    = struct.unpack_from('<I', buf, dir_off)
    base = dir_off + 16
    lo, hi = 0, count
    while lo < hi:
        mid = (lo + hi) // 2
        h, off, size = struct.unpack_from('<III', buf, base + mid*12)
        if   h == key: return buf[off:off+size]
        elif h < key:  lo = mid + 1
        else:          hi = mid
    return None
```

**Extracting everything (even unnamed).** You do not need names to dump all members — walk the directory
and slice each entry, naming files by hash and classifying by magic:

```python
def extract_all(buf, outdir):
    dir_off, = struct.unpack_from('<I', buf, 0x24)
    count,    = struct.unpack_from('<I', buf, dir_off)
    base = dir_off + 16
    for i in range(count):
        h, off, size = struct.unpack_from('<III', buf, base + i*12)
        blob = buf[off:off+size]
        ext = {'P3D\xff'[:4].encode():'p3d', b'RSD4':'rsd'}.get(blob[:4], 'bin')
        open(f"{outdir}/{h:08X}.{ext}", 'wb').write(blob)
```

This is how you inventory an archive whose names you have not yet recovered: 125 blobs out of
`scripts.rcf`, each classified by its own magic, ready for C2.4 to name.

**Repacking — the rules.** An RCF is a header, a sorted directory, and a data region. To rebuild it after
changing a member:

1. **Lay out the data.** Place each (possibly resized) member in the data region, honouring the alignment
   the format uses (members start on aligned boundaries; the retail data region begins at `0x1000`).
   Record each member's new `offset` and `size`.
2. **Rebuild the directory.** For every member compute `{hash, offset, size}` and **sort the array by
   hash** — the engine's binary search depends on it (C3.2). A directory that isn't ascending will fail
   lookups for everything after the first misordered key.
3. **Fix the header and preamble.** Update `dataStart`/`dataSpan` in the directory preamble and the
   pointer at `0x24` if the directory moved.
4. **Write atomically.** Temp file, `fsync`, rename over the original (as with Pure3D, C1.5). A
   half-written archive can hang the game mid-load.

**Why resizing ripples.** Members are packed back-to-back in the data region, so growing one shifts every
member after it, which changes their offsets, which changes the directory. That is why you rebuild the
whole directory rather than patch one entry — the same "recompute from the leaves up" discipline as the
Pure3D size tree, applied to the archive's member table.

**What happens if you bend it.**

- *Patch one member's size in place* without moving the following members and you overlap the next
  member's data — instant corruption of everything downstream. Resize means relayout.
- *Forget to re-sort the directory* after adding a member and the binary search silently fails to find
  keys past the first inversion. Always sort by hash.
- *Change a member's path* expecting the archive to notice — the key is the *hash of the path*; a new
  path is a new key, and every requester must use the new path too (C3.3).
