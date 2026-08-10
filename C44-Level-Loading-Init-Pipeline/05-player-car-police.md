# C44.5 — The Player, Car & Police Setup

> The three things every level must stand up first: the player, their starting vehicle, and the
> police that chase them.

## The player & car (✅ verified)
```
InitLevelPlayerVehicle("famil_v", "level1_carstart", "DEFAULT");
AddCharacter("homer", "homer");
```
- `InitLevelPlayerVehicle(model, startLocator, config)` — spawns the level's **starting vehicle**
  (`famil_v` = the family sedan) at a named start **locator** (`level1_carstart`, C8) with a config
  profile. This is why you begin each level in a specific car at a specific spot.
- `AddCharacter(name, model)` — creates the player character (Homer by default; the playable
  character changes per level/story).

## The police (✅ verified — C31)
```
CreateChaseManager("cPolice", "Pursuit\\L1cop.con", 1);
SetNumChaseCars("1");
SetHitAndRunDecay(3.0);
```
- `CreateChaseManager(name, copConfig, flag)` — arms the pursuit system with the **cop car's `.con`
  config** (per level: `L1cop.con`). This is the `ChaseManager` of C31.
- `SetNumChaseCars(N)` — how many cop cars pursue at once (escalates with the level).
- `SetHitAndRunDecay(seconds)` — how quickly the Hit & Run meter cools when you stop offending.

## Why in init
The player, their car, and the police must exist for the *whole* level (they persist across
missions), so they're created once in init — not per mission. A mission may *reposition* the
player or change cop counts, but the base entities live here.

## What happens if you bend it
Change the starting car (swap `famil_v`), the start locator, the cop count, or the decay rate by
editing these init lines. The car model must be loaded (C44.2) and have a `.con` (C15).

## Cross-references
C24/C35 (the vehicle), C8 (start locator), C31 (police/chase), C15 (the cop `.con`), C25 (the player character).
