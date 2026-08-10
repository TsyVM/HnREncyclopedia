# C42.3 — Enter & Exit a Vehicle

> Getting into and out of a car is a short **AI state sequence** plus car-door handling — and
> it's where the C40 fade/black-box is often seen.

## The state flow (✅ verified)
```
on foot ──► CharacterAi::GetIn  (anim "getin")   ──► CharacterAi::InCar  (anim "incar")
                                                                 │  driving...
        ◄── CharacterAi::GetOut ("GetOutCar") ◄──────────────────┘
```
- **`CharacterAi::GetIn`** — plays the entry animation and moves the character onto the seat.
- **`CharacterAi::InCar`** — the in-vehicle state (the character is now the driver; control
  passes to the vehicle, C24/C35).
- **`CharacterAi::GetOut`** — the exit animation back to on-foot (`Loco`, C42.4).

## The car side (✅ verified)
- **`InCarAction`** — puts a character in a car (the action object).
- **`CarDoorAction`** / **`ReleaseDoorsAction`** — open/close and release the car's doors during
  entry/exit.
- **`InCarCharacterMappable`** — maps the character into the car's driver slot.
- Script verbs: **`PutMFPlayerInCar`** (place the main-family player in a car),
  `SetMissionResetPlayerInCar` (mission reset places you back in a car),
  `StreetRace0%d_getoutofcar` (race start/finish exit).

## The fade
Certain entries/exits (mission-driven, or where the camera/world must adjust) are wrapped by the
C40 `Fader` — the "black box" the player notices. A normal open-world hop in/out is usually
seamless; the box shows when the game hides a reset/reposition.

## Why a state sequence
Entry/exit is animation-plus-logic that must not be interruptible mid-way (you can't be half in a
car). Modeling it as explicit AI states makes it atomic and gives clean hook points.

## What happens if you bend it
Retime `getin`/`GetOutCar`; skip the animation (instant enter); hook `CharacterAi::InCar` to
alter the driver hand-off. Keep entry atomic.

## Cross-references
C40 (the fade), C24/C35 (the vehicle once you're in), C42.4 (locomotion on exit), C42.1 (`GetInCar` button).
