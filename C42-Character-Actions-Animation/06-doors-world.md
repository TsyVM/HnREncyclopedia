# C42.6 — Doors & World Actions

> The animated, interactive props — doors, bells, switches — and the `ActionButton` actions that
> drive them.

## Doors (✅ verified)
- **`ActionButton::OpenDoor`** — a player-opened door (press to open).
- **`ActionButton::AutomaticDoor`** — opens on approach (Kwik-E-Mart style).
- **`CarDoorAction`** / **`ReleaseDoorsAction`** — the *vehicle* door handling during entry/exit
  (C42.3).

## Other interactive props (✅ verified)
- **`ActionButton::Doorbell`** — ring a doorbell (a scripted interaction).
- **`ActionButton::PlayAnim` / `PlayAnimLoop` / `PlayAnimOnce`** — play a prop's animation on
  interaction (one-shot or looping).
- **`ActionButton::AutoPlayAnim` / `AutoPlayAnimLoop` / `AutoPlayAnimInOut`** — auto-play
  (no button), including an in→hold→out cycle.
- **`ActionButton::ToggleAnim` / `ReverseAnim` / `AnimSwitch`** — toggle between states, play in
  reverse, or switch animation.
- **`ActionButton::AnimCollisionEntityDSGWrapper`** — wraps an animated collision entity so its
  collision follows the animation.

## How a prop becomes interactive
A level/entity script attaches the appropriate `ActionButton` to a prop and names the animation to
play. The prop's animated geometry (an `AnimEntityDSG` / `AnimCollisionEntityDSG`) is driven by an
animation player (C42.5); the `ActionButton` decides *when* (on press / on approach / auto).

## Why so many variants
Each variant captures a common interaction idiom (open once, loop, toggle, auto in/out) so
designers pick a behaviour rather than script it — the same data-driven philosophy as the rest of
the action model (C42.1).

## What happens if you bend it
Attach a different `ActionButton` variant to change how a prop reacts; retexture/re-animate the
prop. Custom variants are native work.

## Cross-references
C42.1 (the `ActionButton` family), C42.5 (players), C11 (collision that follows animation), C42.3
(car doors), C41 (`EnterInterior` doors).
