# C33.5 — Sprites, Billboards & Effects

**What it is.** The 2-D-in-3-D rendering primitives (sprites and billboards) that draw flat images in the 3-D
world always facing the camera, plus the miscellaneous **effect** drivers — including one that isn't visual
at all: controller rumble.

**How it works — billboards & sprites (✅ verified).**

```
tBillboardQuad / tBillboardQuadGroup            — camera-facing quads (single / grouped)
tBillboardQuadGroupAnimationController          — animates a billboard group (C34)
tSprite / tSpriteLoader                         — a sprite (2-D image in the world)
FeSprite / Scrooby::Sprite                      — UI sprites (front-end, C21.3)
```

A **billboard** is a quad that always rotates to face the camera, so a flat image looks like it has presence
from any angle — used for coins (a spinning coin is often a billboard), glows, lens flares, distant trees,
and particles (C33.4, `tSpriteParticle` is a billboard particle). `tBillboardQuadGroup` batches many
billboards (a field of them) for efficiency, and `tBillboardQuadGroupAnimationController` animates them (C34).
**Sprites** (`tSprite`) are the general 2-D-image primitive; the UI variants (`FeSprite`, `Scrooby::Sprite`)
are the front-end's sprites (C21.3 — the 436 Scrooby sprites).

**How it works — effect drivers (✅ verified).**

```
tEffectController / tOpticEffect / ConstantEffect   — drive visual effects over time
RumbleEffect / WheelRumble                          — controller force-feedback (rumble)
SoundEffectPlayer                                   — one-shot sound effects (C19)
```

`tEffectController` drives time-varying effects; `tOpticEffect` is a visual/optical effect (a lens flare,
heat shimmer). Most tellingly, **`RumbleEffect`** and **`WheelRumble`** are "effects" that produce **no image
at all** — they drive the controller's **rumble motors**. This reveals that "effect" in the engine means *any
time-varying sensory feedback*, not just visual: a crash produces a visual spark effect (C33.4), a sound
effect (C19), *and* a rumble effect. `WheelRumble` specifically ties rumble to the wheels — you feel the road
through the controller.

**Why billboards.** On fixed-function hardware (C33.1), a full 3-D model for every small detail (a coin, a
glow, a distant tree) is wasteful — a camera-facing quad with a texture looks nearly as good for a fraction
of the cost. Billboards are the universal cheap trick for "3-D-ish detail": particles, pickups, glows, and
far-away objects are all quads that face you. The `tBillboardQuadGroup` batching makes fields of them (a
sparkle cloud, distant foliage) cheap. This is why so much of the world's small detail is billboards — it's
the right cost/quality trade for 2003 hardware.

**Rumble as an effect — the design insight.** That `RumbleEffect` lives alongside visual effects and sound
effects shows the engine models **feedback uniformly**: an event (a crash) fires a set of *effects* across
modalities — visual (particles), audio (sound effect), and haptic (rumble) — each an "effect" object driven
by an effect controller. This is elegant: the crash doesn't hardcode "spawn sparks, play sound, rumble
controller"; it fires effects, and the effect system routes each to its modality. It's the same event-driven,
component design as the rest of the engine (C23.3) — feedback is just another kind of effect.

**What happens if you bend it.**

- *Rely on a sprite/effect member offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Use a full model where a billboard would do* — costlier for no gain on small/distant detail. Prefer
  billboards.
- *Forget rumble is an "effect"* — disabling effects may also disable haptics. Rumble is `RumbleEffect`, part
  of the same system.

**Next:** [Chapter 34 — Animation Channels & Controllers](../C34-Animation-Channels/C34-Animation-Channels.md).
