# File Catalogue — the entire retail data set

A file-by-file inventory of *The Simpsons: Hit & Run* (PC retail), counted and sized by
`tools/p3d_rcf_scan.py`. Everything here is ✅ verified against the shipped tree.

## The ten RadCore archives (root)

The bulk of the game — all audio, all FMV audio streams, the compiled scripts — ships inside ten
`RADCORE CEMENT LIBRARY` archives at the game root (1.43 GB total). See
[C3](../C3-RCF-Archives-VFS/C3-RCF-Archives-VFS.md) for the container format.

| Archive | Size | Holds |
|---|---:|---|
| `music00.rcf` | 228.5 MB | Streamed music set 0 |
| `music01.rcf` | 225.0 MB | Streamed music set 1 |
| `music02.rcf` | 228.5 MB | Streamed music set 2 |
| `music03.rcf` | 226.5 MB | Streamed music set 3 |
| `dialog.rcf` | 173.0 MB | Character dialogue lines |
| `soundfx.rcf` | 135.3 MB | Sound effects |
| `ambience.rcf` | 102.5 MB | World ambience beds |
| `nis.rcf` | 88.4 MB | Non-interactive-sequence (cutscene) data |
| `carsound.rcf` | 20.6 MB | Engine/vehicle audio |
| `scripts.rcf` | 2.7 MB | Compiled script set (**125** directory entries, verified) |

## The loose trees

| Tree | Files | Notes |
|---|---:|---|
| `art/` | 3,125 | 1,969 `.p3d` (264 MB) + 930 `.png` sources + Scrooby UI (`frontend/`) + `chars/` `.cho` |
| `scripts/` | 599 | 344 `.mfk` + 255 `.con`; top-level `ss.mfk`/`ssi.mfk`, `cars/`, `missions/level01…07` |
| `movies/` | 16 | Bink `.rmv` FMVs (244.6 MB): `foxlogo`, `fmv1A`–`fmv8`, `credits`, … |
| `sound/` | 3 | Loose `RSD4PCM` samples (`accept.rsd`, `scroll.rsd`) + `typ` |
| `DLLs/` `mods/` | 13 | Loader/mod support (`Hacks.dll`, `d3d9.dll`, …) — tooling, not retail assets |

## Pure3D census (the `art/` tree)

Walking all `.p3d` files yields **1,941 plain files parsed with 0 failures** (plus **28 compressed
`P3DZ` files** in `art/missions/level05/`, decompressed first — [C1.9](../C1-Pure3D-Container-Model/09-compressed-p3dz.md);
1,941 + 28 = 1,969), containing **179 distinct chunk IDs** across **~2.1 million chunk instances**. The heaviest families by instance count are
geometry (`0x00011003` normals/UV — 224,971 instances), collision (`0x00121110` vector list —
147,655), and the scenegraph (`0x03F0xxxx`). The complete table is
[chunk-ids.md](chunk-ids.md).

### Notable `art/` groupings

- `art/L{1,4,7}_TERRA.p3d`, `art/b**.p3d` — level terrain and world blocks (C12).
- `art/cars/*.p3d` — vehicle models, paired with `scripts/cars/*.con` handling (C15, C24).
- `art/chars/*.p3d` + `art/chars/*.cho` — characters and their choreography (C17).
- `art/missions/level01…/*.p3d` — per-mission props (C16).
- `art/frontend/scrooby2/**` — the Scrooby menu/HUD system (`.pag` XML, C21).
