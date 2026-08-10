# C43.4 — `camlight.p3d`: the Global Light

> Dynamic objects can't use baked vertex lighting (they move), so they're lit by a global light
> asset — `camlight.p3d` — that keeps cars and characters consistent with the scene.

## What it is (🟡 reasoned)
`camlight.p3d` is a light asset shipped in the game's art and loaded by the engine **directly**
(it is *not* referenced by any level script — an exhaustive grep finds no mention, so the engine
loads it by a fixed name at startup). Its role is the **camera-relative directional light** — the
"sun" for dynamic objects: it lights cars, characters, and props from a consistent direction so
they read against the baked world instead of looking flat or mismatched.

## Why a separate light for dynamic objects
Static geometry has baked light (C43.3); moving objects can't. Without a global light, a car
driving through Springfield would be unlit and look pasted on. A single camera-relative
directional light is the cheap, classic solution: one light, applied to everything dynamic,
tuned to match each level's baked mood.

## How it ties to time of day
For a level's dynamic objects to match its time of day, `camlight`'s direction/colour is set to
agree with the baked world (warm and high for noon, low and orange for sunset, dim and blue for
night). If you re-time a level's world art but leave `camlight` unchanged, cars will look
day-lit in a night scene — so `camlight` is part of the time-of-day art set.

## What happens if you bend it
Adjust `camlight.p3d` (its light colour/direction, via the P3D light chunks, C33) to re-light all
dynamic objects at once — the fastest way to shift how cars/characters read without touching the
world geometry.

## Cross-references
C33 (the `tLight` family / lighting), C43.3 (baked light for static world), C43.6 (editing camlight),
C7/C1 (the P3D asset).
