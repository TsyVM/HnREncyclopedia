# Extension → Format → Chapter Index

Every file extension present in the retail data set, what it is, and where it is documented. Counts and
total sizes are ✅ verified by `tools/p3d_rcf_scan.py` over the retail tree.

| Ext | Count | Total | Format | Container? | Chapter |
|---|---:|---:|---|---|---|
| `.p3d` (plain) | 1,941 | 264.0 MB | Pure3D chunk tree | magic `P3D\xff` | [C1](../C1-Pure3D-Container-Model/C1-Pure3D-Container-Model.md) |
| `.p3d` (`P3DZ`) | 28 | (subset) | **Compressed** Pure3D (block-compressed) | magic `P3DZ` | [C1.9](../C1-Pure3D-Container-Model/09-compressed-p3dz.md) |
| `.rcf` | 10 | 1,430.9 MB | RadCore Cement Library archive | `RADCORE CEMENT LIBRARY` | [C3](../C3-RCF-Archives-VFS/C3-RCF-Archives-VFS.md) |
| `.rmv` | 16 | 244.6 MB | Bink video | magic `BIK` | C20 |
| `.png` | 930 | 28.5 MB | PNG image (loose art source) | magic `\x89PNG` | C5 |
| `.mfk` | 344 | 0.9 MB | Level/mission script (text) | — | C14 |
| `.con` | 255 | 0.2 MB | Vehicle/config script (text) | — | C15 |
| `.pag` | 119 | 1.8 MB | Scrooby UI page (XML) | `<?xml` | C21 |
| `.scr` | 68 | — | Scrooby script/screen | text | C21 |
| `.prj` | 13 | — | Scrooby project | text | C21 |
| `.cho` | 9 | 0.1 MB | Choreography (text) | — | C17 |
| `.err` | 11 | — | Build/validation error log | text | C4 |
| `.rsd` | 2 | — | RSD sound sample | `RSD4` | C18 |
| `.ini` | 2 | — | Config (`simpsons.ini`, `imgui.ini`) | text | C27 |
| `.txt` `.rtf` | 3 | 0.5 MB | Readme / notes | text | — |
| `.dll` `.asi` `.exe` | 15 | 21.8 MB | Executable & libraries (`Simpsons.exe`, `binkw32.dll`, …) | PE | C23, C28 |

> The single-letter extensions (`.e .f .g .i .s .x`) and `.typ` are fragments/artefacts in the
> extracted tree, not shipped asset types. `.zip`, `.json`, `.pem`, `.log`, `.started` belong to
> extraction/mod tooling, not the retail game.

## A portable identifier

Toolkit-agnostic: read the first 32 bytes and branch. Reproduces the workflow in
[Glossary/README.md](README.md#the-identification-workflow).

```python
def identify(path):
    with open(path, 'rb') as f:
        head = f.read(32)
    if head[:22] == b'RADCORE CEMENT LIBRARY': return 'rcf'      # C3
    if head[:4]  == b'P3DZ':                   return 'pure3d_z' # C1.9 (compressed)
    if head[:4]  == b'P3D\xff':                return 'pure3d'   # C1
    if head[:3]  == b'BIK':                    return 'bink'     # C20  (.rmv)
    if head[:4]  == b'RSD4':                   return 'rsd'      # C18
    if head[:8]  == b'\x89PNG\r\n\x1a\n':      return 'png'      # C5
    if head.lstrip()[:5] == b'<?xml':          return 'scrooby'  # C21 (.pag)
    if head[:2] in (b'//', b'Se', b'Lo'):      return 'script'   # C14/C15/C17 (text)
    return 'unknown'
```

Every branch here is backed by a magic verified against the shipped files; the `script` branch is a
heuristic on the common leading tokens (`//` comment, `Set…`, `Load…`) and should be confirmed by a
full text read.

---

## What each format *is* — plain answers

Quick, self-contained answers to "what is a …?" for every shipped format. Deep detail is in the
linked chapter.

- **`.p3d` — Pure3D file.** The engine's universal asset container: a tree of typed **chunks**
  (`{id, header_size, total_size}`) holding *everything visual and spatial* — textures, meshes,
  shaders, skeletons, animations, collision, scenegraph, locators, world blocks. If you see a
  model, a texture, a car, a world, or a light in the game, it came out of a `.p3d`. Magic
  `P3D\xff`; compressed variant `P3DZ`. → [C1](../C1-Pure3D-Container-Model/C1-Pure3D-Container-Model.md)
- **`.rcf` — RadCore Cement Library.** An **archive** (like a zip): a hash-addressed directory of
  many files packed into one, backing the loose file tree. The ten shipped `.rcf`s hold the audio
  and packed assets. → [C3](../C3-RCF-Archives-VFS/C3-RCF-Archives-VFS.md)
- **`.mfk` — Mission/Level "Franchise" script.** A **text script** that builds a level and its
  missions: what to load, which peds/characters/vehicles/traffic to spawn, gags, objectives,
  rewards. `level.mfk` = the level's content; `leveli.mfk` = the level's **init** (persistent
  setup); `m{N}i/l.mfk` = per-mission init/logic. This is the primary *gameplay* authoring
  surface. → [C14](../C14-MFK-Scripts/C14-MFK-Scripts.md)
- **`.con` — Configuration script.** A **text script** of `Set*` commands that tune a **vehicle's**
  handling (top speed, grip, mass, gears, shadow, …) and other config. One per car under
  `scripts/cars/`. → [C15](../C15-CON-Scripts/C15-CON-Scripts.md)
- **`.pag` — Scrooby UI page.** An **XML layout** for a menu/HUD screen: elements, positions,
  text anchors, sprites. The *visual* side of the UI. → [C21](../C21-Scrooby-UI/C21-Scrooby-UI.md)
- **`.scr` / `.prj` — Scrooby screen/project.** The screen script and the project that groups
  pages — the rest of the Scrooby UI toolchain. → [C21](../C21-Scrooby-UI/C21-Scrooby-UI.md)
- **`.rmv` — Bink video.** A licensed **FMV** container (RAD Game Tools' Bink; magic `BIK`) for
  the cutscene movies, played via `binkw32.dll`. → [C20](../C20-Bink-Video/C20-Bink-Video.md)
- **`.rsd` — Radical Sound Data.** A **sound sample** container (`RSD4PCM` — mono/16-bit PCM) for
  the game's audio. Most samples live inside the sound `.rcf`s. → [C18](../C18-RSD-Sound/C18-RSD-Sound.md)
- **`.cho` — Choreography.** A **text script** driving NPC/character choreography and scripted
  animation sequences. → [C17](../C17-Choreography-Characters/C17-Choreography-Characters.md)
- **`.png` — Texture source.** Standard PNG images — the loose art (many textures are also
  embedded inside `.p3d`). → [C5](../C5-Textures-Images/C5-Textures-Images.md)
- **`.ini` — Config.** Plain `key=value` settings (`simpsons.ini` = display/audio/controls). →
  [C27](../C27-Save-Config/C27-Save-Config.md)
- **`Save1` (no ext) — Career save.** The binary progress file (missions, unlocks, coins). →
  [C27](../C27-Save-Config/C27-Save-Config.md)
- **`.exe` / `.dll` — Executables.** `Simpsons.exe` (the game, the source of the RTTI class model)
  and its runtime libraries (`binkw32.dll` video, `eax.dll` audio, …). → [C23](../C23-RTTI-Class-Model/C23-RTTI-Class-Model.md), [C28](../C28-Modding-Toolchain/C28-Modding-Toolchain.md)

> *(Not shipped game formats: `.log`/`.err` are logs; `.asi` is a mod plugin (a renamed DLL);
> `.zip`/`.json`/`.pem`/`.csv`/`.py` belong to tooling; single-letter extensions are extraction
> fragments. These are excluded from the format reference.)*
