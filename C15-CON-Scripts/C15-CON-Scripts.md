# Chapter 15 — CON Vehicle & Config Scripts

> **Goal of this chapter:** read and confidently edit any vehicle's handling. After this chapter you can
> open a `.con`, understand every `Set…` call it contains, change how a car drives, and know which value
> maps to which behaviour on the road.

Every drivable and traffic vehicle in *The Simpsons: Hit & Run* is tuned by a plain-text `.con` script in
`scripts/cars/`. There are **255 `.con` files**, and **90 of them are full vehicle definitions** (the
count of `SetMass` across the tree is exactly 90 — ✅ verified). A `.con` is the simplest format in the
whole game: a flat sequence of `SetName(args);` calls and `//` comments, no blocks, no control flow. That
simplicity is a gift to modders — the entire handling model of the game is exposed as a few dozen legible
numbers per car.

This chapter is fully grounded: every command below was extracted from the 255 shipped `.con` files and
its call-count verified, so the vocabulary here is the *complete* set the retail cars use, not a sample.

---

## Deep-dive pages

- [C15.1 — The CON Language](01-the-con-language.md): syntax, comments, argument types, and the flat execution model.
- [C15.2 — Mass & Drivetrain](02-mass-and-drivetrain.md): `SetMass`, `SetTopSpeedKmh`, the gas/brake scales.
- [C15.3 — Steering & Grip](03-steering-and-grip.md): steering angles, the slip model, e-brake, and `SetTireGrip`.
- [C15.4 — Suspension & Balance](04-suspension-and-balance.md): spring/damper, centre of mass, and the "weeble" offset.
- [C15.5 — Abilities & Special Moves](05-abilities-and-special.md): hit points, burnout, donut, wheelie, gambling odds.
- [C15.6 — Visual, Meta & the Runtime Bridge](06-visual-meta-runtime.md): doors, drivers, shadows, scale, and how a `.con` value reaches the live `Vehicle` (C24).

---

## 15.1 The language in one paragraph

A `.con` is executed top to bottom as a list of setter calls against the vehicle currently being built:

```c
// Ambulance (Traffic AI)
SetMass(2500.0);
SetTopSpeedKmh(130.0);
SetTireGrip(2.5);
SetCMOffsetZ(0.6);
SetHitPoints(3.0);
```

Arguments are floats (occasionally an int flag or a string), statements end in `;`, and `//` starts a
comment to end of line. There are **no** blocks, conditionals, or loops — a fact verified by extraction:
every non-comment line across all 255 files is a `Set…(…)` call (the only capitalised non-`Set` tokens in
the corpus are words inside comments, like "Truck" in `// Fish Truck`). [C15.1](01-the-con-language.md).

## 15.2 The complete command set (✅ verified counts)

Extracted and counted across `scripts/cars/*.con`, the handling vocabulary is:

| Command | Cars using | Governs |
|---|---:|---|
| `SetMass` | 90 | vehicle mass (kg) |
| `SetTopSpeedKmh` | 90 | top speed |
| `SetTireGrip` | 90 | lateral/longitudinal grip |
| `SetGasScale` / `SetSlipGasScale` | 90 | acceleration, normal vs. sliding |
| `SetBrakeScale` | 90 | braking force |
| `SetMaxWheelTurnAngle` | 90 | max steering angle |
| `SetHighSpeedSteeringDrop` | 90 | steering reduction at speed |
| `SetNormalSteering` / `SetSlipSteering` | 90 | steering rates, gripping vs. sliding |
| `SetEBrakeEffect` | 90 | handbrake strength |
| `SetSlipSteeringNoEBrake` / `SetSlipEffectNoEBrake` | 86 | slide model without handbrake |
| `SetCMOffsetX/Y/Z` | 90 | centre-of-mass offset |
| `SetSuspensionLimit` / `SetSpringK` / `SetDamperC` | 90 | suspension travel, spring, damper |
| `SetSuspensionYOffset` | 79 | ride height |
| `SetWeebleOffset` | 83 | self-righting bias |
| `SetHitPoints` | 89 | damage before destruction |
| `SetBurnoutRange` / `SetMaxSpeedBurstTime` | 87 | burnout/launch |
| `SetDonutTorque` | 87 | donut-spin torque |
| `SetWheelieRange` / `SetWheelieOffsetY/Z` | 86 | wheelie behaviour |
| `SetGamblingOdds` | 87 | wager payout for this car |
| `SetCharactersVisible` | 88 | show driver/passengers |
| `SetHasDoors` | 55 | doors present |
| `SetDriver` | 55 | assigned driver character |
| `SetShadowAdjustments` | 85 | blob-shadow shape (8 params) |
| `SetShininess` | 33 | specular |
| `SetCharacterScale` | 30 | occupant scale |
| `SetHighRoof` / `SetHighSpeedGasScale` / `SetGasScaleSpeedThreshold` / `SetIrisTransition` / `SetAllowSeatSlide` | 4–36 | assorted flags |

Every one of these is documented in the pages that follow, grouped by what it does to the car.

---

## Key takeaways

- A `.con` is a **flat list of `Set…(args);` calls** plus comments — no control flow. 255 files, 90 full
  vehicles (✅ verified).
- The handling model is fully exposed as ~30 numbers per car: mass, drivetrain, steering/slip, grip,
  suspension, centre of mass, and special abilities.
- Editing is the safest kind of mod: change a number, save — no size tree, no repack (contrast C1.5).
- Where each value lands in the live `Vehicle` object is the runtime bridge of [C24](../C24-Vehicles-Runtime/C24-Vehicles-Runtime.md)
  (class names ✅ from RTTI; member offsets ⏳).

**Next:** [Chapter 16 — Mission Structure & Objectives](../C16-Missions-Objectives/C16-Missions-Objectives.md).
