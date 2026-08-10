# C51.1 — The Particle System

> The architecture behind every spark and dust cloud: a Pure3D factory → emitter → particle chain,
> pooled and drawn as part of the scene.

## The classes (✅ verified)
| Class | Role |
|---|---|
| `tParticleSystemFactory` (+`Loader`) | builds particle systems from asset data |
| `tParticleSystem` (+`Loader`) | a running particle effect |
| `tBaseEmitter` / `tSpriteEmitter` (+`Factory`) | spawns particles over time/space |
| `tBaseParticle` / `tSpriteParticle` | one live particle |
| `tParticleArray` / `tParticlePool` | storage/allocation for particles (C51.4) |
| `ParticleSystemDSG` / `InstParticleSystemLoader` | the particle system as a scene node (drawable) |

## How it flows (✅ mechanism)
```
asset (tParticleSystemFactory) ─► tParticleSystem
     └─ tSpriteEmitter emits ─► tSpriteParticle[] (from tParticlePool)
            └─ each particle: spawn → move/fade over lifetime → die (returned to pool)
     drawn via ParticleSystemDSG in the scenegraph (C10/C33)
```
An emitter creates particles at a rate with initial velocity/spread; each particle ages, moves, and
fades, then returns to the pool. The whole system is a **DSG node** so the renderer draws it with the
rest of the scene.

## Why a factory/emitter/pool design
It's the standard, efficient particle architecture: factories let effects be data-defined (not coded),
emitters encapsulate the spawn behaviour, and a pool avoids per-particle allocation (C51.4). The same
system serves every effect by swapping parameters and textures (C51.2).

## Bend it
Effects are data — retexture (C51.2/C51.6) or, for new behaviour, author a new particle system asset.
Hooking the emitter/system classes allows runtime changes (C28.5).

## Cross-references
C33 (rendering/effects), C10 (the scenegraph node), C51.2 (the effect slots), C51.4 (the pool).
