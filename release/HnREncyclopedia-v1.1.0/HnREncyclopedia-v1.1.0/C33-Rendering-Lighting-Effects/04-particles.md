# C33.4 — Particles & Emitters

**What it is.** The system behind every spark, puff of smoke, burst of fire, cloud of dust, and glittering
sparkle in the game — a full **particle system** with emitters that spawn short-lived sprite particles. It's
what makes the world feel alive with small dynamic detail.

**How it works (✅ verified).** The verified particle family:

```
tParticleSystem / tParticleSystemFactory        — a particle effect, and its reusable template
tParticleSystemFactoryLoader / tParticleSystemLoader — load them from Pure3D chunks
tParticleArray / tParticlePool                  — the live particles (pooled)
tBaseEmitter / tBaseEmitterFactory              — spawn particles
tSpriteEmitter / tSpriteEmitterFactory          — emit sprite (billboard) particles
tSpriteParticle                                 — one billboard particle
ParticleSystemDSG / InstParticleSystemLoader    — a particle system placed in the scene graph (C10)
```

The architecture is **factory → system → emitter → particles**: a `tParticleSystemFactory` is the *template*
(this is what a "spark burst" looks like — its texture, lifetime, spread, colour-over-time); a
`tParticleSystem` is a *live instance* of it; its `tSpriteEmitter` *spawns* `tSpriteParticle`s (billboard
quads, C33.5) from a **pool** (`tParticlePool` — reused, not allocated per particle); and `ParticleSystemDSG`
places the whole thing in the scene graph (C10) so it's drawn and positioned in the world. The particle
texture is set from scripts (`SetParticleTexture`, C14.6) or the factory.

**Why factories and pools.** Two performance patterns, both essential for particles. **Factories** (the
template/instance split) mean one "spark burst" definition is authored once and instanced many times — every
car crash spawns the *same* spark effect from one factory. **Pools** (`tParticlePool`) mean particles are
*reused*, not allocated and freed each time — a fixed buffer of particle slots is recycled as particles are
born and die. Particles are born and die constantly (hundreds per second in a busy scene), so per-particle
allocation would thrash memory; a pool makes it free. This is the same object-pooling as the HUD map icons
(C29.1) and the standard approach for any high-churn objects.

**Particles as sprites.** SHAR's particles are **sprite particles** (`tSpriteParticle`) — camera-facing
billboard quads (C33.5), each a small textured square that always faces you. This is the classic, cheap way
to do particles on fixed-function hardware (C33.1): a spark is a tiny bright quad, smoke is a soft grey quad
fading out, and orienting them toward the camera makes flat quads look volumetric. The emitter controls how
they spawn (rate, spread, velocity) and how they evolve (fade, grow, drift) over their short lifetime.

**Where particles appear.** Everywhere small dynamic detail is needed: car exhaust and tyre smoke (C24),
crash sparks and debris, the sparkle on collectibles (`GagSetSparkle`, C14.4), fire, dust, the nitro effect.
Each is a particle system instanced from a factory, placed as a `ParticleSystemDSG` in the world. Reading a
level's particle systems (the `ParticleSystemDSG` entities) inventories its dynamic effects.

**What happens if you bend it.**

- *Rely on a particle-system member offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Change `SetParticleTexture` (C14.6) to a huge texture* — particles are many small quads; a big texture per
  particle is costly. Keep particle textures small.
- *Spawn unbounded particles* — the pool (`tParticlePool`) is finite; over-emitting exhausts it (particles
  stop appearing). Respect the pool budget.
