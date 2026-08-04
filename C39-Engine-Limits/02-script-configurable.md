# C39.2 — Script-Configurable Limits

> The best kind of limit: a number in a script you can just edit. This page covers the maximums SHAR reads from
> MFK/CON — traffic, per-model instances, props, drivers, characters — and how to raise them.

## Why these are the easy wins

Tier-1 limits (C39.1) are values the engine loads from a level's MFK or a CON script (C14/C15) at level load.
Change the value, reload the level, done — no code, no memory surgery. The engine even points you at the file:
*"See leveli.mfk to increase the max allowed for this model."*

## Traffic — `SetMaxTraffic` (✅ verified lever)

On-road traffic density is capped by `SetMaxTraffic`, a script command. Raising it puts more AI cars on the
road at once (up to what the traffic pool and path system will bear). It pairs with the path/road system
(`PathManager`/`RoadManager`, seen live in the capture) that places them. Raise gradually — traffic also feeds
collision and AI budgets.

## Per-model instance cap (✅ verified)

Each model has a maximum number of simultaneous instances, checked at spawn:

```
"we already have %d of max %d instances allowed."
"See leveli.mfk to increase the max allowed for this model."
```

The cap is set per model in the level's MFK. This is the lever for "I want more of *this* car / prop / ped on
screen": find the model's max in `leveli.mfk` and raise it. The check exists precisely so a script can't
overrun the model's reserved slots — so raise the reserve to match your ambition.

## Props & drivers — `maxPropCount`, `maxDriverCount` (✅ verified fields)

The exe exposes `maxPropCount` and `maxDriverCount` as tunables. Props are the world's placeable objects
(bins, boxes, breakables); drivers are the AI that occupy vehicles. Both are numbers a script sets; raise them
to populate a busier world, within the prop/collision budgets.

## Characters — `AddCharacter` and the PC caution (✅ verified)

Non-player characters are added by script (`AddCharacter` and kin). Pedestrian density is effectively a
Tier-1/Tier-2 mix: the *spawn* is scripted, the *population* is pool-bounded. But **playable characters (PCs)
are a hard limit** — the engine warns:

```
"Tried to add too many PCs, not supported right now. Check level scrips for multiple AddCharacter calls."
```

So: adding more **pedestrians/NPCs** via script is fine (mind the pool, C39.3); adding more simultaneous
**playable characters** is a Tier-3 hard limit (C39.1) — don't, without deep work.

## Other script tunables seen in the exe

`SetMaxSpeedBurstTime`, `SetMaxWheelTurnAngle`, `SetSuspensionLimit`, `maxCurrentVelocity`,
`maxDesiredVelocity`, `maxCurrentAcceleration` — these bound *vehicle behaviour* rather than object counts, but
they are the same kind of lever (script-set values) and belong to the physics tuning in C35. Listed here so you
know they're editable, not hard-coded.

## Workflow

1. Identify the model/system and open the level's MFK (C14) — `leveli.mfk` for the per-model caps.
2. Find the relevant `SetMax…` / `max…Count` / per-model max.
3. Raise it in a **modest** step; reload the level.
4. Watch for the pool/heap ceilings (C39.3) — a Tier-1 raise can push you into a Tier-2/3 wall.
5. Measure with SAHRDiag (C28.7) to confirm the new population and that you're clear of caps.

## Cross-references

- **C14/C15 — MFK/CON**: the script format and command reference.
- **C35 — Vehicle Physics**: the `SetMax…` behaviour tunables.
- **C39.3** — the pools a raised script count then presses against.
