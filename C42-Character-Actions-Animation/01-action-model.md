# C42.1 — The Action Model

> A character doesn't have hard-coded verbs; it runs **action objects**. World objects offer
> context actions through the `ActionButton::*` family.

## Actions as objects (✅ verified)
Behaviours are discrete typed objects (confirmed classes): `KickAction`, `InCarAction`,
`CarDoorAction`, `PlayAnimationAction`, `HoldAnimationAction`, `WalkerLocomotionAction`,
`ReleaseDoorsAction`, etc. An action encapsulates *what to do* and *which animation to play*, so
the character's controller just runs the current action to completion (or interrupt).

## The `ActionButton::*` family (✅ ~20 confirmed classes)
An `ActionButton` is a **context prompt** a world object exposes when the player is near and
presses the action key. Confirmed members include:

| Group | Members |
|---|---|
| Vehicles | `GetInCar` |
| Interiors | `EnterInterior` (C41) |
| Doors | `OpenDoor`, `AutomaticDoor`, `Doorbell` |
| Animation | `PlayAnim`, `PlayAnimLoop`, `PlayAnimOnce`, `AutoPlayAnim`, `AutoPlayAnimLoop`, `AutoPlayAnimInOut`, `ToggleAnim`, `ReverseAnim`, `AnimSwitch` |
| Wrappers | `AnimCollisionEntityDSGWrapper` |

## Why this design
Actions-as-objects makes behaviour **data-driven and composable**: a level/entity script attaches
an `ActionButton` to a prop to make it interactive, without new engine code. The same
`PlayAnimOnce` action drives any one-shot animated prop; the same `GetInCar` drives every car.

## What happens if you bend it
Attach an `ActionButton::PlayAnimLoop` to a prop to make it interactive; hook the action
controller to inject or alter actions. Adding a *new* action type is native work (a new class);
reusing the existing ones is script work.

## Cross-references
C42.2–42.6 (specific actions), C41 (`EnterInterior`), C25 (the character/AI that runs actions).
