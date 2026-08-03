# Chapter 23 — The RTTI Class Model

> **Goal of this chapter:** cross from files on disk to the running game. This chapter introduces the
> **verified runtime class set** — 1,207 RTTI-confirmed classes and 3,924 base-class relationships read
> straight from `Simpsons.exe` — its shape, its base spine, and how the loaded chunks of Parts I–VI become
> live objects.

Every chapter so far has ended by naming the runtime class an asset becomes, always with the same
discipline: **names ✅ from RTTI, offsets ⏳**. This chapter is where that discipline is grounded. The
evidence base is the executable's own **Run-Time Type Information** — the compiler-emitted class metadata
carried by DonutsSDK's `data/shar_dumps.csv` — and everything below was extracted and counted from it.

**Key finding (✅ verified):** the runtime is a deep single-rooted hierarchy. **386** classes derive from
`tRefCounted` (the refcounting base), **117** from `EventListener` (the event system), and a clean
**Drawable Scene Graph** spine — `tRefCounted → tEntity → tDrawable → IEntityDSG` — underlies **32** entity
types. `Vehicle` and `Character` sit on the *same* base (`DynaPhysDSG`/`CollisionEntityDSG`/`IEntityDSG`),
which is why the world treats cars and people as one kind of physical scene entity.

---

## Deep-dive pages

- [C23.1 — What RTTI Proves (and What It Doesn't)](01-what-rtti-proves.md): the evidence base, and the ✅/⏳ line.
- [C23.2 — The DSG Spine: `tRefCounted → IEntityDSG`](02-dsg-spine.md): the base hierarchy under every world entity.
- [C23.3 — Namespaces & Families](03-namespaces-families.md): `sim::`, `choreo::`, `CGui*`, `ActionButton::`, `Fe*`.
- [C23.4 — From Chunk to Class](04-chunk-to-class.md): how loaded data (Parts I–VI) becomes live objects.
- [C23.5 — Identifying a Class by its VTable](05-vtable-identification.md): the mechanism, and why offsets stay ⏳.
- [C23.6 — Using the DonutsSDK Class Database](06-using-the-db.md): querying the 1,207-class set in a mod.

---

## 23.1 The evidence base (✅ verified)

The class set comes from `_RTTIBaseClassDescriptor` records in `Simpsons.exe` — the program describing its
own types. It proves **class existence, exact names, and inheritance** (including base sub-object offsets).
It does **not** prove arbitrary member offsets, method addresses, or singleton pointers — those stay ⏳.
`shar_dumps.csv` carries **1,207 classes** and **3,924 relations**, every row tagged `CONFIRMED`.
[C23.1](01-what-rtti-proves.md).

## 23.2 The DSG spine (✅ verified)

Almost everything in the world is a **Drawable Scene Graph** entity built on one spine:

```
tRefCounted (386 derived) → tEntity → tDrawable (50 derived) → IEntityDSG (32 derived)
   ├── StaticEntityDSG → InstStatEntityDSG        (static world props, C10/C12)
   ├── CollisionEntityDSG (15 derived)            (solid geometry, C11)
   │     ├── AnimCollisionEntityDSG               (moving collision — doors, platforms)
   │     └── FenceEntityDSG                       (the fences of C13!)
   └── DynaPhysDSG (10 derived) ── Vehicle, Character, GagDrawable
```

Verified: `Vehicle` and `Character` both inherit `DynaPhysDSG, StaticPhysDSG, CollisionEntityDSG,
IEntityDSG` — cars and people are the *same kind* of physical, collidable, drawable scene entity.
[C23.2](02-dsg-spine.md).

## 23.3 Namespaces & families (✅ verified)

The set is organised into namespaces and prefix families: **`CGui*`** (74 — the UI, C21), **`sim::`** (39 —
physics, C26), **`choreo::`** (46 — choreography/animation, C17), **`ActionButton::`** (36 — context
actions), **`Fe*`** (31 — front-end), **`GuiSFX::`** (22 — UI transitions), plus `Sound`, `Scrooby`,
`radmusic`. Each maps to a subsystem this book documents. [C23.3](03-namespaces-families.md).

## 23.4 From chunk to class (✅ mechanism)

The Pure3D loader (C1.8) reads a chunk and constructs the class it describes via a **chunk-handler
registry** — the RTTI set contains the handlers themselves (`tChunkHandler`, `radLoadDataLoader`,
`sim::CollisionObjectLoader`, `CameraDataLoader`, `tCompositeDrawableLoader`). So a `0x00019000` Texture
chunk (C5) builds a texture object; a collision chunk (C11) builds a `sim::CollisionObject`; a camera chunk
builds a `SuperCam`. [C23.4](04-chunk-to-class.md).

## 23.5 & 23.6 VTables and the SDK

A live object is identified by its **vtable pointer** — the mechanism DonutsSDK uses to recognise a class
at runtime (✅ mechanism; per-class vtable addresses ⏳). The SDK's generated class DB (`shar::db`) exposes
the whole verified set to a mod for querying names and inheritance. [C23.5](05-vtable-identification.md),
[C23.6](06-using-the-db.md).

---

## Key takeaways

- The runtime is proven by **`Simpsons.exe`'s own RTTI**: 1,207 classes, 3,924 relations, all CONFIRMED.
  RTTI proves **names + inheritance**, not member offsets (⏳).
- A single **DSG spine** (`tRefCounted → tEntity → tDrawable → IEntityDSG`) underlies the world;
  **`Vehicle`** and **`Character`** share the `DynaPhysDSG`/`CollisionEntityDSG` base.
- The set is organised by namespace/family (`CGui*` 74, `choreo::` 46, `sim::` 39, `ActionButton::` 36,
  `Fe*` 31), each a documented subsystem.
- Chunks become classes via a **handler registry** (the handlers are themselves in the RTTI set).
- Classes are identified live by **vtable**; DonutsSDK exposes the verified set for querying.

**Next:** [Chapter 24 — Vehicles at Runtime](../C24-Vehicles-Runtime/C24-Vehicles-Runtime.md).
