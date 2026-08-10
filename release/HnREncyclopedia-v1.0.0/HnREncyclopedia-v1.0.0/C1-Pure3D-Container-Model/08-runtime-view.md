# C1.8 — The Runtime View: How `radLoadObject` Walks the Same Tree

**What it is.** The engine's side of everything in this chapter. Your dumper and RadCore's loader read a
`.p3d` with the *same* algorithm; the only difference is what they do at each recognised leaf. Seeing
that equivalence is what makes the format learnable — and it ties the on-disk model (C1.1–C1.7) to the
runtime class model of Part VII.

**How it works.** When the game loads a Pure3D file (typically named through an `.mfk` `LoadP3DFile`
call, Chapter 14), RadCore:

1. **Identifies and opens** the file — the same magic test you use, `50 33 44 FF`.
2. **Walks the chunk stream** from offset 12, comparing `headerSize` against `chunkSize` to decide
   whether to descend — the identical container test from C1.2.
3. **Dispatches each id to a registered handler.** Pure3D keeps a table mapping chunk id → loader
   callback. A `0x00019000` builds a texture object; a `0x00011000` family assembles a mesh; a
   `0x03F0xxxx` family wires a scene-graph node. Ids with no registered handler are **skipped by
   stepping `chunkSize`** — which is precisely why unknown or future chunk ids never crash the engine,
   and why your walker can safely skip what it doesn't decode.
4. **Builds live objects** and hands them to the relevant manager. The resulting objects are instances of
   the RTTI classes documented in Part VII — `tDrawable`, `IEntityDSG`, `CollisionEntityDSG`, and so on.
   The *file chunk* `0x00019000` and the *runtime class* Texture are two views of the same asset: one
   serialised, one live.

**Why it's built this way.** A generic, table-driven loader is what lets one engine ship on PC,
GameCube, PS2, and Xbox with the same asset pipeline: the walker is universal, and only the per-id
handlers and the endianness sentinel (C1.4) differ per platform. It also makes the format *forward- and
backward-compatible* — a tool can add a chunk the engine doesn't know (it is skipped) and the engine can
add a handler for a chunk older tools ignore.

**The bridge to the class model (⏳ where addresses are Open).** The correspondence between a chunk id
and the class it constructs is the seam this book crosses in Part VII. The class set is ✅ verified from
`Simpsons.exe`'s RTTI (1,207 classes; DonutsSDK's `shar_dumps.csv`), so we can name the classes with
confidence — `tDrawable`, `sim::*`, `Character`, `Vehicle`. What is **not** yet tabulated here is the
exact *address* of each chunk handler in the executable, or the precise member offset where a loaded
value lands in its object. Those are marked ⏳ Open and are recovered per-subsystem in the later
chapters; this book never invents a handler address it has not confirmed.

**Practical consequence for modders.** Because the loader is generic and skips unknown ids, two robust
modding strategies fall out directly:

- **Replace, keeping ids and the size tree valid** (C1.5). The loader will build your edited asset with
  the same handler — a retextured car, a retuned mesh — as long as every ancestor size still balances.
- **Add ids the engine ignores** to carry tool-only metadata inside a `.p3d` (provenance, editor state).
  The game steps over them; your tools read them. Keep them well-formed so they don't break the size
  tree.

**What happens if you bend it.** Hand the loader a file whose size tree doesn't balance and it desyncs
exactly as your walker would (C1.7) — but *inside the game*, mid-load, which usually means a hang or a
crash rather than a clean error. The same discipline that keeps your dumper in sync keeps the game
loading: balance the size tree, keep ids in the known set unless you intend a deliberate skip, and test
the file through the real loader before you ship it.

**Next:** [Chapter 2 — Identifiers & Radical Hashing](../C2-Identifiers-And-Hashing/C2-Identifiers-And-Hashing.md).
