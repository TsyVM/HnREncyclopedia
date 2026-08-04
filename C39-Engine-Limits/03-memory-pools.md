# C39.3 — Memory Pools & the Static Heap

> Particles, sounds, and events don't allocate freely — they come from fixed pools carved out of a static heap
> at startup. This page explains the pool system, the caps a live capture revealed, the static-heap ceiling
> above them all, and how to enlarge a pool.

## The pool model (✅ verified)

SHAR pre-allocates **fixed-size pools** for high-churn objects, so it never fragments the heap mid-game. The exe
names them:

| Pool (mangled name) | Serves |
|---|---|
| `MemoryPool` / `IRadMemoryPool` | general fixed-block allocation |
| `tParticlePool` | particles (effects) |
| `radSoundHalBufferDataPool` | sound buffers |
| `AllocPool<FMVEvent>` | full-motion-video events |
| `AllocPool<NISEvent>` | NIS (scripted cutscene) events |
| `AllocPool<TransitionEvent>` | transition events |
| `groundplanepool`, `lightpool` | world-render helpers |

A pool has a fixed **capacity** set when it's created. Ask for one more than capacity and you either get nothing
(the effect silently doesn't spawn) or, for critical pools, a fatal heap error.

## The caps, caught in the act (✅ verified)

A SAHRDiag dynamic capture (C28.7) counted live instances. The round numbers are the pool capacities:

| Class | Live count | Pool it implies |
|---|---|---|
| `tSpriteParticle` | **1000** | particle pool ≈ 1000 slots |
| `daSoundResourceData` | **5000** | sound-resource pool ≈ 5000 slots |

When your effect-heavy scene stops spawning new particles, or a busy soundscape starts dropping sounds, you're
hitting these. The capture *proves* the cap exists and gives you its size — the starting point for enlarging it.

## The static heap — the master ceiling (✅ verified)

Every pool is carved from a **static heap** reserved at startup. Its exhaustion is fatal and explicit:

```
"Static heap full - requested:%d.  available:%d.  overflow:%d."
```

This is the number that ultimately bounds everything: enlarging one pool consumes heap that another pool, or the
level's assets, needed. **You cannot enlarge pools for free** — you spend static heap. So pool tuning is a
zero-sum budgeting exercise, and the static-heap message is the alarm that says you overspent.

## Enlarging a pool (✅ method)

Pools are sized at initialization, so you intercept that init and request a larger capacity:

1. **Find the pool's init** — the function that creates the pool with its capacity argument. Locate it via its
   name string / SAHRDiag (C28.7).
2. **Hook it** (DonutsSDK + VanHooks, C28.5) and substitute a larger capacity, *or* patch the immediate
   capacity constant if it's a literal.
3. **Pay for it** — either raise the static-heap reservation to match, or reclaim heap by shrinking something
   you don't use (e.g. a mode you removed).
4. **Verify** — run SAHRDiag again; the live cap should rise, and you should stay clear of *"Static heap full"*.

```cpp
// Illustrative: enlarge the particle pool at init.
static InitFn orig_particlePoolInit;
void __fastcall hk_particlePoolInit(void* self, void*, int capacity) {
    orig_particlePoolInit(self, capacity * 2);   // 1000 -> 2000, if the heap can pay
}
```

## Event pools (FMV / NIS / Transition)

The `AllocPool<…Event>` pools bound how many cutscene/transition events can be queued. These rarely need
raising for gameplay mods, but if a heavily-scripted sequence stops firing events, these are the cap — same
enlarge-at-init method.

## Practical guidance

- **Measure before you enlarge.** SAHRDiag tells you the current cap and how close you run to it — don't guess.
- **Double, then test.** Enlarge in modest multiples and watch the static heap, not all at once.
- **Prefer Tier-1 first.** If a script number (C39.2) achieves your goal, do that before touching pools.

## Cross-references

- **C28.5 / C28.7** — hooking pool init and measuring live populations.
- **C39.1** — the tier taxonomy (pool vs script vs hard).
- **C39.5** — the sound and particle pools specifically, for content mods.
