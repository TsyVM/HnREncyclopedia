# Chapter 51 — Particles & Projectiles

> **Goal of this chapter:** decode the sparkle, spark, dust, and shockwave effects that sell every
> impact — the **particle system** — and the **projectiles** (the wasp's ray). We referenced
> `SetParticleTexture`/`SetProjectileStats` but never opened the systems behind them.

Smash a crate and it *sparkles*; a car hit throws *sparks*; running kicks up a *dust cloud*; hitting
a tree scatters *leaves*. Those effects are a proper Pure3D **particle system** (emitters, particles,
pools, factories), and the game tells us exactly what each effect is — the level script assigns the
textures with the developers' own comments.

**Key finding (✅ verified — from the game's own comments):** particle effects are a fixed set of
**textured slots** assigned in the level script via `SetParticleTexture(index, texture)`, and the
retail comments name each one:

| Slot | Texture | Effect (dev comment) |
|---|---|---|
| 0 | `scratch2.bmp` | sparkles |
| 1 | `spark4.bmp` | sparks when vehicle hits |
| 2 | `cloud.tga` | dust cloud when running/jumping |
| 3 | `cloud.tga` | leaves when hitting shrubs/trees |
| 4 | `star.tga` | stars when hitting something static |
| 5 | `cloud.tga` | paint chips when vehicle is damaged |
| 6 | `halo.bmp` | ring for shock-wave fx |

Under the hood it's a Pure3D particle architecture: `tParticleSystem`/`tParticleSystemFactory`,
`tBaseEmitter`/`tSpriteEmitter`, `tBaseParticle`/`tSpriteParticle`, drawn as sprites, allocated from
`tParticlePool` (the ~1000-slot cap of C39). **Projectiles** are separate: `Projectile`/`ProjectileDSG`
tuned by `SetProjectileStats("waspray", speed, param)` — the wasp's spray attack (C31/C47).

---

## Deep-dive pages

- [C51.1 — The Particle System](01-particle-system.md): the emitter/particle/factory/pool architecture.
- [C51.2 — The Effect Slots](02-effect-slots.md): the seven `SetParticleTexture` slots and what triggers each.
- [C51.3 — Sprite Particles](03-sprite-particles.md): `tSpriteParticle`/`tSpriteEmitter` — how a particle draws.
- [C51.4 — The Particle Pool & Limits](04-pool-limits.md): `tParticlePool`, the ~1000 cap (C39).
- [C51.5 — Projectiles](05-projectiles.md): `Projectile`/`ProjectileDSG`, `SetProjectileStats`, the wasp ray.
- [C51.6 — Modding Effects](06-modding.md): retexturing effects, tuning projectiles, adding particles.

---

## 51.1 The particle system (✅ verified classes)

A Pure3D particle system is a **factory → emitter → particles** chain: a `tParticleSystemFactory`
builds a `tParticleSystem`; a `tBaseEmitter`/`tSpriteEmitter` spawns `tBaseParticle`/`tSpriteParticle`
instances; they live in the scene as a `ParticleSystemDSG` and are pooled. [C51.1](01-particle-system.md).

## 51.2 The effect slots (✅ verified — dev comments)

Seven textured effect slots, assigned in the level script and named by the retail comments (table
above): sparkles, vehicle-hit sparks, run/jump dust, tree leaves, static-hit stars, damage paint
chips, and the shockwave ring. Each is triggered by a specific gameplay event. [C51.2](02-effect-slots.md).

## 51.3 Sprite particles (✅ verified)

Effects are **sprite particles** — camera-facing textured quads (`tSpriteParticle`) spawned by a
`tSpriteEmitter` — cheap and always face the camera, ideal for sparks/dust/stars. [C51.3](03-sprite-particles.md).

## 51.4 The pool & limits (✅ verified — C39)

Particles come from `tParticlePool`, whose live population capped at ~**1000** in the diagnostic
capture — a hard concurrency limit (C39.3). Effect-heavy scenes hit it. [C51.4](04-pool-limits.md).

## 51.5 Projectiles (✅ verified)

`Projectile`/`ProjectileDSG` are the game's projectiles; `SetProjectileStats("waspray", "120.0", "6")`
tunes the **wasp's ray** (speed 60–150, a second param 3–6). The wasps (C31/C47) fire these at you.
[C51.5](05-projectiles.md).

## 51.6 Modding (✅ practical)

Retexture any effect slot (`SetParticleTexture`), tune projectile speed/param (`SetProjectileStats`),
or add particles within the pool budget. [C51.6](06-modding.md).

---

## What this chapter established

- Impact/ambient effects are a Pure3D **particle system** (factory/emitter/sprite-particle/pool).
- The seven effect **slots** are named by the game's own comments and each maps to a gameplay
  trigger (vehicle hit, run/jump, tree, static hit, damage, shockwave).
- **Projectiles** are a separate system (`Projectile`/`ProjectileDSG`), tuned by `SetProjectileStats`
  — the wasp ray being the prime example.
- Particles are **pool-bounded** (~1000, C39).

**Cross-references:** C33 (rendering/sprites/effects — the parent chapter), C39 (the particle pool
limit), C31/C47 (wasps that fire projectiles), C35 (vehicle damage that triggers paint-chip/spark
effects), C5 (the effect textures), C14 (`SetParticleTexture`/`SetProjectileStats` scripts).
