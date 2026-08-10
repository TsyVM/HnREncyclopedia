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
