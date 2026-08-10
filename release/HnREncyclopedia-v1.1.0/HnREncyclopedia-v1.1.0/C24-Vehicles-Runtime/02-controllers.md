# C24.2 — Controllers: Human vs. AI

**What it is.** The hierarchy that decides *who drives* a `Vehicle`. Driving is deliberately factored out of
the car and into a **controller**, so one vehicle type serves the player, the AI, and traffic depending only
on which controller is attached.

**How it works (✅ verified).** From `shar_dumps.csv`:

```
VehicleController                 (base — 6 classes derive from it)
  ├ HumanVehicleController        — reads player input, drives the car
  └ AiVehicleController           — drives from AI decisions
        └ VehicleAI               — the full AI driver
```

A `Vehicle` (C24.1) holds a `VehicleController`. When the player is in the car, it's a
`HumanVehicleController` translating stick/pedal input into the handling model; when the AI drives (traffic,
chase cars, mission vehicles), it's an `AiVehicleController`/`VehicleAI` translating navigation decisions
(follow the road graph, C13; chase the player) into the *same* handling model. The car doesn't change — only
the controller.

**Why separate the driver from the car.** This is the strategy pattern applied to driving, and it buys three
things. First, **one car, many drivers**: the same `.con`-tuned handling (C15) feels consistent whether you
or the AI drives, because both go through the same `Vehicle`. Second, **hand-off**: `getin`/`getout`
objectives (C16.3) and `SummonVehiclePhone` (in the RTTI set) swap the controller as the player enters or
leaves — the car keeps its state, the driver changes. Third, **traffic vs. player**: `LoadDisposableCar(…,
"AI")` (C14.2) attaches an AI controller so a spawned car drives itself. All of this is one seam — the
controller slot on the `Vehicle`.

**The AI's inputs.** An `AiVehicleController` drives from the road network (C13.2) — following lanes,
turning at intersections — and from higher-level goals (chase, flee, patrol) set by the character AI (C25).
So the road graph you decoded in C13 is *consumed here*: the AI controller reads it to produce steering and
throttle, which the `Vehicle`'s handling model turns into motion. The fence data (C13.1) and physics (C26)
then keep the car on the road.

**What happens if you bend it.**

- *Assume the player and AI drive different car objects* — they drive the same `Vehicle` via different
  controllers. To change handling for both, edit the `.con` (C15); to change only AI behaviour, target the
  AI controller.
- *Rely on a controller member offset* — the classes are ✅, the offsets ⏳. Diff (C4.3).
- *Remove a controller expecting the car to stop* — a car with no controller is undriven, not parked; use
  `SuppressDriver` (C12.5) for empty cars.
