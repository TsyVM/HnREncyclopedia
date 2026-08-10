# C35.2 — Drifting & Skidmarks

**What it is.** The slide — SHAR's signature handbrake drift — is the **`SkidEngineState`**, and its visible
trace is the **`Skidmark`**. This page connects the drift you feel to the `.con` slip parameters (C15.3) that
tune it and the marks it leaves.

**How it works (✅ verified).**

```
SkidEngineState (0x0060A5B8)  — the sliding/drifting driving regime
Skidmark        (0x00607730)  — the black tyre marks laid on the road while skidding
```

A car enters **`SkidEngineState`** when its tyres break traction — pulling the handbrake, cornering hard
past the grip limit, or launching (a burnout). While in this state, the car *slides*: it keeps momentum in
its old direction while the front wheels point elsewhere, steering by the **slip model** rather than the grip
model. The slip model is exactly the `.con` parameters of C15.3:

- `SetSlipSteering` — how sharply you steer *while sliding* (usually less than gripping, C15.3).
- `SetEBrakeEffect` — how strongly the handbrake breaks traction (triggers the skid).
- `SetSlipSteeringNoEBrake` / `SetSlipEffectNoEBrake` — the slide when you're sliding *without* the handbrake
  (from sheer speed).
- `SetSlipGasScale` — drive force while sliding (C15.2).

So `SkidEngineState` *is* the runtime of the CON slip model: those params configure this state. As it slides,
the car lays **`Skidmark`s** — the black marks on the road that visually confirm the drift.

**Why drifting is its own state.** A drift is physically a different regime — the car is moving one way while
pointed another, with the tyres sliding rather than rolling. Modelling this as a distinct `SkidEngineState`
(separate from `NormalEngineState`) lets the physics switch cleanly between "grippy, precise" and "loose,
sliding" driving, and lets designers tune each independently (C15.3). It's what makes SHAR's handbrake slides
feel *deliberate and controllable* — you enter the skid state on command (handbrake), it behaves by its own
tuned rules, and you exit it (regain grip) when you straighten out. Without a separate state, drifting would
be an awkward special case of normal driving; as a state, it's a first-class driving mode.

**Skidmarks as decals.** A `Skidmark` is a **decal** — a mark drawn on the road surface where the sliding
tyre touched. It's rendered as geometry laid on the ground (a strip of dark quads following the tyre path),
persisting for a while then fading. Skidmarks are pure *feedback* — they don't affect physics — but they
make the drift *readable*: you see where you slid, which is satisfying and communicates the car's behaviour.
They're the visual counterpart to the tyre-screech sound (C19.2) the skid also produces.

**Reading a car's drift character.** From the `.con` (C15.3): a car with low `SetTireGrip` and high
`SetEBrakeEffect` slides easily and dramatically (a drift machine); high grip and low e-brake effect resists
sliding (a planted car). The `SkidEngineState` is the same for both; the `.con` params make one drifty and
one grippy. So "tuning drift" is tuning the C15.3 slip params — a safe, verified data edit.

**What happens if you bend it.**

- *Rely on a `SkidEngineState`/`Skidmark` member offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Tune grip without the slip params* — you change when the car *enters* skid but not how it *behaves*
  sliding. Tune both (C15.3).
- *Expect skidmarks to affect handling* — they're visual decals, not physics. The slide is the state; the
  marks are feedback.
