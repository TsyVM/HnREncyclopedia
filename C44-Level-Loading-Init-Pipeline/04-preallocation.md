# C44.4 — Preallocation & the Actor Pool

> `PreallocateActors` reserves the actor pool at level load so spawns during play are instant and
> never fragment memory. It's a direct tie between level loading and the engine's limits (C39).

## What it does (✅ verified)
Called during init, `PreallocateActors` tells the engine how many **actors** (characters/NPCs/
spawnables) to reserve capacity for up front. The pool is carved from the static heap (C39.3) once,
so every later spawn (a pedestrian, a mission NPC, a wasp) draws from the reserve instead of
allocating on the fly.

## Why preallocate
- **No mid-game hitches:** allocating during play would stutter and could fail; a reserve makes
  spawns O(1).
- **No fragmentation:** one big reservation beats thousands of small allocations.
- **A hard ceiling by design:** the reserve *is* the actor cap for the level — spawn past it and
  the engine warns/refuses (the *"Tried to add too many PCs"* / actor-limit family, C39.1).

## The limit interaction
This is exactly the pool-tier limit of C39: the preallocated actor count is a fixed pool. Raising
how many peds/NPCs a level can hold means raising this reservation — and paying for it from the
static heap (C39.3). Measure first (C39.6): a level near its actor cap won't spawn more no matter
how many `AddPed`s you add.

## What happens if you bend it
Increase the preallocation to allow denser crowds/more NPCs — within the static-heap budget. Too
high and you risk *"Static heap full"*; too low and later spawns silently fail.

## Cross-references
C39 (engine limits — pools & the static heap), C45 (peds that draw from the pool), C44.3 (the init
vocabulary), C30 (loading).
