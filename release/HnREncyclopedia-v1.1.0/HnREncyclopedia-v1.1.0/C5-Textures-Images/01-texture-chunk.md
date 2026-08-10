# C5.1 — The Texture Chunk (`0x00019000`)

**What it is.** The descriptor for one texture: its name and the nine numbers that say how big it is, how
it's encoded, and how many mip levels it carries. It is a container — its `headerSize < chunkSize` (C1.2)
— holding the Image that follows.

**How it works (✅ verified).** The own-data (bytes `[off+12, off+headerSize)`) is a length-prefixed name
then nine `uint32`. Verified from `flag.bmp`:

| Field | Bytes | Value | Meaning |
|---|---|---|---|
| name | `08` + 8 chars | `flag.bmp` | plaintext, length-prefixed (C4.1 `pstr`) |
| version | `36 B0 00 00` | 14000 | Pure3D format-version stamp |
| width | `40 00 00 00` | 64 | pixels |
| height | `40 00 00 00` | 64 | pixels |
| bpp | `04 00 00 00` | 4 | bits/pixel or format selector |
| alphaDepth | `00 00 00 00` | 0 | alpha bits |
| numMips | `01 00 00 00` | 1 | mip levels present |
| textureType | `01 00 00 00` | 1 | texture class |
| usage | `00 00 00 00` | 0 | usage hint |

The nine-field shape is consistent with the standard Pure3D texture header, and it is confirmed here by a
real read: the dimensions are powers of two (64×64), `numMips` is a small positive count, and the name's
extension (`.bmp`) matches an image type — all the sanity checks of C4.4 pass.

**Why it's built this way.** Separating the *descriptor* (this chunk) from the *pixels* (the Image-Data
leaf two levels down) lets the loader read size and format cheaply — nine words — and decide how much
memory to reserve and which decoder to use before it touches the payload. The plaintext name is the hook
the shader system (C6) uses to bind the texture, which is why it is not hashed like other references.

**What happens if you bend it.**

- *Change `width`/`height` without re-encoding the payload* — the loader reserves the wrong buffer and the
  image tears or the load fails. Dimensions must match the actual pixel data (C5.5).
- *Set `numMips` higher than the mip levels actually present* — the loader reads past the payload for the
  missing mips. Keep the count truthful.
- *Corrupt the `pstr` length byte* — the name read runs into the numeric header and every field after
  shifts. The length byte is load-bearing; preserve it exactly when editing names.
