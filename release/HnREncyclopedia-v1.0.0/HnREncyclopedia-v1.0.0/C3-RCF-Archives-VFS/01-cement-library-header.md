# C3.1 — The Cement Library Header

**What it is.** The fixed 64-byte preamble that opens every `.rcf`. It identifies the archive and points
at the directory; everything else in the file is member data and the directory itself.

**How it works (✅ verified on `scripts.rcf`).**

```
0x00:  52 41 44 43 4F 52 45 20 43 45 4D 45 4E 54 20 4C   "RADCORE CEMENT L"
0x10:  49 42 52 41 52 59 00 00 00 00 00 00 00 00 00 00   "IBRARY" + zero pad
0x20:  01 02 00 01                                       version   = 0x01000201
0x24:  00 08 00 00                                       dirOffset = 0x00000800
0x28:  00 00 00 00
0x2C:  00 08 00 00                                       0x00000800  (data base / second pointer)
0x30..0x3F: 00                                           reserved
```

- **Magic** — the ASCII string `RADCORE CEMENT LIBRARY` (22 bytes), zero-padded to `0x20`. This is the
  cheapest possible identity test and the first branch in the [portable identifier](../Glossary/extensions.md#a-portable-identifier).
  "Cement Library" is Radical's house name for the format — RadCore's answer to a WAD or PAK.
- **Version** at `0x20` — `0x01000201`. Treat it as an opaque version/flags word: check it equals the
  value your parser was written against and refuse anything else rather than guessing at a variant.
- **Directory offset** at `0x24` — `0x800`. The one field you must read; it is where the member index
  lives (C3.2). It is page-aligned (`0x800` = 2048), as is the member data region (`0x1000`).
- **The second `0x800`** at `0x2C` — a second pointer that, together with the directory's `dataStart`
  field (C3.2), delimits the data region; the region base and the directory happen to coincide here. Its
  precise role is 🟡 reasoned; you do not need it to extract files, only the `0x24` pointer.

**Why it's built this way.** A fat, obvious ASCII magic plus a single directory pointer is the classic
shippable-archive header: trivially identifiable, version-gated, and self-locating. Page-aligning both
the directory (`0x800`) and the data (`0x1000`) lets the engine DMA or memory-map regions on aligned
boundaries — cheap on 2003 console hardware and harmless on PC.

**What happens if you bend it.**

- *Skip the version check* and a future or console variant with a different directory shape will be
  parsed with your PC assumptions and produce garbage offsets. Gate on `0x01000201`.
- *Hard-code the directory at `0x800`* instead of reading `0x24`. It is `0x800` in `scripts.rcf`, but the
  correct, portable thing is to follow the pointer — other archives may align differently.
- *Assume the reserved bytes are always zero* and you may trip over a variant that uses them. Read the
  two fields you need (version, dirOffset); ignore, don't assert, the rest.
