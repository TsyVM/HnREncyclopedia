# C51.2 — The Effect Slots

> The game exposes a fixed set of particle **effect slots**, assigned textures in the level script.
> The retail comments name every one — a rare, direct window into the developers' intent.

## The slots (✅ verified — from the game's own comments)
```
SetParticleTexture( 0, "scratch2.bmp" ); // sparkles.
SetParticleTexture( 1, "spark4.bmp" );   // sparks when vehicle hits.
SetParticleTexture( 2, "cloud.tga" );    // dust cloud when running/jumping.
SetParticleTexture( 3, "cloud.tga" );    // leaves when hitting shrubs/trees.
SetParticleTexture( 4, "star.tga" );     // stars when hitting something static.
SetParticleTexture( 5, "cloud.tga" );    // paint chips when vehicle is damaged.
SetParticleTexture( 6, "halo.bmp" );     // Ring for shock wave fx.
```

| Slot | Trigger | Texture |
|---|---|---|
| 0 | ambient/pickup **sparkles** | `scratch2.bmp` |
| 1 | **vehicle hits** something → sparks | `spark4.bmp` |
| 2 | **running/jumping** on foot → dust | `cloud.tga` |
| 3 | **hitting shrubs/trees** → leaves | `cloud.tga` |
| 4 | **hitting a static object** → stars | `star.tga` |
| 5 | **vehicle damaged** → paint chips | `cloud.tga` |
| 6 | **shockwave** fx → ring | `halo.bmp` |

## How it works
Each slot is a preconfigured emitter; the gameplay event (a vehicle collision, a foot-step, a tree
hit) fires the matching slot at the contact point. `SetParticleTexture(index, tex)` just assigns which
texture that slot draws — so the *behaviour* is fixed per slot, the *look* is data.

## Why fixed slots
A small, named set of effect slots keeps the common feedback (hit, dust, damage) consistent and cheap
across the whole game, while still being re-skinnable per level. The devs' comments show these were
deliberately enumerated — not ad-hoc.

## Bend it
Swap any slot's texture for a custom effect look (C51.6). The trigger→slot mapping is engine
behaviour; changing *when* a slot fires is a native hook (C28.5).

## Cross-references
C51.1 (the system), C51.3 (how sprites draw), C35 (vehicle-hit/damage triggers), C5 (the textures),
C51.6 (modding).
