# C43.2 — The Sky Dome

> The single biggest carrier of "time of day" is the **sky**, and the sky is a textured
> dome/backdrop — pure art, not a simulated atmosphere.

## What it is (✅ verified — C33.3)
Chapter 33.3 established that SHAR's sky has **no code system**: it is a drawable (a dome or
backdrop geometry) with a **texture**, drawn behind the world. There is no atmospheric
scattering, no sun position math, no cloud simulation — the clouds, the gradient, the sun glow
are all *painted into the texture*.

## How it carries the time of day
- **Daytime (L1):** a bright blue sky texture with white clouds.
- **Sunset (L3):** an orange/pink gradient texture.
- **Night (L7):** a dark blue/black texture, often with stars/moon painted in.

Because the whole mood is in the image, swapping the sky texture is the highest-leverage single
change to a level's time of day.

## Why a dome, not a simulation
A textured dome renders in one cheap pass and gives the artists total control of the look. For a
stylized, cartoon world (very on-brand for The Simpsons), a painted sky is *better* than a
simulated one — it matches the show's flat, illustrated aesthetic.

## What happens if you bend it
Replace the sky dome texture (a PNG/texture in the level's art, C5) with a different time-of-day
painting and the level's whole atmosphere shifts. Pair with vertex-light and camlight changes
(C43.3/43.4) for a consistent result — a new sky over day-lit geometry looks wrong.

## Cross-references
C33.3 (sky-is-art), C5 (the sky texture), C7 (the dome geometry), C43.6 (swapping it).
