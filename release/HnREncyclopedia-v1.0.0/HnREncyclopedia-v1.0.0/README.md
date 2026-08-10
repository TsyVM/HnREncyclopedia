<p align="center">
  <img src="hnrencyclopedia-logo.png" alt="The Simpsons: Hit &amp; Run Encyclopedia" width="480">
</p>

<h1 align="center">The Simpsons: Hit &amp; Run Encyclopedia</h1>

<p align="center"><i>A complete engine-level reference for The Simpsons: Hit &amp; Run (2003, PC — retail)</i></p>

<p align="center">
  <img src="https://img.shields.io/badge/chapters-36-brightgreen" alt="36 chapters">
  <img src="https://img.shields.io/badge/pages-250%2B-brightgreen" alt="250+ pages">
  <img src="https://img.shields.io/badge/verified-byte--level%20%2B%20RTTI-blue" alt="verified">
  <img src="https://img.shields.io/badge/Legend-master%20index-blue" alt="Legend">
</p>

---

This is a self-contained, byte-level and runtime-level guide to the file formats, data structures,
classes, and subsystems of *The Simpsons: Hit & Run* — the open-world driving-and-platforming game
built by **Radical Entertainment** on their **Pure3D** engine and **RadCore** runtime. It is the
a self-contained, byte-level and runtime-level reference, and it follows one discipline throughout: understand the
game the way its authors did, and change it with confidence — from swapping a single texture, to
rebuilding a car's handling, to retuning a mission, to tracing a value from the HUD down to the byte
it was read from on disk.

Everything here is grounded in the **retail PC data set** shipped with the game and in the code of
the retail executable (`Simpsons.exe`). Wherever a claim describes bytes on disk, it was produced by
actually parsing the shipped files with the tools in [`tools/`](tools/); wherever a claim describes
the running game — a class, a base-class relationship, a vtable — it comes from the **RTTI-verified
data set** extracted directly from `Simpsons.exe` and carried by the companion **DonutsSDK**
(`../DonutsSDK`). Nothing on-disk is asserted that the parser cannot reproduce, and nothing about the
class model is asserted that the executable's own RTTI does not contain.

It is written **format-first and mechanism-first**: byte layouts, the algorithms that read and write
them, the runtime classes that consume them, worked examples in portable C/Python, and — always —
the *reasoning* behind why each thing is built the way it is. Code is deliberately
**toolkit-agnostic**: it reads and writes raw bytes, so the knowledge outlives any single program.

---

## How to read this book

The work is split into a **Glossary** (terminology, the master chunk-ID table, an extension index,
and a file-by-file catalogue of the entire game) followed by **chapters** that build from first
principles — a single Pure3D chunk header — all the way up to the running game.

> **Every chapter is a hub plus focused deep-dive pages.** The chapter file (e.g.
> `C1-Pure3D-Container-Model/C1-Pure3D-Container-Model.md`) is the overview and the map; inside the
> same folder, numbered pages (`01-….md`, `02-….md`, …) each take a *single* mechanism and answer
> four questions about it: **what it is, how it works, why it's built that way, and what happens if
> you bend it — the right way or the wrong way.** A chapter runs 5–12 such pages. The hub links to
> its deep-dive pages near the top.

### Confidence markers

Because much of this is reverse-engineered, every non-obvious claim is tagged so you always know how
much weight it bears:

- ✅ **Verified** — reproduced directly from retail bytes (by the parser in `tools/`) or read from
  the executable's own RTTI (via the DonutsSDK data set). Reproducible on your own copy.
- 🟡 **Reasoned** — a well-supported inference about *intent*, *mechanism*, or a *name* that fits all
  observed evidence (often aligned with public Pure3D documentation) but is not a byte-for-byte proof
  in this data set.
- ⏳ **Open** — known to exist, not yet fully decoded; the boundary of current knowledge is stated
  explicitly rather than hidden.

A claim with no marker is either self-evidently structural (a stated struct offset you can see in a
hex editor) or established earlier in the same chapter.

### What "verified" rests on, concretely

Two independent, reproducible evidence bases sit under this book:

1. **The shipped files.** `tools/p3d_rcf_scan.py` walks every `.p3d` and `.rcf` in the retail tree.
   Its census — **1,941 plain Pure3D files (0 parse failures) plus 28 compressed `P3DZ` files, 179
   distinct chunk IDs** — is the source of the master chunk table and of every on-disk structural claim.
2. **The executable's RTTI.** DonutsSDK ships `data/shar_dumps.csv`: **1,207 RTTI-confirmed classes
   and 3,924 base-class relationships** read straight out of `Simpsons.exe`'s
   `_RTTIBaseClassDescriptor` records. Every runtime-class claim traces to a row there.

Member offsets, function addresses, and singleton pointers that neither base has proven are marked
⏳ **Open** and never invented.

---

## Glossary

| Page | Contents |
|---|---|
| [Glossary/README.md](Glossary/README.md) | How the glossary is organised; the "identify an unknown file" workflow |
| [Glossary/terminology.md](Glossary/terminology.md) | Every acronym and concept: Pure3D, chunk, container/leaf, RadCore, RCF, Radical hash, CON/MFK, RSD, Bink, Scrooby, choreography, vtable, RTTI, DSG… |
| [Glossary/chunk-ids.md](Glossary/chunk-ids.md) | Master table of all **179** chunk identifiers observed in the retail data set, each with role (container/leaf) and occurrence count |
| [Glossary/extensions.md](Glossary/extensions.md) | Extension → format → chapter map, plus the "identify an unknown file" decision tree and a portable identifier |
| [Glossary/file-catalogue.md](Glossary/file-catalogue.md) | A file-by-file inventory of the entire retail data set: the ten `.rcf` archives and the loose `art/`, `scripts/`, `sound/`, `movies/` trees |

---

## Chapters

### Part I — Foundations & the container model

Everything downstream depends on Part I. Read C1–C4 in order; the rest of the book assumes them.

1. [C1 — The Pure3D Container Model](C1-Pure3D-Container-Model/C1-Pure3D-Container-Model.md): the chunk tree, the 12-byte header, the header-size/chunk-size distinction that decides container vs. leaf, walking, dumping, editing, and repacking *any* Pure3D file.
2. [C2 — Identifiers & Radical Hashing](C2-Identifiers-And-Hashing/C2-Identifiers-And-Hashing.md): how names become 32-bit numbers, the Radical string hash used by `radLoadObject` and the RCF directory, chunk-ID families, and name recovery.
3. [C3 — RCF Archives & the Virtual File System](C3-RCF-Archives-VFS/C3-RCF-Archives-VFS.md): the `RADCORE CEMENT LIBRARY` container, its hash-addressed directory, and how the ten shipped archives back the loose file tree.
4. [C4 — Byte-Level Toolcraft](C4-Byte-Level-Toolcraft/C4-Byte-Level-Toolcraft.md): bounded readers/writers, tree dumpers, hex-diffing, and the reverse-engineering workflow used to produce this book.

### Part II — Textures, shaders & geometry

5. **C5 — Textures & Images** (`0x00019000/1/2`): the Texture→Image→Image-Data hierarchy and embedded PNG/BMP payloads.
6. **C6 — Shaders & Materials** (`0x00010000` + typed params): how a drawable binds textures and render state.
7. **C7 — Meshes & Primitive Groups** (`0x00011000` family): vertex streams, normals/UVs, colours, and index buffers.
8. **C8 — Skeletons, Skinning & Locators**: joints, skin weights, and the locator groups that pin gameplay to geometry.
9. **C9 — Geometry Import/Export**: exporting to OBJ/glTF and rebuilding vertex/index buffers.

### Part III — The world & scene

10. **C10 — The Scenegraph** (`0x03F0xxxx`): roots, branches, transforms, drawables, and sort order.
11. **C11 — Collision & Intersect** (`0x00120xxx`/`0x00121xxx`): the collision-volume tree and the Intersect DSG.
12. **C12 — Level Composition**: terrain (`L*_TERRA.p3d`), world blocks (`b**.p3d`), and static entities.
13. **C13 — Paths, Fences & Road Data** (`0x03000xxx`): the navigation and barrier geometry cars and NPCs use.

### Part IV — Scripting, missions & characters

14. **C14 — MFK Level & Mission Scripts**: the `LoadP3DFile`/`LoadDisposableCar` vocabulary that assembles a level.
15. **C15 — CON Vehicle & Config Scripts**: the `Set*` handling vocabulary (`scripts/cars/*.con`).
16. **C16 — Mission Structure & Objectives**: how the seven levels' missions are wired.
17. **C17 — Choreography & Characters** (`.cho`, `.p3d` chars): NPC scripting and character rigs.

### Part V — Audio & video

18. **C18 — RSD Sound Format**: the `RSD4PCM`/ADPCM sample container.
19. **C19 — The Audio Archives**: `carsound`, `soundfx`, `ambience`, `dialog`, and the four `music0*` RCFs.
20. **C20 — Bink Video** (`.rmv`, `BIKi`): the FMV container and playback.

### Part VI — Front-end, UI & text

21. **C21 — Scrooby UI** (`.pag` XML, `.scr`, `.prj`): the menu/HUD layout system.
22. **C22 — Fonts, Glyphs & Localization**: text rendering and string tables.
29. [**C29 — Maps & the HUD Minimap**](C29-Maps-Minimap/C29-Maps-Minimap.md): the seven per-level HUD maps (`l1hudmap`–`l7hudmap.p3d`), the full-screen map, and mission/objective icons.

### Part VII — The runtime class system

The book pivots here from *files on disk* to the *running game*, using the RTTI-verified class set.

23. **C23 — The RTTI Class Model**: roles, namespaces, and how the 1,207-class set is organised.
24. **C24 — Vehicles at Runtime** (`Vehicle`, `VehicleCentral`): from `.con` values to live handling.
25. **C25 — Characters & AI** (`Character`, `CharacterAi`, `choreo::*`).
26. **C26 — Missions, Cameras & Physics at Runtime** (`Mission*`, `SuperCam*`, `sim::*`).

### Part VIII — Save data, config & modding

27. [**C27 — Save Data & `simpsons.ini`**](C27-Save-Config/C27-Save-Config.md): the career-save container (mission/reward records), `MemoryCardManager`, and the retail config file.
28. [**C28 — The Modding Toolchain**](C28-Modding-Toolchain/C28-Modding-Toolchain.md): Lucas' Mod Launcher, the Lua layer, and where **DonutsSDK** fits for native C++ mods.

### Part IX — Systems, backend & gameplay

Systems you see and feel in play, and the "backend" machinery you don't — all grounded in the RTTI-verified
class set (with confirmed vtable addresses).

30. [**C30 — GameFlow & the Load Sequence**](C30-GameFlow-LoadSequence/C30-GameFlow-LoadSequence.md): "what happens between loading screens" — the `GameFlow` context state machine (`BootupContext`→`FrontEndContext`→`LoadingContext`→`GameplayContext`), `LoadingManager`, streaming, and the frame.
31. [**C31 — Police, Hit & Run & Wasps**](C31-Police-HitAndRun/C31-Police-HitAndRun.md): the Hit & Run meter (`HitnRunManager`), the police chase (`ChaseManager`/`ChaseAI`), and the wasp cameras.
32. [**C32 — Combat, Health, Collectibles & Inventory**](C32-Combat-Health-Inventory/C32-Combat-Health-Inventory.md): the kick (`KickAction`) & attack behaviours, hit points & damage, coins/cards/items, and `tInventory`.
33. [**C33 — Rendering, Lighting, Sky & Effects**](C33-Rendering-Lighting-Effects/C33-Rendering-Lighting-Effects.md): the render pipeline, the `tLight` family, the sky (which is *art*, not code), particles, sprites & billboards.
34. [**C34 — Animation Channels & Controllers**](C34-Animation-Channels/C34-Animation-Channels.md): the keyframe-channel substrate (14 typed channels incl. compressed quaternions) under all animation.
35. [**C35 — Vehicle Physics, Drifting & Destruction**](C35-Vehicle-Physics/C35-Vehicle-Physics.md): the engine state machine (`Skid`=drift, `InAir`=jump, gears), skidmarks, suspension, `sim::` rigid body, and breakable objects (glass).
36. [**C36 — Cameras & Camera Effects**](C36-Cameras-Effects/C36-Cameras-Effects.md): the full 41-camera roster, `SuperCamCentral` switching, camera **shake** (`SineCosShaker`), and event-driven reactions (jump/crash/glass).

> **The Legend** — a companion to the chapters — is the exhaustive **categorized master index** of the whole
> game: [Legend/README.md](Legend/README.md). Every [function](Legend/functions.md) (212 script commands),
> [vehicle](Legend/vehicles.md) (90), [character](Legend/characters.md) (132),
> [costume](Legend/costumes.md), [texture name](Legend/textures.md) (751),
> [object](Legend/objects.md), [mission](Legend/missions.md), [level & map](Legend/levels-maps.md), and
> [class](Legend/classes.md) — listed and grouped, all ✅ verified by extraction.

> **Status:** this edition is **complete** — **all 36 chapters** (C1–C36) are written to full depth (a hub
> plus 5–9 deep-dive pages each), plus the 10-file **Legend** master index — ~252 files and ~15,000 lines,
> every internal link resolving. No scaffolds remain.
>
> **Open items — mostly closed.** Of the three long-standing ⏳ items: **member offsets are now recovered**
> — 1,917 verified offsets across 694 of the 1,207 classes (`DonutsSDK/data/member_offsets.csv`, C23.1); the
> **NIS "format" is resolved** — it is not a bespoke format but a composition of decoded ones (RSD audio +
> Pure3D + choreo + scripts, C17.4). The one genuinely-open item is the **P3DZ codec** — now *identified* as
> Radical's `p3dcompress v1.0.0 (with ATG 2.0)` and characterized as LZSS-family, but not yet bit-exact
> (C1.9). **Sky/atmosphere has no code system** — verified to be art (C33.3).

### Levels, missions & maps — where they live

The game's content structure gets first-class, dedicated coverage:

- **Levels** — [C12 (Level Composition)](C12-Level-Composition/C12-Level-Composition.md): terrain, world
  blocks, and how a level's assets are assembled. The retail data holds mission trees for
  `level01`–`level09` plus an `h2h` (head-to-head/multiplayer) tree (✅ verified in `scripts/missions/`).
- **Missions** — [C16 (Mission Structure & Objectives)](C16-Missions-Objectives/C16-Missions-Objectives.md):
  the `m{N}i`/`m{N}l`/`m{N}sd` script split, objectives, and rewards. Note that **all 28 compressed
  `P3DZ` files are `level05`'s mission/camera/race assets** ([C1.9](C1-Pure3D-Container-Model/09-compressed-p3dz.md))
  — a concrete verified reason the mission pipeline needs its own chapter.
- **Maps** — [C29 (Maps & the HUD Minimap)](C29-Maps-Minimap/C29-Maps-Minimap.md): the seven per-level
  HUD maps, the full-screen map, and mission icons.
- **Paths / road network** — [C13 (Paths, Fences & Road Data)](C13-Paths-Fences/C13-Paths-Fences.md): the
  navigation graph cars and NPCs drive on.

---

## A note on provenance

Findings that describe files on disk are properties of the **retail data set** and are reproducible
with `tools/p3d_rcf_scan.py` on your own copy. Findings that describe the running game are properties
of **`Simpsons.exe`** as established by its own compiler-emitted RTTI, carried by DonutsSDK. Where a
layout is only partially recovered, that is said plainly. The emphasis throughout is on the *fact* and
its *confidence*, not on any particular tool.
