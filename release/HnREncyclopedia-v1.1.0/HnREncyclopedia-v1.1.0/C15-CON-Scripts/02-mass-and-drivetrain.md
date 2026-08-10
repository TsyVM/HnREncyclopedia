# C15.2 — Mass & Drivetrain

**What it is.** The commands that decide how heavy a car is and how it converts throttle and brake into
motion — the core of straight-line feel. All are ✅ present in 90/90 vehicles (except the two high-speed
refinements); their *values* are verified from the files, their *effects* are 🟡 reasoned from the
command names and a standard arcade-physics reading.

**The commands.**

- **`SetMass(kg)`** — vehicle mass. Verified range spans light cars to the Ambulance's `2500.0`. Mass
  feeds every force interaction: acceleration for a given drive force, momentum in collisions (C11/C26),
  and how hard the suspension (C15.4) is loaded. Heavier ⇒ more stable, slower to accelerate, harder
  hitting.
- **`SetTopSpeedKmh(kmh)`** — the speed cap. Ambulance `130.0`. This is the governed maximum; the drive
  model accelerates toward it and holds. It is a *target*, not merely a display number — cross-checking a
  car's on-road top speed against this value is a clean verification (C4.3).
- **`SetGasScale(x)`** — throttle-to-drive-force multiplier while gripping. Ambulance `5.0`. The primary
  acceleration knob.
- **`SetSlipGasScale(x)`** — the same, but while the tyres are sliding. Ambulance `6.0`. Separating grip
  and slip lets a car keep (or lose) drive when it breaks traction — the heart of the arcade slide feel.
- **`SetBrakeScale(x)`** — brake force multiplier. Ambulance `6.0`.
- **`SetHighSpeedGasScale(x)`** and **`SetGasScaleSpeedThreshold(kmh)`** — a two-part refinement (only 17
  cars) that changes throttle response above a threshold speed, shaping the top of the acceleration curve
  so fast cars don't feel identical to slow ones near their cap. (🟡 — inferred from the names and their
  paired use.)

**Why it's built this way — grip vs. slip scales.** The defining choice here is the *pair* of gas scales.
A realistic sim derives drive from a tyre model; SHAR instead exposes two explicit multipliers — one for
grip, one for slip — so designers can dial the exact feel of losing and regaining traction per car
without touching a physics model. It is the arcade shortcut that makes a garbage truck and a sports car
feel distinct with four numbers.

**Reading a car's character from these five numbers.** The Ambulance (`mass 2500`, `top 130`, `gas 5`,
`slipGas 6`, `brake 6`) reads as a heavy, moderate-top-speed traffic vehicle that keeps drive when
sliding — exactly a lumbering AI truck. Contrast that mental model with a light, high-`SetTopSpeedKmh`
player car and you can predict handling before you drive it. That predictive reading is the practical
payoff of understanding the drivetrain block.

**What happens if you bend it.**

- *Raise `SetTopSpeedKmh` without raising `SetGasScale`* — the car aims higher but accelerates to it
  slowly; it may never reach the new cap in a short street. Tune the pair together.
- *Set `SetMass` very low* — the car becomes twitchy and gets thrown by collisions (C26); very high and it
  won't accelerate or turn. Mass is the multiplier under everything; change it in small steps and re-test.
- *Diverge `SetSlipGasScale` far below `SetGasScale`* — the car dies the instant it slides, feeling
  "sticky-then-dead." Keep the two within a sensible ratio unless that lurch is the effect you want.
