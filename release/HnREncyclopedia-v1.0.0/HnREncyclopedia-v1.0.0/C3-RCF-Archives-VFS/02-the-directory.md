# C3.2 — The Directory: a Sorted Hash Table

**What it is.** The index at `dirOffset` that lists every member file. It is a count, a short preamble,
then a flat array of fixed 12-byte entries — and the array is **sorted by hash**, which makes lookup a
binary search.

**How it works (✅ verified on `scripts.rcf`).**

```
0x800:  count      uint32   = 125
0x804:  dataStart  uint32   = 0x1000     first member offset (page-aligned)
0x808:  (pad/align) uint32  = 0x1000
0x80C:  dataSpan   uint32   = 0x0043FDA0 total bytes covered by members
0x810:  entries[count] × {
            uint32 hash;      // Radical hash of the member's path (C2.2)
            uint32 offset;    // absolute byte offset of the member in the archive
            uint32 size;      // member length in bytes
        }
```

The first entries, read straight from the file:

| # | hash | offset | size |
|---:|---|---:|---:|
| 0 | `0x062B1126` | 2,584,576 | 331 |
| 1 | `0x0726F620` | 159,744 | 326 |
| 2 | `0x08972DA6` | 200,704 | 493 |
| 3 | `0x0BFF30DF` | 2,711,552 | 323 |
| 4 | `0x0ED04D31` | 2,695,168 | 327 |

**The key property: sorted by hash.** Notice the hash column strictly ascends
(`0x062B1126 < 0x0726F620 < 0x08972DA6 < …`) while the offsets do *not* — member data is scattered
through the file, but the *directory* is ordered by key. That is deliberate: the engine looks a file up
by hash with a **binary search** over this array, O(log n) instead of O(n). Your extractor should do the
same (C3.4).

**Why a hash table with no names.** Storing `{hash, offset, size}` and nothing else makes every entry a
fixed 12 bytes — no variable-length strings, no string heap, no second table to parse. The directory is
therefore a single contiguous sorted array you can `bsearch` directly in memory. The price, paid once at
build time, is that the human-readable paths are gone from the shipped archive (C3.3).

**Reading it, in full.**

```python
def read_directory(buf):
    dir_off, = struct.unpack_from('<I', buf, 0x24)          # C3.1
    count,    = struct.unpack_from('<I', buf, dir_off)
    base = dir_off + 16                                       # count + 3-word preamble
    entries = []
    for i in range(count):
        h, off, size = struct.unpack_from('<III', buf, base + i*12)
        entries.append((h, off, size))
    return entries      # already sorted by hash
```

**What happens if you bend it.**

- *Assume the entries start right after the count* (at `dirOffset+4`) and you are 12 bytes early, reading
  the preamble as a bogus first entry — the classic off-by-preamble. Entries start at `dirOffset+16`.
- *Linear-scan a directory you assume is unsorted* and you both waste time and miss the chance to detect
  corruption: if the hashes are *not* ascending, the archive is damaged or not what you think.
- *Trust `offset+size` blindly* — validate each entry lies within the file before slicing; a bad entry
  should be reported, not dereferenced.
