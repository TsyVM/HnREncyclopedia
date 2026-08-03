# C15.5 — Abilities & Special Moves

**What it is.** The commands behind a car's durability and its stunt repertoire — the burnout, donut,
wheelie, and the wager odds — plus how much punishment it takes. These are what make SHAR's cars *toys*,
not just vehicles. Present in 86–89/90; values ✅, effects 🟡 from the names.

**Durability.**

- **`SetHitPoints(x)`** — damage the car absorbs before it's wrecked (89 cars). Ambulance `3.0`. Low for
  fragile traffic, higher for mission cars meant to survive a chase (C16). This ties directly to the
  damage model at runtime (C26).

**Launch & stunts.**

- **`SetBurnoutRange(x)`** — the throttle/grip window in which a stationary launch spins the wheels
  (burnout). Ambulance `0.08`. Small window ⇒ hard to trigger.
- **`SetMaxSpeedBurstTime(s)`** — how long a launch burst lasts. Ambulance `1.0`.
- **`SetDonutTorque(x)`** — the rotational torque available for donut spins (handbrake + throttle on the
  spot). Ambulance `2.0`. Higher ⇒ tighter, faster donuts.
- **`SetWheelieRange(x)` / `SetWheelieOffsetY(x)` / `SetWheelieOffsetZ(x)`** — whether and how the car pops
  a wheelie under hard acceleration, and where the pivot sits. Ambulance `range 0.15`, offsets `(0.0,
  -0.5)`.

**Wager.**

- **`SetGamblingOdds(x)`** — the payout multiplier when this car is used in a wager/bet event (87 cars).
  Ambulance `3.0`. A pure gameplay-economy value attached to the vehicle, showing how tightly SHAR welds
  driving to its mission and reward systems (C16).

**Why it's built this way.** These commands encode *identity*, not physics. A garbage truck that can pull
a donut and pop a wheelie is a comedy object first and a vehicle second, and SHAR makes that explicit by
giving every car — even traffic — a full stunt parameter set. Putting `SetGamblingOdds` in the same file
as `SetSpringK` is the clearest sign that in this engine a "vehicle" is a bundle of *gameplay*
properties, of which physics is only one part.

**Reading the Ambulance's kit.** `hp 3`, `burnout 0.08`, `donut 2.0`, `wheelie 0.15`, `odds 3.0`: fragile,
hard to burnout, capable of a modest donut and a small wheelie, worth 3× in a wager. A believable AI
truck that still obeys the game's toy-physics rules.

**What happens if you bend it.**

- *Set `SetHitPoints` very high on a traffic car* — it stops being destructible, which can break gags and
  missions that expect it to wreck (C16). Match durability to the car's role.
- *Crank `SetDonutTorque`* — the car spins violently and can become uncontrollable in tight spaces; fun,
  but test it in the world it's used in.
- *Change `SetGamblingOdds` without balancing* — you alter the mission economy for any event that wagers
  that car. Treat it as a gameplay-balance value, not a handling one.
