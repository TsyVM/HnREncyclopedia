# C43.3 — Baked Vertex Lighting

> The static world carries its own light: it was lit offline and the result stored in the
> mesh's **vertex colours**. That's why the world's time of day is fixed in the geometry.

## The mechanism (✅ verified)
Pure3D meshes carry a **colour stream** alongside positions and UVs (C7). For the static world,
that colour stream *is* the lighting: during authoring, the level was lit (a sun, ambient, local
lights), and the resulting per-vertex brightness/tint was **baked** into the vertex colours. At
runtime the world is drawn with those colours modulating the textures — no runtime lights
required for static geometry.

## Why bake
- **Free at runtime:** no per-frame lighting math for a huge world.
- **Art-directed:** artists get exactly the look they painted, including bounce/ambient occlusion
  that real-time lighting of the era couldn't do.
- **Consistent:** the world looks identical every frame — good for a fixed-time-of-day level.

## The consequence
The world's time of day is **literally in the vertices**. A daytime level's geometry has bright,
cool-white vertex colours; a night level's has dark, blue-shifted ones. You can't "turn down the
sun" at runtime because there is no runtime sun for the static world — only the baked result.

## What happens if you bend it
To re-time a level you must **re-tint the vertex colours** (darken/warm them) in the world P3D,
or replace the world art with a differently-lit version. This is the hardest of the three art
changes (it touches geometry data, C7), which is why sky + camlight are usually adjusted first.

## Cross-references
C7 (mesh colour streams), C10 (the world drawables), C43.4 (dynamic objects use a real light
instead), C43.6 (re-tinting).
