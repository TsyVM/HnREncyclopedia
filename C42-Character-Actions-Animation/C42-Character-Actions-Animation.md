# Chapter 42 — Character Actions, Attacks & Animation

> **Goal of this chapter:** decode what a character *does* — the attack/kick, getting in and out
> of a vehicle, opening doors, playing scripted animations — and the animation machinery
> underneath (locomotion sets, action controllers, animation players). This is the "when Homer
> attacks / enters / exits a vehicle" system the book was missing.

Every character action — a kick, a car entry, a door open, an idle — is a confirmed class in an
**action + locomotion + animation** stack. Actions decide *what happens*; locomotion and the
animation players decide *how it looks*.

**Key finding (✅ verified):** actions are objects. Attacks run through **`AttackBehaviour`**
(and `UFOAttackBehaviour`, wasp `Wasp_Attack`), with Homer's melee as **`KickAction`** (anim
tokens `jump_kick`, `kickwave`, and *"Kick Swaps Character Model"*). Vehicle entry/exit is a
sequence of **`CharacterAi::GetIn` → `CharacterAi::InCar` → `CharacterAi::GetOut`** states
(anim tokens `getin`, `incar`, `GetOutCar`; script `PutMFPlayerInCar`), with `InCarAction`,
`CarDoorAction`, and `ReleaseDoorsAction` handling the car side. The vast **`ActionButton::*`**
family (~20 classes: `GetInCar`, `OpenDoor`, `AutomaticDoor`, `Doorbell`, `PlayAnim`/`Loop`/
`Once`, `AutoPlayAnimInOut`, `ToggleAnim`, `ReverseAnim`, `AnimSwitch`, `EnterInterior`…) are the
context-button actions the world offers. On-foot movement is a **locomotion** system
(`ChangeLocomotion`, `PhysicsLocomotion`, `WalkerLocomotionAction`, `VehicleLocomotion`,
`TrafficLocomotion`) driven by animation sets (`locomotion4`, `locomotion8` — the *"animations
required for locomotion"* the engine warns about), played by **`AnimationPlayer`** /
`ActorAnimation` / `SimpleAnimationPlayer`.

---

## Deep-dive pages

- [C42.1 — The Action Model](01-action-model.md): actions as objects; `ActionController`, the `ActionButton::*` family.
- [C42.2 — Attacks: Kick, UFO & Wasps](02-attacks.md): `AttackBehaviour`, `KickAction`, `UFOAttackBehaviour`, wasp attacks.
- [C42.3 — Enter & Exit a Vehicle](03-enter-exit-car.md): the `GetIn → InCar → GetOut` state flow, doors, `PutMFPlayerInCar`.
- [C42.4 — Locomotion](04-locomotion.md): locomotion sets, rigs, `ChangeLocomotion`, the `locomotion4/8` animation counts.
- [C42.5 — The Animation Players](05-animation-players.md): `AnimationPlayer`, `ActorAnimation`, `PlayAnimationAction`, idle/hold.
- [C42.6 — Doors & World Actions](06-doors-world.md): `OpenDoor`, `AutomaticDoor`, `Doorbell`, `AnimSwitch`, `ToggleAnim`.
- [C42.7 — Modding Actions & Animations](07-modding.md): swapping/adding animations, retiming actions, custom `ActionButton`s.

---

## 42.1 The action model (✅ verified)

A character runs **actions** — discrete, typed behaviours. World objects expose
`ActionButton::*` context actions (the button prompt you get near a car/door). [C42.1](01-action-model.md).

## 42.2 Attacks (✅ verified)

`KickAction` is Homer's melee (`jump_kick`/`kickwave`; *"Kick Swaps Character Model"* — the model
briefly swaps for the kick pose). `AttackBehaviour` is the general attacker behaviour;
`UFOAttackBehaviour` and `Wasp_Attack`/`wasp_attack` (with `UFO_ATTACK_ALL`, `ATTACK_PLAYER`) are
the enemy variants. [C42.2](02-attacks.md).

## 42.3 Enter/exit vehicle (✅ verified)

Getting in/out is a state sequence: `CharacterAi::GetIn` (anim `getin`) → `CharacterAi::InCar`
(anim `incar`) → `CharacterAi::GetOut` (`GetOutCar`). `InCarAction`, `CarDoorAction`,
`ReleaseDoorsAction` and the script verb `PutMFPlayerInCar` handle the car/door side; the wrapping
fade is C40. [C42.3](03-enter-exit-car.md).

## 42.4 Locomotion (✅ verified)

On-foot motion uses **locomotion sets** — bundles of directional walk/run animations
(`locomotion4` = 4-direction, `locomotion8` = 8-direction). The engine asserts *"Locomotion
specified without rig"* and *"…animations required for locomotion"*, so a locomotion is
`rig + a required animation set`. `ChangeLocomotion` swaps sets. [C42.4](04-locomotion.md).

## 42.5 Animation players (✅ verified)

`AnimationPlayer` plays an animation on a rig; `ActorAnimation`/`SimpleAnimationPlayer` are
variants; `PlayAnimationAction`/`PlayIdleAnimationAction`/`HoldAnimationAction` are the action
wrappers. [C42.5](05-animation-players.md).

## 42.6 Doors & world actions (✅ verified)

`ActionButton::OpenDoor`, `AutomaticDoor`, `Doorbell`, `PlayAnim*`, `AutoPlayAnimInOut`,
`ToggleAnim`, `ReverseAnim`, `AnimSwitch` — the animated-prop actions the world offers.
[C42.6](06-doors-world.md).

## 42.7 Modding (✅ practical)

Swap/add animations, retime a kick or car-entry, or add a custom `ActionButton` via the confirmed
classes + hooks. [C42.7](07-modding.md).

---

## What this chapter established

- Character behaviour is an **action stack**: typed actions (incl. the `ActionButton::*` family),
  attacks (`KickAction`/`AttackBehaviour`), and vehicle entry/exit as an AI **state sequence**.
- On-foot motion is a **locomotion set** system (rig + required animations; 4/8-direction).
- Animation is played by `AnimationPlayer`/`ActorAnimation`, wrapped by play/idle/hold actions.

**Cross-references:** C40 (enter/exit fade), C24/C25 (vehicles/characters & AI), C34 (animation
channels — the keyframe substrate), C35 (vehicle physics), C32 (combat/health), C41 (entering
interiors on foot), C28.5/28.7 (hooking + vtables).
