# C46.1 — What a Traffic Group Is

> The road analogue of a ped group: a weighted pool of vehicle models the traffic system spawns
> from.

## The block (✅ verified)
```
CreateTrafficGroup( 0 );
AddTrafficModel( "minivanA", 2 );      // weight 2 — common
AddTrafficModel( "glastruc", 1, 1 );   // weight 1, flag 1 (large vehicle 🟡)
AddTrafficModel( "schoolbu", 1, 1 );
AddTrafficModel( "pickupA",  1 );
CloseTrafficGroup( );
```
- `CreateTrafficGroup(N)` opens numbered group N.
- `AddTrafficModel(model, weight[, flag])` adds a vehicle model with a relative spawn weight; the
  optional flag is 🟡 (appears on the large vehicles — glass truck, school bus — so likely a
  size/lane or special-handling marker).
- `CloseTrafficGroup()` finalizes it.

## Why a weighted pool
A handful of models plus weights produces believable, varied traffic without placing individual
cars. Weighting keeps common cars common and big rigs rare, matching a real streetscape.

## Multiple groups
Different groups let the level vary traffic by area or moment (a highway vs a suburb), and missions
can swap to a lighter group. The group is chosen by the active spawn context.

## What happens if you bend it
Re-cast traffic by editing the models/weights; add a model (must be a loaded vehicle with a `.con`,
C15/C44.2). Removing all models yields empty roads.

## Cross-references
C46.2 (spawning), C45.1 (the ped-group analogue), C15 (vehicle `.con`), C44.2 (loading).
