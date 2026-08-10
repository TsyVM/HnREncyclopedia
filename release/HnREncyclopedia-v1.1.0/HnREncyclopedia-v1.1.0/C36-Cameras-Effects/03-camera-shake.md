# C36.3 — Camera Shake: `SineCosShaker`

**What it is.** The camera *jolt* — the shake you feel when you land a big jump, crash into something, or
smash through a window. It's a dedicated class, **`SineCosShaker`**, that perturbs the camera with a decaying
oscillation. This is the single most important "camera effect" the game has.

**How it works (✅ verified).** **`SineCosShaker`** (0x00614FC0) shakes the camera by adding a time-varying
**sine/cosine** displacement to its position and/or rotation:

```
offset(t) = amplitude · e^(−decay·t) · (sin(freq·t), cos(freq·t), …)
```

The name says the method: it drives the shake with **sine and cosine** functions of time, so the camera
wobbles smoothly (not randomly), and an **exponential decay** shrinks the amplitude over the shake's
lifetime — a sharp initial jolt that oscillates and settles back to still. The **amplitude** sets how violent
the shake is (a small bump vs. a big crash), the **frequency** how fast it wobbles, and the **decay** how
quickly it calms. So a hard landing is a big-amplitude, fast-decaying shake; a rumble strip is a small,
sustained one.

**Why sine/cosine + decay.** It's the classic, cheap, good-looking camera-shake recipe. **Sine/cosine** gives
*smooth* oscillation — the camera sways rather than jitters randomly, which reads as a physical shudder, not
noise. **Exponential decay** gives the natural "hit hard, settle down" envelope of a real impact — a struck
object vibrates most at first and calms exponentially. Two parameters (amplitude, frequency) plus a decay
capture the whole feel of an impact, and the math is trivial to compute per frame. This is far better than a
random-jitter shake (which looks like static) and far cheaper than simulating the camera as a physical
object. It's the right tool, and SHAR uses it directly (the class is literally named for its method).

**What triggers it.** The shake is fired by impact *events* (C36.4): landing from a jump (`InAirEngineState`
→ ground, C35.3), a car crash (a hard collision, C26.6), smashing a `BreakableObjectDSG` (glass, C35.5), an
explosion. Each fires a `SineCosShaker` with an amplitude scaled to the impact's force — a gentle bump is a
small shake, a head-on crash a big one. This is what makes collisions *felt*: without the shake, a crash is
just the car stopping; with it, the whole view shudders, selling the impact.

**Part of the multi-modal impact.** The camera shake is one channel of the game's impact feedback (C33.5): a
crash fires a **visual** shake (`SineCosShaker`), **debris** particles (C33.4), a **sound** (C19), and
controller **rumble** (`RumbleEffect`, C33.5) — all from the one impact event. The shake is the *camera's*
share of that feedback. This event-fires-effects-across-modalities design (C33.5) is why big impacts hit so
hard: everything reacts at once, and the camera shake is the most visceral part.

**What happens if you bend it.**

- *Rely on a `SineCosShaker` member offset* — class/vtable ✅, offset ⏳. Diff (C4.3).
- *Over-shake* (huge amplitude, slow decay) — the camera becomes nauseating and you lose sight of the action.
  Scale amplitude to impact and decay quickly.
- *Expect random-jitter shake* — it's smooth sine/cosine, by design. Don't replace it with noise.
