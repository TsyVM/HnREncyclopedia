# C42.4 — Locomotion

> On-foot movement is a **locomotion set**: a rig plus a bundle of directional animations the
> engine blends by movement direction and speed.

## What a locomotion is (✅ verified)
The exe asserts:
```
Locomotion specified without rig.
Incorrect number of animations specified for locomotion; %d are required.
Too many animations required for locomotion.
Degenerate locomotion, direction count is less than 1.
Degenerate locomotion, velocity count of %d is less than 2.
```
So a locomotion = **a rig + an exact-count set of animations** indexed by **direction** and
**velocity**. Tokens `locomotion4` and `locomotion8` are the 4-direction and 8-direction sets
(more directions = smoother turning).

## The classes (✅ verified)
- **`ChangeLocomotion`** — switch a character's active locomotion set (e.g. walk→run, or a
  special state).
- **`PhysicsLocomotion`** — physics-driven motion.
- **`WalkerLocomotionAction`** — the on-foot walk action.
- **`VehicleLocomotion`** / **`TrafficLocomotion`** — the vehicle and ambient-traffic variants.
- **`PhysicsLocomotion`** ties motion to the sim (C35).

## How it blends
At runtime the character's velocity vector picks the nearest direction bin(s) and speed level;
the player blends the corresponding animations. Too-few animations → the "degenerate/insufficient"
asserts; that's an authoring constraint, and a hard limit worth respecting (C39).

## Why sets, not one clip
Directional blending from a small animation set gives responsive, omnidirectional movement
cheaply — essential for a 2003 open-world character.

## What happens if you bend it
Swap the locomotion animations for a custom walk; use `ChangeLocomotion` for a new movement
state. Respect the required animation counts or you hit the asserts.

## Cross-references
C34 (the channel substrate the animations are made of), C42.5 (players), C35 (physics locomotion),
C39 (locomotion animation-count limits), C25 (characters).
