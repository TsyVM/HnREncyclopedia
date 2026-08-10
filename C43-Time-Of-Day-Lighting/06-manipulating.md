# C43.6 — Manipulating the Look

> Time of day is art, so you change it with an **art mod** — three levers, easiest to hardest.
> Want a night Level 1? Here's how.

## Lever 1 — swap the sky dome texture (easiest, biggest impact)
Replace the level's sky texture (C5/C43.2) with a different time-of-day painting (night blue,
sunset orange). Via loose-file shadowing (C3.6) this is a drop-in texture swap — no code, fully
reversible. This alone dramatically shifts the mood.

## Lever 2 — adjust `camlight.p3d` (re-light dynamic objects)
Edit the global light (C43.4) so cars/characters match the new sky — dimmer and bluer for night,
warm and low for sunset. This keeps dynamic objects from looking day-lit in a night scene.

## Lever 3 — re-tint the world's baked vertex colours (hardest, most complete)
Darken/shift the world geometry's vertex colours (C43.3) so the static world itself reads as
night. This touches mesh colour streams in the world P3D (C7) — the most involved change, but the
only way to make the *buildings and streets* themselves look night-time rather than just the sky.

## Doing it consistently
A convincing re-time needs all three in agreement: a night sky over day-lit streets and day-lit
cars looks broken. Start with the sky (lever 1) to prototype, then bring camlight (2) and finally
the world tint (3) into line.

## What you can't do
You can't animate a day→night *cycle* at runtime — there's no time-of-day system to drive
(C43.1). You can only ship a different fixed look. A true cycle would be a substantial native mod
(a new lighting system), not a value tweak.

## Discipline
Back up the original art; use loose-file shadowing so it's reversible; single-player/offline
(C28.6). Test in-game — baked lighting and sky must read together.

## Cross-references
C43.1–43.4 (the three art places), C5/C3.6 (texture swap + shadowing), C7 (vertex re-tint),
C28 (modding toolchain).
