# Chapter 39 — Engine Limits: Maximums, Pools & Exceeding Them Safely

> **Goal of this chapter:** find the game's hard numbers — max traffic, max characters, max props, max
> particles, max sounds — say *where each one lives*, and show how to raise the ones that can be raised and add
> more content that actually **loads and renders**, without crashing the game. This is the "how much can I put
> in, and how" chapter.

Every engine has ceilings. SHAR's are enforced by three different mechanisms, and the mechanism decides how (and
whether) you can lift the ceiling. Some limits are **numbers in a script** you can just edit; some are the size
of a **memory pool** you must enlarge; a few are **hard assumptions** in the code that fight back. This chapter
sorts SHAR's limits into those three buckets — using the game's own error strings and a live memory capture as
evidence — and gives a safe method for pushing each.

**Key finding (✅ verified from the retail exe + a live capture):** SHAR's limits fall into three tiers. **(1)
Script-configurable** — the engine literally tells you where: *"See leveli.mfk to increase the max allowed for
this model"*, and exposes `SetMaxTraffic`, `maxPropCount`, `maxDriverCount`, and per-model instance caps
(*"we already have %d of max %d instances allowed"*) through MFK/CON (C14/C15). **(2) Pool-bounded** — fixed
allocator pools (`MemoryPool`, `tParticlePool`, `AllocPool<FMVEvent/NISEvent/TransitionEvent>`,
`radSoundHalBufferDataPool`) whose sizes cap particles, sounds, and events; a live capture shows round
populations (`tSpriteParticle` ×1000, `daSoundResourceData` ×5000) that betray those caps. **(3) Hard limits** —
guarded by fatal checks like *"Static heap full"*, *"Tried to add too many PCs, not supported right now"*, and
*"Too many animations required for locomotion"*, which you exceed at your peril. The trick to modding SHAR big
is knowing which tier a limit is in **before** you push it.

---

## Deep-dive pages

- [C39.1 — The Limit Taxonomy](01-the-limit-taxonomy.md): the three tiers, the exe error strings that prove them, and the live pool populations.
- [C39.2 — Script-Configurable Limits](02-script-configurable.md): `SetMaxTraffic`, per-model max in `leveli.mfk`, `maxPropCount`/`maxDriverCount`, `AddCharacter` — the easy wins via MFK/CON.
- [C39.3 — Memory Pools & the Static Heap](03-memory-pools.md): the pool system, particle/sound/event pools, `Static heap full`, and enlarging a pool.
- [C39.4 — Adding Content that Loads & Renders](04-adding-content.md): getting new objects/vehicles/peds to actually stream in (RCF/P3D + GameFlow, C30) and draw (scenegraph + render, C10/C33).
- [C39.5 — Sounds & Effects Past Their Caps](05-sounds-effects.md): more sounds (RSD + sound-buffer pool) and more effects (particle pool, `tSpriteParticle`).
- [C39.6 — Exceeding Limits Safely](06-exceeding-safely.md): measure-first with SAHRDiag, raise the right lever, watch the heap, test — and the debug/limits menu that ties this to C38.

---

## 39.1 The three tiers (✅ verified)

| Tier | Enforced by | Raise it by | Evidence (exe string) |
|---|---|---|---|
| **Script** | a number read from MFK/CON | edit the script | *"See leveli.mfk to increase the max allowed for this model"* |
| **Pool** | a fixed allocator pool | enlarge the pool (hook/patch) | `tParticlePool`, `radSoundHalBufferDataPool`, `AllocPool<…>` |
| **Hard** | a fatal `if` in the code | avoid / deep patch | *"Static heap full"*, *"Tried to add too many PCs"* |

[C39.1](01-the-limit-taxonomy.md) lays out every limit string and the live evidence.

## 39.2 Script limits — the easy wins (✅ verified)

The engine advertises these. `SetMaxTraffic` caps on-road traffic; per-model caps are set in `leveli.mfk`
(*"we already have %d of max %d instances allowed"*); `maxPropCount` / `maxDriverCount` bound props and drivers.
All are MFK/CON values (C14/C15) — **edit the script, raise the number**. [C39.2](02-script-configurable.md).

## 39.3 Pools — enlarge the allocator (✅ verified)

Particles, sounds, and events come from **fixed pools**. A live capture caught `tSpriteParticle` at exactly
**1000** and `daSoundResourceData` at **5000** — round numbers that are the pool sizes, not coincidences. To
exceed them you enlarge the pool at init (a DonutsSDK hook, C28.5), and watch the **static heap**
(*"Static heap full — requested:%d available:%d overflow:%d"*). [C39.3](03-memory-pools.md).

## 39.4 Adding content (✅ practical)

A higher cap is useless if the content never loads or draws. Adding objects/vehicles/peds means: put the asset
in an RCF/P3D (C2/C1), reference it from the level's MFK (C14), let the **GameFlow loader** stream it (C30), and
ensure it enters the **scenegraph** so the renderer draws it (C10/C33). [C39.4](04-adding-content.md).

## 39.5 Sounds & effects (✅ practical)

More sound variety needs RSD samples in an RCF (C18/C19) and room in `radSoundHalBufferDataPool`; more on-screen
effects need room in `tParticlePool`. Both are pool-tier limits. [C39.5](05-sounds-effects.md).

## 39.6 Doing it safely (✅ method)

Measure the live population with SAHRDiag (C28.7) to see how close you are to a cap, raise the correct lever for
that tier, keep an eye on the static heap, and test incrementally. A small in-game **limits/debug menu**
(built with C38) makes this tuning practical. [C39.6](06-exceeding-safely.md).

---

## What this chapter establishes

- SHAR's ceilings are **three-tier**: script numbers, allocator pools, and hard code checks — and the tier
  dictates the method.
- **Script limits** (traffic, per-model, props, drivers) are edits to MFK/CON (C14/C15) — the safest, biggest
  wins.
- **Pool limits** (particles ~1000, sound resources ~5000, event pools) are enlarged by hooking the pool init
  (C28.5), bounded by the **static heap**.
- **Hard limits** (playable-character count, static heap, locomotion animation counts) resist and should be
  respected or approached very carefully.
- Adding content is a pipeline: **author → package (RCF/P3D) → reference (MFK) → load (GameFlow) → render
  (scenegraph)** — a cap raise plus all five steps.

**Cross-references:** C1/C2 (P3D/RCF packaging), C10 (scenegraph — getting drawn), C14/C15 (MFK/CON — the
scripts that hold the numbers), C18/C19 (sound), C28.5/C28.7 (hooking + measuring), C30 (GameFlow loading),
C33 (rendering & particles), C38 (a menu to drive the tuning).
