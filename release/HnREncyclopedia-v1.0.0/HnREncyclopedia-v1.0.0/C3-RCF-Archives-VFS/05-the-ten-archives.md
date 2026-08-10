# C3.5 — The Ten Shipped Archives

**What it is.** A tour of the ten root `.rcf` files — what each holds, how big it is, and which chapter
decodes its members. Sizes are ✅ verified by measuring the retail tree.

**The inventory.**

| Archive | Size | Members hold | Decoded in |
|---|---:|---|---|
| `music00.rcf` | 228.5 MB | Streamed music, set 0 | C19 |
| `music01.rcf` | 225.0 MB | Streamed music, set 1 | C19 |
| `music02.rcf` | 228.5 MB | Streamed music, set 2 | C19 |
| `music03.rcf` | 226.5 MB | Streamed music, set 3 | C19 |
| `dialog.rcf` | 173.0 MB | Character dialogue lines | C19 |
| `soundfx.rcf` | 135.3 MB | Sound effects | C18–C19 |
| `ambience.rcf` | 102.5 MB | World ambience beds | C19 |
| `nis.rcf` | 88.4 MB | Non-Interactive Sequence (cutscene) data | C17, C20 |
| `carsound.rcf` | 20.6 MB | Engine/vehicle audio | C19, C24 |
| `scripts.rcf` | 2.7 MB | Compiled scripts (**125** members) | C14–C16 |

**Reading the split.** The shape of this table tells you where the game spent its disc budget: **~1.24 GB
of the 1.43 GB is audio** across seven archives (four music, dialog, soundfx, ambience) — a talking,
music-driven game of a licensed comedy world. `nis.rcf` (88 MB) is the cutscenes. `scripts.rcf`, the
smallest at 2.7 MB, is the brain: 125 compiled script members that drive levels and missions (Chapters
14–16). The visual art, by contrast, is *loose* in `art/` (264 MB of `.p3d`), not archived — which is
exactly why the art is the easiest thing to mod and the audio the hardest (C3.6).

**Why audio is packed and art is loose (🟡 reasoned).** Streamed audio is read sequentially in large
runs during play; packing it into a few big archives keeps it contiguous on disc and minimises seeks — a
real concern on 2003 optical media. Art is loaded per-level in bursts and benefits from the flexibility
of loose files (and, for the shipped game, was simply left unpacked on the PC build). The practical
upshot for modders is the resolution order in C3.6: loose files can shadow packed ones, so even packed
content can often be overridden by dropping a loose file in the right path.

**Working with the big archives.** The music/dialog/soundfx archives are hundreds of MB; do not read them
whole into memory to pull one member. Open the file, read the header and directory (a few KB), then
`seek` to the one member's `offset` and read its `size` bytes. The directory is tiny; only the member you
want needs to be touched.

**What happens if you bend it.**

- *Load a 228 MB archive fully to extract one 300 KB sound* and you waste a quarter-gig of RAM for
  nothing. Seek to the offset the directory gives you.
- *Assume every archive uses the same alignment/preamble as `scripts.rcf`* — read each archive's own
  header (`0x24` pointer) and directory preamble rather than reusing constants from one file.
