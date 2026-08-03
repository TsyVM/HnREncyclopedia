# C35.1 — The Engine State Machine

**What it is.** The heart of how a car drives: a finite state machine of **engine states**, each a distinct
driving regime with its own physics. It's why idling, cruising, drifting, and flying all feel different — the
car is literally in different states.

**How it works (✅ verified).** The verified engine-state family:

```
IdleEngineState     (0x0060A5D0)  — stopped or idling
NormalEngineState   (0x0060A5A0)  — driving with grip
SkidEngineState     (0x0060A5B8)  — sliding/drifting (broken traction, C35.2)
InAirEngineState    (0x0060A600)  — airborne (a jump, C35.3)
ReverseEngineState  (0x0060A5E8)  — reversing
UpshiftEngineState  (0x0060A588)  — shifting up a gear
DownshiftEngineState(0x0060A570)  — shifting down a gear
```

A vehicle is always in exactly one engine state. Transitions follow the driving inputs and world: from
`Normal`, brake+turn hard (or handbrake) → `Skid`; hit a ramp → `InAir`; land and regain grip → `Normal`;
select reverse → `Reverse`; cross a speed/RPM threshold → `Up`/`DownshiftEngineState` briefly, then back to
`Normal`. Each state applies *its own* physics: `Normal` uses the grip model (tyre traction, C15.3);
`Skid` uses the slip model (sliding, C35.2); `InAir` removes tyre forces entirely (C35.3).

**Why a state machine for driving.** Driving has distinct *modes* that obey different rules — a car with grip
behaves nothing like one that's sliding or airborne — and a state machine captures exactly that: one active
mode, clean transitions, mode-specific physics. This is the same FSM pattern as the character AI (C25.2), the
camera switcher (C26.4), and the top-level GameFlow (C30.1). Rather than one tangled physics function full of
`if drifting… if airborne…` branches, each regime is its own state class with its own update, and the machine
switches between them. It makes the physics both correct (you can't be gripping and sliding at once) and
tunable (each state reads the relevant `.con` params, C15).

**The tie to the CON parameters (C15).** The `.con` handling values (C15) are the *tuning* for these states:
`SetTireGrip`/`SetNormalSteering` tune `NormalEngineState`; the slip params (`SetSlipSteering`,
`SetEBrakeEffect`, `SetSlipGasScale`, C15.3) tune `SkidEngineState`; `SetWeebleOffset` (C15.4) helps
`InAirEngineState` land upright. So a car's *personality* (C15) is really "how do its engine states behave" —
the same state machine, different numbers per car. This is why the Ambulance (heavy, gripping) and a sports
car (loose, drifty) feel different: same states, different `.con` tuning of them.

**Gears — a light touch.** `Upshift`/`DownshiftEngineState` are brief transition states for gear changes,
producing the shift sound and a momentary drive change. SHAR's gearing is arcade-simple (automatic, felt more
than managed) — the gear states exist to *animate* the shift (sound, a beat of reduced drive) rather than
model a manual gearbox. This fits the arcade physics: gears are flavour, not a mechanic you control.

**What happens if you bend it.**

- *Rely on an engine-state member offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Expect one physics rule for all driving* — it's mode-specific (grip vs. slip vs. air). Reason per state.
- *Tune `.con` params expecting a global effect* — each param feeds a specific state (C15.3 params feed
  `SkidEngineState`). Know which state a param configures.
