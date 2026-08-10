# C39.1 — The Limit Taxonomy

> Before you push a limit, know which of three kinds it is — because the kind decides the method, the risk, and
> whether it's even possible. This page classifies SHAR's limits with the exe's own error strings and a live
> memory capture as evidence.

## Tier 1 — Script-configurable (edit a number)

Some maximums are just values the engine reads from a level's MFK or a CON script (C14/C15). The engine tells
you so, in its own strings:

```
"See leveli.mfk to increase the max allowed for this model"
"we already have %d of max %d instances allowed."
```

and it exposes the levers as script commands and fields:

| Lever | Governs | Where |
|---|---|---|
| `SetMaxTraffic` | on-road traffic vehicle count | MFK/CON (C14/C15) |
| per-model max | how many of one model may spawn | `leveli.mfk` |
| `maxPropCount` | world props | level script |
| `maxDriverCount` | drivers | level/vehicle script |

**Raise by:** editing the script. Lowest risk, biggest practical wins — [C39.2](02-script-configurable.md).

## Tier 2 — Pool-bounded (enlarge an allocator)

Many object kinds are served from **fixed-size allocator pools**. When the pool is full, no more of that thing
can exist. The exe names the pools:

```
.?AVMemoryPool@@                     ; general memory pool
.?AVtParticlePool@@                  ; particle pool  → effects
.?AV?$AllocPool@VFMVEvent@@@@        ; FMV event pool
.?AV?$AllocPool@VNISEvent@@@@        ; NIS event pool
.?AV?$AllocPool@VTransitionEvent@@@@ ; transition event pool
radSoundHalBufferDataPool            ; sound buffer pool → sounds
groundplanepool / lightpool          ; world-render pools
```

**The live-capture smoking gun (✅ verified).** A SAHRDiag dynamic run (C28.7) counted live instances per class.
Two are suspiciously round — those are pool sizes, not accidents:

| Class | Live count | Reads as |
|---|---|---|
| `tSpriteParticle` | **1000** | the particle pool cap |
| `daSoundResourceData` | **5000** | the sound-resource pool cap |
| `radBaseObject` | 1445 | general object churn |
| `tTexture` | 1269 | loaded textures this level |
| `sim::CollisionObject` | 336 | active collidables |

A cap that shows up as an exact round number in memory is a pool you can enlarge. **Raise by:** hooking the
pool's init to allocate a bigger pool (C28.5), within the static-heap budget — [C39.3](03-memory-pools.md).

## Tier 3 — Hard limits (a fatal check)

A few limits are guarded by fatal `if`s that stop the game rather than degrade. The strings are blunt:

```
"Static heap full - requested:%d.  available:%d.  overflow:%d."
"Tried to add too many PCs, not supported right now. Check level scrips for multiple AddCharacter calls."
"Too many animations required for locomotion."
"Too many transitions required to build this locomotion."
"Too many animations required to build this locomotion."
"Width too large to process image data; rowbytes will overflow."
```

These say what they mean: the **static heap** is the master memory ceiling every pool draws from; the **playable
character (PC) count** is explicitly *"not supported right now"*; **locomotion** has animation/transition
ceilings; textures have a width ceiling. **Raise by:** mostly *don't* — respect them, or approach with deep
patching and heavy testing ([C39.6](06-exceeding-safely.md)).

## The decision rule

```
Is the max named in a script string?         → Tier 1: edit the script.        (safe)
Is it a pool / round live count?              → Tier 2: enlarge the pool.       (moderate)
Is it guarded by a fatal "full/too many"?     → Tier 3: avoid or patch deeply.  (risky)
```

Everything else in this chapter is applying that rule to specific content — traffic, peds, props, particles,
and sounds.

## Cross-references

- **C14/C15 — MFK/CON**: where Tier-1 numbers live.
- **C28.7 — SAHRDiag**: measuring live populations to spot Tier-2 caps.
- **C39.3** — the pool/heap mechanics behind Tier 2 and Tier 3.
