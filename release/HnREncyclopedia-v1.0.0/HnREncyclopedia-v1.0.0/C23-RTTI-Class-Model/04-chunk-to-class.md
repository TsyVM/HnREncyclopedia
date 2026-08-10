# C23.4 — From Chunk to Class

**What it is.** The seam this whole book crosses: how a chunk of data on disk (Parts I–VI) becomes a live
C++ object (Part VII). The bridge is a **chunk-handler registry**, and — usefully — the handlers themselves
are in the verified RTTI set.

**How it works (✅ mechanism; ⏳ addresses).** The Pure3D loader (C1.8) walks a file's chunks and, for each
recognised id, calls a registered **handler** that constructs the class the chunk describes. The RTTI set
confirms the handler family by name:

```
tChunkHandler                    — base chunk handler
  tSimpleChunkHandler
radLoadDataLoader                — RadCore data loader
sim::CollisionObjectLoader : tSimpleChunkHandler, tChunkHandler, radLoadDataLoader   (C11)
CameraDataLoader           : tChunkHandler, radLoadDataLoader                          (C26)
tCompositeDrawableLoader   : tSimpleChunkHandler, tChunkHandler, radLoadDataLoader     (C7)
```

So the correspondences the book has stated all along are real, named handlers:

- Texture chunk `0x00019000` (C5) → a texture object, via a texture loader.
- Mesh `0x00010000` (C7) → a `tDrawable`/composite drawable, via `tCompositeDrawableLoader`.
- Collision `0x00121000` (C11) → a `sim::CollisionObject`, via `sim::CollisionObjectLoader`.
- Camera chunk (C26) → a `SuperCam`, via `CameraDataLoader`.
- Scene-graph chunk `0x03F0xxxx` (C10) → `Scenegraph::Node`/`Drawable` entities.

The **mechanism** (a registry of handlers, one per chunk family) is verified — the handler classes exist in
RTTI with these names and inheritance. The **addresses** of the handler functions, and the exact fields they
write, are ⏳.

**Why a registry.** A table of `chunk id → handler` is what lets the loader be generic (C1.8): it walks any
file, dispatches known ids, and skips unknown ones. It also makes the format extensible — add a handler and
the engine can load a new chunk; older tools skip it. For reverse engineering, the registry is the Rosetta
stone: it pairs each on-disk format (Parts I–VI) with the runtime class it becomes (Part VII), so decoding a
chunk and identifying its class are two ends of one bridge.

**Following the bridge both ways.** *Disk → runtime*: decode a chunk (its chapter), then find the handler
class that consumes it (its name in RTTI). *Runtime → disk*: identify a live object by vtable (C23.5), find
its class, then find the chunk family that builds it. This two-way mapping is how you connect a value you see
on screen to the byte it came from — the recurring goal since C4.3.

**What happens if you bend it.**

- *Assume a chunk maps to exactly one class* — some build composite objects (a mesh becomes a
  `tCompositeDrawable` of several elements). Follow the handler, not a 1:1 guess.
- *Rely on a handler's address* — it's ⏳; the handler *class* is named, but its function address needs a
  disassembly. Don't hardcode it.
- *Add a chunk without a handler expecting it to load* — an unregistered id is skipped (C1.8). A new runtime
  effect needs a handler, not just a chunk.
