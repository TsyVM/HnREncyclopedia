# Terminology

Every term used across the chapters, defined once. Confidence markers (✅/🟡/⏳) are defined in the
[top-level README](../README.md#confidence-markers).

### Pure3D
Radical Entertainment's proprietary cross-platform 3D engine and its on-disk asset format. A Pure3D
file (`.p3d`) is a **chunk tree**: a recursive sequence of self-describing blocks. Magic `50 33 44 FF`
(`"P3D\xff"`). ✅ (magic verified on all 1,941 files).

### P3DZ (compressed Pure3D)
A block-compressed Pure3D file. Magic `P3DZ` (`50 33 44 5A`); a header of `{uncompSize, compSize,
blockSize}` then a Radical-LZ compressed payload that decompresses to a normal `P3D\xff` chunk tree.
28 files in the retail tree — all in `art/missions/level05/` — use it. Must be decompressed before
walking. Container ✅ verified; decompression algorithm ⏳ Open. See
[C1.9](../C1-Pure3D-Container-Model/09-compressed-p3dz.md).

### RadCore
The runtime services layer beneath Pure3D — memory, streaming, object loading (`radLoadObject`),
sound (`radSound`), file I/O. The class names in the RTTI set (`rad*`, `IRefCount`, `tRefCounted`)
belong to RadCore. ✅ (present in `shar_dumps.csv`).

### Chunk
The universal Pure3D unit: a 12-byte header `{ uint32 id; uint32 headerSize; uint32 chunkSize; }`
followed by data and, optionally, child chunks. See [C1](../C1-Pure3D-Container-Model/C1-Pure3D-Container-Model.md). ✅

### Container / Leaf
A chunk whose `headerSize < chunkSize` carries **child chunks** in the range
`[off+headerSize, off+chunkSize)` — it is a **container**. When `headerSize == chunkSize` it is a
**leaf** (raw data only). The container/leaf distinction is **structural** (a size
comparison), not a flag bit. ✅

### id / headerSize / chunkSize
The three `uint32` of a chunk header. `id` is the type. `headerSize` is the length of this chunk's own
header-plus-data (where children begin). `chunkSize` is the total length of the chunk **including** all
children. To step to the next sibling, advance `chunkSize` bytes. ✅

### RCF — RadCore Cement Library
Radical's resource archive. Magic string `RADCORE CEMENT LIBRARY`. A header, then a directory of
`{ hash, offset, size }` records — files are addressed by **Radical hash of their path**, not by stored
name. See [C3](../C3-RCF-Archives-VFS/C3-RCF-Archives-VFS.md). ✅ (directory verified in `scripts.rcf`).

### Radical hash
The 32-bit string hash Radical uses for asset names and RCF directory keys (the key that `radLoadObject`
looks up). The DonutsSDK `hashing` module reproduces it as `constexpr`. 🟡 (algorithm from SDK; RCF keys
verified numerically).

### CON
A plain-text vehicle/config script (`scripts/cars/*.con`). A sequence of `SetX(value);` calls that set
handling parameters (`SetMass`, `SetTopSpeedKmh`, `SetTireGrip`, …). See
[C15](../README.md#chapters). ✅ (parsed).

### MFK
A plain-text level/mission script (`scripts/**/*.mfk`). Built from asset-loading and world-setup calls
(`LoadP3DFile`, `LoadDisposableCar`, …). See [C14](../README.md#chapters). ✅ (parsed).

### CHO — Choreography
A text character/NPC scripting file (`art/chars/*.cho`). See [C17](../README.md#chapters). ✅ (text
verified).

### RSD
A Radical sound sample container. Magic `RSD4`; observed variant `RSD4PCM` with a 24,000 Hz sample rate
in the loose `sound/` files. See [C18](../README.md#chapters). ✅ (header parsed).

### RMV / Bink
The full-motion-video container (`movies/*.rmv`). Magic `BIK` — it is a **Bink** stream (RAD Game Tools),
decoded through `binkw32.dll`. See [C20](../README.md#chapters). ✅ (magic verified).

### Scrooby
Radical's front-end/UI system. Pages ship as `.pag` **XML** documents (`art/frontend/scrooby2/...`),
with `.scr` and `.prj` companions. See [C21](../README.md#chapters). ✅ (XML verified).

### DSG
"Drawable Scene Graph" — the runtime scene-graph entity family (`IEntityDSG`, `CollisionEntityDSG`,
`AnimCollisionEntityDSG`, `DynaPhysDSG`, `InstStatEntityDSG`). ✅ (in `shar_dumps.csv`).

### Locator
A named, positioned marker embedded in Pure3D data (`0x00015800/1`, `0x07010001/4/7`) that gameplay,
cameras, and scripts attach to (spawn points, trigger anchors, camera nodes). 🟡 (name public; IDs and
counts verified).

### Scenegraph chunks (`0x03F0xxxx`)
The Pure3D scene-graph family: root, branch, transform, drawable, and sort-order chunks that arrange
drawables in a hierarchy. 🟡 names / ✅ IDs & counts.

### RTTI
Run-Time Type Information: the compiler-emitted class metadata (`_RTTIBaseClassDescriptor`, type
descriptors) left in `Simpsons.exe`. The source of the verified class/inheritance data set. ✅

### vtable
A class's virtual-method table. Identifying an object by its vtable pointer is how the DonutsSDK runtime
recognises a live class instance. ✅ (mechanism), ⏳ (per-class vtable addresses not yet tabulated).

### DonutsSDK
The companion C++20 modding SDK (`../DonutsSDK`): an offline data library (P3D/CON/RSD/RCF parsers) plus
a header-only runtime layer generated from the RTTI class set. This encyclopedia and the SDK share the
same verified data.
