# C1.4 — The File Header & the `P3D\xff` Magic

**What it is.** The 12 bytes at the very start of a `.p3d` file, before any real chunk. It is shaped
exactly like a chunk header, which is what lets a file be treated as one outermost chunk.

```
offset 0:  50 33 44 FF   0C 00 00 00   21 09 00 00
           id             headerSize    chunkSize
           0xFF443350     0x0000000C=12  (whole file length)
```

**How it works.** The `id` is the magic: bytes `50 33 44 FF`, i.e. ASCII `P`, `3`, `D`, then `0xFF`.
Read as a little-endian `uint32` it is `0xFF443350`. `headerSize = 12` tells you the real chunk stream
starts at offset 12 — the file header carries no data of its own. `chunkSize` is the total file length,
so a correct reader can also use it to detect truncation (`chunkSize == len(file)` should hold).

**Why the `0xFF`.** The trailing `0xFF` is the format's endianness/variant sentinel. On the PC (and
Xbox) little-endian builds the magic reads `50 33 44 FF`; a byte-swapped big-endian build (the GameCube
version) stores the mirrored order. Testing all four magic bytes — not just `"P3D"` — is therefore also
a cheap endianness check. In the retail PC tree this book documents, **every one of the 1,941 files
begins `50 33 44 FF`** (✅ verified), so PC tooling can hard-require little-endian and reject anything
else early.

**Worked confirmation (✅ verified).** `art/atc/atc.p3d`:

```
50 33 44 FF   0C 00 00 00   21 09 00 00   ...
"P3D\xff"     headerSize=12  chunkSize=2337
```

The file on disk is 2,337 bytes; the first real chunk sits at offset 12 and its own `chunkSize` is
`2337 − 12 = 2325`, so the whole file is a single outermost chunk with one child. Start every walk at
offset 12 and this all lines up.

**Why start at 12, always.** Because the file header is itself a valid-looking 12-byte header, a naive
walker that starts at offset 0 will read the magic as a chunk id, see `headerSize = 12 == chunkSize? no`
and generally misbehave. The convention is simpler and universal: **verify the magic, then begin the
chunk walk at offset `headerSize` (which is 12).**

**What happens if you bend it.**

- *Skip the magic test* and you will happily "parse" a Bink `.rmv` or an RCF as if it were Pure3D,
  desyncing on the first step. The four-byte test is one comparison; always do it (the portable
  identifier in [Glossary/extensions.md](../Glossary/extensions.md#a-portable-identifier) does it for
  every format at once).
- *Trust `chunkSize` in the file header as gospel for the buffer length* — always clamp to the actual
  file size (`min(chunkSize, len(buf))`). A tool that truncated the file, or an archive slice that
  over-reads, will otherwise send your walk past the end.
- *Rewrite the file but forget to fix the header `chunkSize`* after adding or removing data and the
  engine may read a stale total. Treat the file header as the ultimate ancestor in the size-tree fixup
  of [C1.5](05-editing-and-repacking.md).
