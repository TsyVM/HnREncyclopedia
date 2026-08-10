# C1.9 — The Compressed Variant: `P3DZ`

**What it is.** A second Pure3D container magic — **`P3DZ`** (`50 33 44 5A`) — that wraps a
**block-compressed** Pure3D file. It is a compression boundary: a file that
must be **decompressed before any chunk header is visible**. It is not a different asset format — inside,
it is an ordinary `P3D\xff` chunk tree (C1.1–C1.8); it is only stored compressed.

**Where it occurs (✅ verified).** Of the 1,969 files carrying the `.p3d` extension in the retail tree,
**1,941 begin `P3D\xff` (plain) and exactly 28 begin `P3DZ` (compressed)**. All 28 sit in a single
directory — `art/missions/level05/` — and are the mission, camera, and race assets for that level
(`m1`–`m7.p3d`, `mission{1,2,3,5,7}cam.p3d`, `race{1..4}cam.p3d`, `sr{1,2,3}.p3d`, `bm1`, `gr1`, `demo`,
`key`, `litter`, `wasps`, `folder`, `i_folder`, `level.p3d`). This is why the census reports "1,941
parsed, 0 failures": the 28 `P3DZ` files are not parse *failures*, they are a *different container* the
plain walker correctly declines to treat as a chunk tree.

**How the header works (✅ structure verified; codec ⏳ Open).** The `P3DZ` header, read from
`art/missions/level05/bm1.p3d`:

```
50 33 44 5A   9B 11 00 00   2F 04 00 00   00 10 00 00   ...compressed blocks...
"P3DZ"        uncompSize     compSize?      blockSize
              = 0x119B=4507   = 0x042F=1071  = 0x1000=4096
```

- **`uncompSize` (+4)** — the length of the decompressed Pure3D file. **Verified**: it equals `4507`,
  and the decompressed stream begins `50 33 44 FF 0C 00 00 00 9B 11 00 00` — a normal file header whose
  `chunkSize` is exactly `0x119B = 4507`. The compressed wrapper and the plain file agree on the size,
  which is the proof that `P3DZ` decompresses to a standard tree.
- **`compSize` (+8)** — `1071`, consistent with the size of the compressed payload (🟡 reasoned).
- **`blockSize` (+12)** — `4096` (`0x1000`). The data is decompressed in fixed blocks of this size
  (🟡 reasoned; a common Radical scheme).
- **The codec itself is ⏳ Open in this data set.** The payload is *not* standard zlib (no `0x78` stream
  header) — it is a Radical LZ variant. This book does not yet ship a byte-exact decompressor for it, so
  the *algorithm* is marked Open; the *container* (magic, sizes, block size, and that it yields a normal
  `P3D\xff` tree) is Verified.

**Why it's built this way.** Level 05 is Springfield's most asset-heavy mission set; compressing those
`.p3d` files trades a little load-time CPU for disc space and read time — the classic compression trade.
That only *one* level's mission assets are compressed is 🟡 evidence of a late, targeted size
optimisation rather than an engine-wide policy: the loader clearly supports both magics everywhere, but
the build only applied compression where it was needed.

**How a reader must handle it.** The compression test comes **first**, before the plain magic test and
before any walk:

```python
def open_any_pure3d(path):
    buf = open(path, 'rb').read()
    if buf[:4] == b'P3DZ':
        buf = p3dz_decompress(buf)     # ⏳ Radical LZ — not yet byte-exact here
    if buf[:4] != b'P3D\xff':
        raise ValueError('not a Pure3D file')
    _, hs, fs = struct.unpack_from('<III', buf, 0)
    return list(walk_tree(buf, hs, min(fs, len(buf))))     # C1.3
```

The rule is **decompress before you inspect**. A tool that
skips the `P3DZ` test will read the compressed bytes as a chunk stream and desync instantly (C1.7) — the
give-away is a file whose extension is `.p3d` but whose first four bytes are `50 33 44 5A`, not
`50 33 44 FF`.

**What happens if you bend it.**

- *Walk a `P3DZ` file as if plain* → immediate desync at offset 12; the "ids" you read are compressed
  bytes. Test the magic's fourth byte (`FF` vs `5A`) first.
- *Assume all `.p3d` are plain because "0 failures"* → you silently skip the 28 compressed level-05
  assets. The honest census is **1,941 plain + 28 compressed = 1,969**; state both.
- *Re-emit a decompressed file over a `P3DZ` name without recompressing* → the game may still load it
  (the loader accepts plain `P3D\xff` too), but you have changed the file's size profile; prefer to keep
  the container form the build shipped unless you have a verified recompressor.

## What a later pass established (🟡 — codec identified, not yet bit-exact)

A deeper look advanced this considerably:

- **The codec is named.** The compressed stream contains the literal signature **`p3dcompress version
  1.0.0 (with ATG 2.0)`** ("ATG" = Radical's Advanced Technology Group middleware). So P3DZ is Radical's
  *p3dcompress v1* — a specific, named format, not an anonymous blob.
- **The header is fully decoded** (above): magic, uncompSize, a compressed-size field, and a `blockSize` of
  `0x1000` (4096) — the data decompresses in 4 KB blocks.
- **It is an LZSS-family codec with literal runs.** The decompressed P3D header (`P3D\xff`, size 4507) and the
  file's history/version string are stored **literally** near the start of the stream (text and headers don't
  compress well), with back-references compressing the repetitive geometry that follows. This was confirmed by
  observing the decompressed content appear verbatim in the compressed stream.

**Located in the executable (✅).** The decompression path was traced in retail `shar.exe`: the P3DZ magic is
dispatched at **VA `0x5748D9`** (`cmp eax, 0x5a443350; je 0x5748fd`), which reads the header (uncompSize,
compSize, blockSize) and then decompresses. Every *standard* codec was **ruled out** — the payload is not
zlib, raw DEFLATE, LZMA, or bz2 (tested exhaustively from every offset) — so it is genuinely Radical's own
`p3dcompress` LZ. A first-token anchor is established: the 12-byte P3D file header is the first literal run,
commanded by the `00 03` stream prefix.

**Why a standalone decompressor isn't shipped here (the honest boundary).** The decompression is **not a
standalone `decompress(src,dst)` function** — it is implemented as the **`read` method of a decompressing
*stream*** behind an abstract interface (the loader pulls decompressed bytes on demand through
`stream->vtable[+0x2c]`; the direct helper at `0x574740` is only stream-record management). Reconstructing it
bit-exactly therefore requires either **tracing the decompressing-stream's vtable** through several indirect
calls in the exe, or **CPU-emulating** that stream's `read` with its object graph set up — a dedicated
reverse-engineering effort in its own right. Dozens of LZSS bit-flag and byte-command LZ variants were
brute-forced against a full-walk oracle without converging, confirming the token format is non-standard.

**The practical path.** Because the codec is the game's own streaming loader, a P3DZ file *does* load
correctly in the retail game — a tool that needs the level-05 mission trees can let the game (or a hook of its
decompress-stream at `0x5748D9`) do the decompression, rather than reimplementing the codec.

**Status.** Container: ✅ Verified. Codec **identity, header, and location: ✅** (`p3dcompress v1.0.0 (with ATG
2.0)`, dispatched at `0x5748D9`, custom LZ — standard codecs ruled out). Standalone bit-exact reimplementation:
⏳ Open — the single remaining open item in the whole encyclopedia, now fully characterized and bounded (it
needs the decompressing-stream's vtable emulated/traced, not more guessing).
