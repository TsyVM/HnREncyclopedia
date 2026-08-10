# C5.4 — Extracting Textures

**What it is.** Getting a picture out of a `.p3d` and into a file you can open. It is a straight
application of the toolkit (C4): walk to the Image-Data leaf, read the descriptor for context, write the
payload out.

**How it works.** Two reads and a write:

```python
import struct
def extract_textures(path, outdir):
    buf = open(path, 'rb').read()
    assert buf[:4] == b'P3D\xff'
    _, hs, fs = struct.unpack_from('<III', buf, 0)
    for cid, off, h, d, depth in walk_tree(buf, hs, min(fs, len(buf))):   # C1.3
        if cid != 0x00019000:            # Texture
            continue
        # name + dims from the descriptor (C5.1)
        nlen = buf[off+12]
        name = buf[off+13:off+13+nlen].decode('latin-1')
        w, hh = struct.unpack_from('<II', buf, off+13+nlen+4)
        # find this Texture's Image-Data leaf(s)
        for c2, o2, h2, d2, dep2 in walk_tree(buf, off+h, off+d):
            if c2 == 0x00019002:         # Image-Data (raw payload)
                payload = buf[o2+12 : o2+d2]
                open(f"{outdir}/{name}", 'wb').write(payload)
                print(f"{name}: {w}x{hh}, {len(payload)} bytes")
```

Because the Texture carries its **name in the clear** (C5.1), extracted files land with their real names —
`flag.bmp`, `flarebase2.bmp` — no hash recovery needed. The descriptor also gives you the dimensions to
print or to validate the payload against.

**Why this is easy here.** The payload is a single contiguous leaf (C5.2), so extraction is one slice — no
reassembly, no de-swizzling in the common case. And the format is close to a desktop image (C5.3), so the
written file often opens directly. This is the pay-off of the container model: once you can walk the tree,
pulling any leaf out is trivial and identical for every asset type.

**Batch extraction.** Point the same loop at a whole directory to dump every texture in a level, or feed
it packed textures pulled from an `.rcf` (C3.4) — the walk is the same whether the `.p3d` came loose or
out of an archive. A level's entire texture set falls out in one pass, named.

**What happens if you bend it.**

- *Grab the first `0x00019002` and stop* — you miss multi-image textures and mip levels (C5.2). Iterate all
  leaves under the Texture.
- *Write the payload with the wrong extension* — the bytes are fine but your image viewer may refuse them.
  Use the name's real extension, or sniff the payload magic (C5.3) and name accordingly.
- *Ignore the dimensions* — extracting without checking `w×h` against the payload size hides corruption.
  Cross-check: a 64×64 paletted image should be about `64*64` index bytes plus a palette.
