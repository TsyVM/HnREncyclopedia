# C41.4 — Where Interiors Are Declared (`level.mfk`)

> Interiors surface in the scripts as the **scope for gags**. This page shows the real
> vocabulary and clears up which MFK file does what.

## `level.mfk` vs `leveli.mfk` (✅ verified — don't confuse them)
- **`level.mfk`** — the level's **content** script: gag definitions (and their interior
  scoping), among other level content. This is where `GagSetInterior` lives.
- **`leveli.mfk`** — the level's **init** script ("Anything here is persistent across the entire
  level"): `AddPed`, `AddAmbientCharacter`, `CreateChaseManager`, `AddTrafficModel`,
  `InitLevelPlayerVehicle`, `SetHitAndRunDecay`, ped/traffic groups. **No interior commands.**
  The `i` suffix means *init*, not "interior".

## The gag/interior vocabulary (✅ from `level.mfk`)
Gags (the interactive touch jokes/collectibles) are defined in `GagBegin … GagEnd` blocks and
scoped to an interior:
```
ClearGagBindings();
GagBegin("gag_s5.p3d");
  GagSetInterior("SimpsonsHouse");        // scope this gag to an interior
  GagSetCycle("cycle");
  GagSetPosition(500.196, -20, -400.579);
  GagSetRandom(1);
  GagSetSound("gag_s5");
  GagSetTrigger("touch", 496.942, -19.341, -394, 6.0);   // touch radius
GagEnd();
```
Other gag verbs seen: `GagSetPersist`, `GagSetCoins`, `GagSetSparkle`, `GagSetAnimCollision`,
`GagSetIntro`/`GagSetOutro`, `GagSetCameraShake`, `GagPlayFMV`. A leading comment states the
intent: *"Bind gag NISes to the interiors they can be used in."*

## What this tells us about interiors
Interiors are, from the script's view, **named spaces that gags (and NISes) attach to**. The
geometry/entrance is placed as world assets + locators (C41.1); the *content* (which gags, with
what triggers/sounds/coins) is authored in `level.mfk` under `GagSetInterior`.

## What happens if you bend it
Add/edit a `GagBegin…GagEnd` block under a `GagSetInterior` to place your own interactive gag
inside an interior (position, trigger radius, sound, coin reward). See C41.6.

## Cross-references
C14 (MFK scripts), C32 (collectibles/gags), C41.3 (the interior ids), C17 (gag NISes/FMV).
