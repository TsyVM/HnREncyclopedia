# Chapter 3 — RCF Archives & the Virtual File System

> **Goal of this chapter:** open any of the ten `RADCORE CEMENT LIBRARY` archives, read its directory,
> pull a member file out by name, and understand how the archives and the loose `art/`/`scripts/` trees
> together form the game's virtual file system.

Most of *The Simpsons: Hit & Run* by weight does not sit in loose files — it sits inside **ten `.rcf`
archives at the game root, 1.43 GB in total**. All of the audio (six archives), the cutscene data
(`nis.rcf`), and the compiled scripts (`scripts.rcf`) are packed. An `.rcf` is a **RadCore Cement
Library**: a fixed header, then a directory that locates each member file by the **Radical hash of its
path** (Chapter 2), then the file data. There are no stored filenames — the directory is pure
`{hash, offset, size}` — which is why Chapter 2 came first.

Everything on this page is ✅ verified against `scripts.rcf` with `tools/p3d_rcf_scan.py` and a short
directory parser; the exact offsets and the 125-entry count are read straight from the shipped file.

---

## Deep-dive pages

- [C3.1 — The Cement Library Header](01-cement-library-header.md): the magic, the version, and the pointer to the directory.
- [C3.2 — The Directory: a Sorted Hash Table](02-the-directory.md): count, preamble, and the `{hash, offset, size}` entries — verified sorted by hash.
- [C3.3 — Hash Addressing: Files Without Names](03-hash-addressing.md): why there are no filenames, and what that means for you.
- [C3.4 — Extracting & Repacking](04-extracting-and-repacking.md): pulling a member out, and the rules for putting one back.
- [C3.5 — The Ten Shipped Archives](05-the-ten-archives.md): what each `.rcf` holds and how big it is.
- [C3.6 — The Virtual File System at Runtime](06-vfs-and-runtime.md): how packed and loose files resolve to one namespace.

---

## 3.1 The header (✅ verified)

An `.rcf` opens with the ASCII magic string **`RADCORE CEMENT LIBRARY`** (22 bytes), zero-padded to
offset `0x20`. Then a small fixed header:

```
0x00:  "RADCORE CEMENT LIBRARY\0\0\0\0\0\0\0\0\0\0"   (32 bytes, magic + pad)
0x20:  01 02 00 01     version   = 0x01000201
0x24:  00 08 00 00     dirOffset = 0x00000800   → the directory
0x28:  00 00 00 00
0x2C:  00 08 00 00     0x00000800  (a second pointer; data region base — see C3.6)
0x30..0x3F: zero
```

The one pointer you need is at `0x24`: the **directory offset**, `0x800` in `scripts.rcf`. Full detail in
[C3.1](01-cement-library-header.md).

## 3.2 The directory (✅ verified)

At `dirOffset` the directory begins with a count and a short preamble, then a flat array of 12-byte
entries:

```
0x800:  7D 00 00 00     count      = 125 entries
0x804:  00 10 00 00     dataStart  = 0x1000  (first member's offset; data is page-aligned)
0x808:  00 10 00 00     0x1000
0x80C:  A0 FD 43 00     0x0043FDA0 (total data span)
0x810:  entries[125] × { uint32 hash; uint32 offset; uint32 size; }
```

Verified entry 0: `hash=0x062B1126, offset=2,584,576, size=331`. The entries are **sorted in ascending
hash order** (`0x062B1126 < 0x0726F620 < 0x08972DA6 < …`), which means lookup is a **binary search** — a
property the engine relies on and you should too. [C3.2](02-the-directory.md) walks the whole structure.

## 3.3 Files are addressed by hash, not name (✅ verified)

The directory stores **no filenames** — only the 32-bit Radical hash of each member's path. To find a
file you hash its path (C2.2) and binary-search the sorted keys. This is the single most important fact
about RCF and the reason name recovery (C2.4) matters: extracting *by name* requires you to know, or
recover, the paths that were hashed. [C3.3](03-hash-addressing.md).

## 3.4 Extracting a member (✅ reproducible)

Given the directory, a member is just a slice `[offset, offset+size)` of the archive:

```python
def read_member(buf, key):
    count, = struct.unpack_from('<I', buf, 0x800)
    base = 0x810
    lo, hi = 0, count
    while lo < hi:                                   # binary search — entries sorted by hash
        mid = (lo + hi) // 2
        h, off, size = struct.unpack_from('<III', buf, base + mid*12)
        if h == key:   return buf[off:off+size]
        if h < key:    lo = mid + 1
        else:          hi = mid
    return None
```

Repacking has the same size-tree discipline as Pure3D (C1.5): change a member's length and you must
rewrite offsets and the total span. [C3.4](04-extracting-and-repacking.md).

## 3.5 The ten archives

| Archive | Size | Holds |
|---|---:|---|
| `music00`–`music03.rcf` | ~908 MB | Streamed music (four sets) |
| `dialog.rcf` | 173.0 MB | Character dialogue |
| `soundfx.rcf` | 135.3 MB | Sound effects |
| `ambience.rcf` | 102.5 MB | World ambience |
| `nis.rcf` | 88.4 MB | Cutscene (NIS) data |
| `carsound.rcf` | 20.6 MB | Vehicle audio |
| `scripts.rcf` | 2.7 MB | Compiled scripts (125 members) |

Detail and per-archive contents in [C3.5](05-the-ten-archives.md).

## 3.6 One namespace, two backings

At runtime the game resolves an asset path without caring whether it lives loose in `art/` or packed in
an `.rcf`. The VFS layers the archives over the loose tree so a `LoadP3DFile("art\…")` call (Chapter 14)
finds its target either way. [C3.6](06-vfs-and-runtime.md) covers the resolution order and how mods
exploit it by shadowing packed files with loose ones.

---

## Key takeaways

- Ten root `.rcf` archives (`RADCORE CEMENT LIBRARY`) hold 1.43 GB — all audio, cutscenes, and compiled
  scripts.
- Header: magic to `0x20`, version `0x01000201`, directory offset at `0x24`.
- The directory is a **count + preamble + array of `{hash, offset, size}`**, **sorted by hash** →
  binary-searchable. Verified: 125 entries in `scripts.rcf`.
- Members are addressed by the **Radical hash of their path**; no filenames are stored, so extraction by
  name needs recovered paths (C2.4).
- Packed and loose files share one runtime namespace, which is what makes loose-file modding possible.

**Next:** [Chapter 4 — Byte-Level Toolcraft](../C4-Byte-Level-Toolcraft/C4-Byte-Level-Toolcraft.md).
