# C35.3 — Jumps & Air Control

**What it is.** What happens when a car leaves the ground — off a ramp, a hill, or a big bump. The car enters
**`InAirEngineState`**, and the physics changes completely: no tyres on the road means no grip, no drive, and
gravity taking over. It's also the trigger for the jump camera effect (C36).

**How it works (✅ verified).**

```
InAirEngineState (0x0060A600)  — the airborne driving regime
```

The moment all wheels leave the ground, the vehicle transitions from `NormalEngineState` (or `SkidEngineState`)
to **`InAirEngineState`**. Airborne, the tyre-based forces vanish — there's nothing to grip, so:

- **No drive** — the throttle does nothing (no wheel contact to push against).
- **No steering** — the front wheels can't turn the car (no traction). Some arcade air-control (slight pitch/
  yaw influence) may remain for playability, but it's not tyre steering.
- **Gravity** pulls the car down (from `sim::SimEnvironment`, C35.4).
- **Rotation** carries over — the car keeps whatever spin it launched with, which is why hitting a ramp
  crooked sends you tumbling.
- **The weeble bias** (`SetWeebleOffset`, C15.4) works to right the car toward a wheels-down landing.

On landing, the wheels regain contact and the car transitions back to `NormalEngineState` (or `SkidEngineState`
if it lands sliding). A bad landing (nose-first, on its side) can flip it — which is why the weeble bias
(C15.4) matters.

**Why air is a distinct state.** Airborne physics is fundamentally different from grounded — no contact means
no tyre forces — so making it a separate `InAirEngineState` is the clean way to switch off grip/drive/steering
all at once. Trying to handle "in air" as a special case within normal driving would mean guarding every tyre
force with an "if grounded" check; a distinct state simply *doesn't apply* those forces. It also lets the
game *react* to the state transition: entering `InAirEngineState` is a clear event to trigger the jump camera
(C36), a "whee!" sound, and to start tracking air time (for stunt scoring). The state boundary is the hook.

**The camera tie (C36).** Going airborne is one of the game's signature camera moments: the camera pulls back
or shifts to emphasise the jump (a `WrecklessCam`-style dramatic angle, C36), and lands with a shake
(`SineCosShaker`, C36) on impact. This is exactly the "camera effect when a car jumps" the systems are built
for — the `InAirEngineState` transition drives it. The physics state and the camera effect are wired together:
enter air → jump camera; land → impact shake.

**Landing and damage.** A hard landing can damage the car (hit points, C15.5/C32.2) and, if it lands on a
breakable (C35.5) or another car, trigger those interactions. The landing is a collision (C26.6) resolved by
the `sim::` solver, so a big drop transfers real impact. This is why launching off the biggest ramps is both
thrilling (air time, camera) and risky (landing damage).

**What happens if you bend it.**

- *Rely on an `InAirEngineState` member offset* — class/vtable ✅, offset ⏳. Diff (C4.3).
- *Expect throttle/steering to work airborne* — they don't (no grip). Air control is limited by design.
- *Set `SetWeebleOffset` to 0 and launch big jumps* — the car won't self-right and will land badly (C15.4).
  Keep the weeble bias for playable jumps.
