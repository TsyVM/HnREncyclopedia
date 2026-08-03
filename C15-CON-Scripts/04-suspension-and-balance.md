# C15.4 — Suspension & Balance

**What it is.** The commands that place the car's mass and connect its body to its wheels — centre of
mass, spring/damper, ride height, and the self-righting "weeble" bias. These decide how a car leans,
bounces, lands, and whether it tips over. Present in 79–90/90; values ✅, effects 🟡.

**Centre of mass.**

- **`SetCMOffsetX(m)` / `SetCMOffsetY(m)` / `SetCMOffsetZ(m)`** — the centre of mass relative to the model
  origin, as three separate calls forming a vector. Ambulance `(0.0, -0.1, 0.6)`. This is the pivot
  everything rotates around: move it forward/back (Z) to bias understeer/oversteer, down (Y negative) to
  lower the effective roll centre and resist tipping, sideways (X) only for deliberately lopsided
  vehicles. It is the most physically meaningful trio in the file.

**Suspension.**

- **`SetSpringK(x)`** — spring stiffness. Ambulance `0.5`. Higher ⇒ firmer, less body roll, harsher
  landings.
- **`SetDamperC(x)`** — damping. Ambulance `0.25`. Controls how quickly oscillation settles; too low and
  the car wallows, too high and it feels rigid.
- **`SetSuspensionLimit(m)`** — maximum travel. Ambulance `0.55`. How far the wheels can move before
  bottoming out.
- **`SetSuspensionYOffset(m)`** — ride-height offset (79 cars). Raises or lowers the body on its
  suspension.

**Balance.**

- **`SetWeebleOffset(x)`** — the self-righting bias (83 cars). Ambulance `-0.6`. Named for the "weebles
  wobble but they don't fall down" toy: it biases the car back toward upright, so an arcade car recovers
  from a lean instead of tipping. This is a pure game-feel parameter with no real-world analogue — it
  exists so players don't spend the game on their roof.

**Why it's built this way.** A real suspension sim would derive roll and pitch from geometry and load;
SHAR exposes the *outcomes* directly — one spring number, one damper number, one travel limit, a mass
point, and a righting bias. Five to six numbers replace a whole subsystem. The `WeebleOffset` in
particular is the giveaway that this is arcade physics tuned for *fun*, not fidelity: it actively fights
the physics to keep the car playable.

**Reading the Ambulance's stance.** `CM (0, -0.1, 0.6)` (mass low and toward the front), `spring 0.5`,
`damper 0.25`, `travel 0.55`, `weeble -0.6` describes a front-heavy, softly-sprung, well-damped, strongly
self-righting truck — stable, planted, slow to roll, forgiving. Every one of those adjectives is a
consequence you can predict from the numbers.

**What happens if you bend it.**

- *Raise the centre of mass (`SetCMOffsetY` toward 0 or positive)* — the car rolls and tips far more
  easily; combined with high grip it can flip in hard corners. Lower is safer.
- *Drop `SetDamperC` to near 0* — the car wallows and bounces after every bump and landing, never
  settling. Keep damping in proportion to spring stiffness.
- *Zero out `SetWeebleOffset`* — the car loses its self-righting help and will happily end up on its roof.
  Only remove the weeble bias if you *want* a tippy, punishing vehicle.
