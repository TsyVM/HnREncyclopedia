# C44.1 — What "Level Init" Means

> `leveli.mfk` is the level's **initialization** script. Its own header comment states the rule:
> *"Anything here is persistent across the entire level."* Everything else follows from that.

## Persistent vs per-mission (✅ verified)
- **`leveli.mfk` (init):** runs once at level load; what it creates lives for the whole level —
  the player's car, the police, crowds, traffic, spawn points, the coin model.
- **`level.mfk` (content):** the level's gags/interiors and world content (C41.4).
- **`m{N}l.mfk` (mission logic) / `m{N}i.mfk` (mission init):** per-mission; set up when the
  mission starts and **torn down** when it ends.

So the same world has two layers: a persistent base (init) and transient missions on top.

## Why the split
An open-world level must keep its ambient life (crowds, traffic, cops) running *between* missions,
while each mission adds and removes its own actors and objectives. Separating persistent init from
per-mission setup makes both clean: the world never "resets" when you finish a mission, and a
mission can't leak actors into the persistent world.

## The `i` = init, not interior
The `i` suffix throughout the mission scripts means **init**: `leveli.mfk` = level init,
`m0i.mfk` = mission 0 init. (Interiors are declared in `level.mfk` via `GagSetInterior`, C41.4 —
a common point of confusion.)

## What happens if you bend it
Put something in `leveli.mfk` and it persists all level; put it in a mission script and it's
scoped to that mission. Choosing the right file is the difference between a permanent change and
a temporary one.

## Cross-references
C44.2 (load order), C41.4 (`level.mfk` vs `leveli.mfk`), C16 (missions), C14 (MFK).
