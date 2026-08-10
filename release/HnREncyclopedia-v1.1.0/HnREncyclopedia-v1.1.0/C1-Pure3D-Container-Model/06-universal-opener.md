# C1.6 — A Universal Opener & Dumper

**What it is.** The hardened, reusable tool that opens *any* file in the game, decides what it is, and —
for Pure3D — prints its tree. It is the practical distillation of C1.1–C1.5 and the thing you actually
run first on every unknown file for the rest of this book. It is the same logic as the shipped
[`tools/p3d_rcf_scan.py`](../tools/p3d_rcf_scan.py) that verified the whole data set.

**How it works.** Identify by magic, then branch. Only Pure3D gets the recursive dump; the other
formats are handed to their own chapters.

```python
import struct

MAGICS = {
    b'RADCORE CEMENT LIBRARY': 'rcf',      # C3
    b'P3D\xff':                'pure3d',   # this chapter
    b'BIK':                    'bink',     # C20 (.rmv)
    b'RSD4':                   'rsd',      # C18
    b'\x89PNG\r\n\x1a\n':      'png',      # C5
}

def identify(head):
    if head[:22] == b'RADCORE CEMENT LIBRARY': return 'rcf'
    for magic, name in MAGICS.items():
        if head.startswith(magic): return name
    if head.lstrip()[:5] == b'<?xml': return 'scrooby'   # C21 (.pag)
    if head[:2] in (b'//', b'Se', b'Lo'): return 'script' # C14/C15/C17
    return 'unknown'

def walk_tree(buf, start, end, depth=0):
    off = start
    while off + 12 <= end:
        cid, h, d = struct.unpack_from('<III', buf, off)
        if d < 12 or h < 12 or h > d or off + d > end: break
        yield cid, off, h, d, depth
        if h < d:
            yield from walk_tree(buf, off + h, off + d, depth + 1)
        off += d

def open_file(path, names=None):
    buf = open(path, 'rb').read()
    kind = identify(buf[:32])
    if kind != 'pure3d':
        return kind, buf                      # hand off to the right chapter
    _, hs, fs = struct.unpack_from('<III', buf, 0)
    tree = list(walk_tree(buf, hs, min(fs, len(buf))))
    return 'pure3d', tree

def dump(path, names=None):
    kind, data = open_file(path)
    print(f"{path}: {kind}")
    if kind != 'pure3d': return
    for cid, off, h, d, depth in data:
        label = (names or {}).get(cid, '')
        role = 'C' if h < d else 'L'
        print(f"{'  '*depth}0x{cid:08X} [{role}] h={h} d={d} @{off} {label}")
```

**Why it's built this way.** One entry point, magic-first, so you never mis-parse a Bink file as Pure3D.
The dump is deliberately *toolkit-agnostic*: no external library, no per-format schema, just the header
model. Feed it the [master chunk table](../Glossary/chunk-ids.md) as `names` and the dump annotates
every id with its (🟡 reasoned) name.

**Using it.** For any mystery file: `dump("art/whatever.p3d")`. The shape of the tree tells you the
asset class before you decode a single payload byte — a Texture-heavy tree is an image atlas, a
`0x03F0xxxx`-heavy tree is a scene graph (Chapter 10), a `0x00121xxx`-heavy tree is collision (Chapter
11). This is how each later chapter starts: dump, recognise the family, then decode.

**Extending it.** Every subsequent chapter adds a *decoder* for one chunk family — a function that takes
the `(buf, off, h, d)` of a chunk and returns structured fields. The opener stays fixed; only the
decoders grow. That separation — a frozen walker plus a growing set of decoders — is the architecture of
the whole toolkit, and of the DonutsSDK data library that mirrors it.

**What happens if you bend it.** Skipping `identify()` and assuming `.p3d` files are always Pure3D is
usually fine — but the moment you point the tool at a directory that also holds `.rmv` or `.rcf`, the
magic branch is what saves you from a confident, wrong parse. Keep the front door.
