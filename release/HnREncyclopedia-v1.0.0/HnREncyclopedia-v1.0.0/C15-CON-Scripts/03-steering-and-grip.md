# C15.3 — Steering & Grip

**What it is.** The commands that decide how a car turns, how much it holds the road, and how it behaves
once it starts to slide. This is the richest group in a `.con` and the one that most defines a car's
personality. Present in 90/90 (the no-e-brake slip pair in 86); values ✅, effects 🟡 from the names.

**The gripping-drive commands.**

- **`SetTireGrip(x)`** — the master traction number. Ambulance `2.5`. Higher grip resists sliding and
  tightens cornering; lower grip makes a car loose and drifty. The single most impactful handling knob
  after mass and top speed.
- **`SetMaxWheelTurnAngle(deg)`** — how far the front wheels can turn. Ambulance `25.0`. Sets the tightest
  possible turn radius at low speed.
- **`SetNormalSteering(x)`** — the steering *rate*/authority while gripping. Ambulance `90.0`.
- **`SetHighSpeedSteeringDrop(x)`** — how much steering authority falls off as speed rises. Ambulance
  `0.267`. This is what stops fast cars from flipping on a flick of the stick — steering softens the
  faster you go.

**The slide model.** SHAR models "gripping" and "sliding" as distinct regimes, and the slide has its own
full set of knobs — this duplication is deliberate and is what makes the game's handbrake-slides feel
good:

- **`SetSlipSteering(x)`** — steering rate while sliding. Ambulance `55.0` (note: lower than the gripping
  `90.0` — you steer *less* sharply mid-slide).
- **`SetEBrakeEffect(x)`** — how strongly the handbrake breaks traction. Ambulance `0.3`.
- **`SetSlipSteeringNoEBrake(x)`** and **`SetSlipEffectNoEBrake(x)`** — the slide model when you're sliding
  *without* pulling the handbrake (e.g. from sheer speed). Ambulance `50.0` / `0.14`. Splitting
  e-brake-slides from natural slides lets designers make the handbrake feel special without making every
  high-speed corner uncontrollable.

**Why it's built this way — two regimes, two parameter sets.** Rather than a continuous tyre-slip curve,
SHAR flips between grip and slide and gives each its own steering and effect values. That is more knobs,
but it hands designers direct control of the exact moment and feel of a slide — the game's signature
move. The `NoEBrake` variants exist because a slide you *asked for* (handbrake) and a slide you *fell
into* (speed) should feel different, and the only way to guarantee that with a regime model is to
parameterise them separately.

**Reading the Ambulance's steering personality.** `grip 2.5`, `maxTurn 25°`, `normalSteer 90`,
`highSpeedDrop 0.267`, `slipSteer 55`, `eBrake 0.3` describes a vehicle that turns adequately at low
speed, tightens up under grip, softens noticeably at speed, and — when it slides — becomes distinctly
less responsive. That is a heavy AI truck that discourages aggressive driving, exactly as intended.

**What happens if you bend it.**

- *Raise `SetTireGrip` too high* — the car turns on rails, never slides, and can feel it's "stuck to the
  road"; the game's slides stop working. Tune grip against the slip values, not alone.
- *Set `SetHighSpeedSteeringDrop` to 0* — full steering authority at top speed; the car becomes a
  spin-out machine at speed. The drop is a safety feature; lower it only for deliberately twitchy cars.
- *Make `SetSlipSteering` ≥ `SetNormalSteering`* — you steer *more* sharply while sliding than while
  gripping, which feels wrong and makes slides snap. Keep slip steering below normal unless chasing an
  arcade drift feel.
