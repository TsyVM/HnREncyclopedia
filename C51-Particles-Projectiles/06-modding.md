# C51.6 — Modding Effects

> Particles and projectiles are data-driven (textures + stats) with confirmed classes, so most
> effect mods are asset/script edits.

## Retexture an effect (easiest)
Change any slot's texture via `SetParticleTexture(index, "yourtex")` (C51.2), or shadow the effect
texture file (`spark4.bmp`, `cloud.tga`, `star.tga`, `halo.bmp`, …) with your own (C5/C3.6). Instant
new look for sparks/dust/stars/shockwaves — no code.

## Tune projectiles
Edit `SetProjectileStats("waspray", speed, param)` (C51.5) to change the wasp ray's speed and
difficulty. It's a script value per mission.

## Add / intensify particles
More concurrent particles press `tParticlePool` (~1000, C51.4) — enlarge the pool at init (C39.3) if
you want denser effects, paying static heap. Author a new particle-system asset for a genuinely new
effect (C51.1).

## Native (DonutsSDK + VanHooks)
Hook `tSpriteEmitter`/`tParticleSystem` or `Projectile`/`AttackBehaviour` (confirmed classes) to change
spawn behaviour or projectile logic at runtime (C28.5/C28.7).

## Cautions
- Effect textures should keep alpha/format the engine expects (C5).
- Don't exceed the particle pool expecting more to appear — measure and enlarge (C39.6).
- Reversible, single-player/offline (C28.6).

## Cross-references
C51.2 (slot textures), C51.4/C39 (the pool), C5/C3.6 (texture assets/shadowing), C51.5 (projectiles),
C28.5/28.7 (hooking).
