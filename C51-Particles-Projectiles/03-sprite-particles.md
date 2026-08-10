# C51.3 — Sprite Particles

> Every effect particle is a **sprite** — a camera-facing textured quad. Cheap, always readable,
> perfect for sparks, dust, stars, and rings.

## What a sprite particle is (✅ verified)
`tSpriteParticle` is a single billboarded quad: a small textured rectangle that always **faces the
camera** (a billboard, C33). `tSpriteEmitter` (+`Factory`, +`Loader`) spawns them; `tSprite` is the
sprite primitive. Because the quad turns to face you, a flat texture (a spark, a puff) reads as a 3D
effect from any angle.

## How it draws
```
tSpriteEmitter spawns tSpriteParticle (textured quad, slot texture from C51.2)
   → billboarded to face camera → alpha-blended → fades over its lifetime → recycled (C51.4)
```
Sprites are alpha-blended so sparks/dust glow and fade rather than pop. They draw in the transparent
pass of the renderer (C33).

## Why sprites, not 3D particles
A camera-facing textured quad is the cheapest way to render a convincing small effect: one quad, one
texture, no geometry cost. For hundreds of concurrent sparks/dust motes, that efficiency is essential
(and bounded by the pool, C51.4). It's the universal 2003-era particle technique.

## The live evidence
The diagnostic capture caught `tSpriteParticle` at ~1000 live instances — confirming both that
effects are sprite particles and that they're pool-capped (C51.4/C39).

## Bend it
Retexture (C51.2). For new look/behaviour, author a sprite emitter asset. Hook `tSpriteEmitter` for
runtime control (C28.5).

## Cross-references
C33 (billboards/sprites/transparent pass), C51.2 (slot textures), C51.4 (the ~1000 pool), C51.1 (the system).
