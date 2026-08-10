# C51.4 — The Particle Pool & Limits

> Particles are drawn from a fixed pool. When it's full, new effects silently don't spawn — a real
> limit you can hit in an effect-heavy scene.

## The pool (✅ verified)
`tParticlePool` (with `tParticleArray`) pre-allocates the particle storage. A live diagnostic capture
counted `tSpriteParticle` at exactly **~1000** — the round number that betrays the pool's capacity
(the pool-tier limit of C39.1/C39.3).

## What happens at the cap (✅ verified behaviour)
Ask for one more particle than the pool holds and you get **nothing** — the effect silently doesn't
spawn (particles are non-critical, so the engine drops them rather than fail). In practice a scene
with lots of simultaneous sparks/dust/smoke will stop adding new particles once the pool is saturated,
and effects look thinner.

## Why a fixed pool
Particles are the highest-churn objects in the game (spawned and destroyed constantly). A fixed pool
gives O(1) spawn/recycle with zero fragmentation — essential at this volume — at the cost of a hard
concurrency ceiling. That trade is exactly why the cap exists (C39.3).

## Raising it (✅ method)
Enlarge `tParticlePool` at init (hook the pool init, C39.3) for more concurrent particles — paying the
extra memory from the static heap (C39). Measure first (C39.6): if effects thin out under load, you're
at the cap; if not, enlarging won't help.

## Cross-references
C39.1/C39.3 (pool-tier limits + the static heap), C39.6 (measure before enlarging), C51.3 (the sprite
particles counted), C51.1 (the system).
