# C43.1 — What Sets the Time of Day

> The claim that surprises everyone: **nothing at runtime sets it.** Level 1 is day and Level 7
> is night because their *art* is day and night. Here's the proof.

## The proof by absence (✅ verified)
An exhaustive search of the retail level/mission scripts and `Simpsons.exe` finds **no**:
- `SetTimeOfDay` / `TimeOfDay`
- `SetFog` / fog render-state command
- `SetSky` / `SetSkyColour`
- `SetAmbientLight` / `SetAmbientColour` / `SetSunDirection`

There is simply no command or exposed variable that says "it is now dusk." If there were, it
would appear in the level scripts (where everything else about a level is set up) or as an exe
string. It appears in neither.

## What *is* different per level
Each level loads a **different set of world art** (C12): its terrain and world-block P3Ds, its
sky dome texture, its baked lighting. Level 1's assets were lit and skinned as bright daytime;
Level 3's as an orange sunset; Level 7's as night. The engine doesn't "compute" the time — it
draws the art it was given.

## Why the authors did it this way
2003-era hardware couldn't afford a dynamic global-illumination/time-of-day system for a big
open world. Baking the lighting offline into the art gives rich, art-directed lighting for free
at runtime — at the cost of it being *fixed* per level. That trade (fixed but beautiful vs
dynamic but flat) is exactly why each level has one immutable time of day.

## What this means for modding
You cannot "set" Level 1 to night with a flag. You change its **art**: the sky texture, the
baked vertex colours, the global light (C43.6). It's a texture/art mod, not a value edit.

## Cross-references
C12 (which art a level loads), C33.3 (sky is art), C43.2–43.4 (the three art places the look lives).
