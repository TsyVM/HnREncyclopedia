# C17.2 — The Animation Engine: Banks, Blends & Transitions

**What it is.** The core of `choreo::` — the system that stores animation clips in **banks**, plays them
through **drivers**, **blends** between them, and runs **transitions**. It's the runtime of the `.cho`
state→clip map (C8.2), and it's a genuine, layered animation engine.

**How it works (✅ verified).** The verified class families from `shar_dumps.csv`:

```
choreo::Engine                                   — runs the whole system each frame
choreo::Bank / MultiBank : choreo::BaseBank      — collections of animation clips (the C8.2 clips)
choreo::Animation / AnimationDriver / AnimationFrame  — a playing clip and its per-frame pose
choreo::Blend / BlendDriver / BlendSlot / BlendPhase  — blending multiple clips together
choreo::Transition : choreo::Animation           — a transition between clips (the C8.2 state changes)
choreo::Puppet ── driven by ──► Driver (Animation/Blend/Locomotion/Replay/Root)
```

The pattern is a **driver stack**: a `choreo::Puppet` (C17.1) is posed each frame by one or more **drivers**.
An `AnimationDriver` plays a single clip; a `BlendDriver` mixes several (a `BlendSlot` per input); a
`Transition` (which *is* an `Animation`) smoothly moves from one clip to the next. The `choreo::Engine` runs
the drivers, blends their outputs, and produces the puppet's final pose. This is the runtime of the `.cho`
state→clip map (C8.2): a state request selects a clip from a **bank**, and the engine blends from the current
clip to it via a transition.

**Why banks, blends, and transitions.** Three separate concerns, three mechanisms:

- **Banks** solve *storage and selection* — a character has dozens of clips (idles, walks, per-costume
  variants, C8.2), organised in banks the engine selects from by name.
- **Blends** solve *smoothness across simultaneous animations* — walking while turning, or an upper-body
  gesture over a lower-body walk (C17.3). A `BlendDriver` with multiple `BlendSlot`s mixes them by weight.
- **Transitions** solve *smoothness across sequential animations* — you don't snap from idle to walk, you
  blend over a few frames. A `choreo::Transition` is exactly that timed cross-fade.

Together they turn a library of discrete clips (C8.2) into continuous, natural motion — the difference
between a character that snaps between poses and one that moves believably.

**The replay system.** `choreo::Replay`/`ReplayBuffer`/`ReplayDriver` record and play back motion — used for
things like a character repeating a captured performance, or the game replaying an action. It's another
*driver* type in the same stack: a `ReplayDriver` poses the puppet from a `ReplayBuffer` instead of a live
clip. This shows the driver architecture's flexibility — any source of poses (clip, blend, replay,
locomotion, C17.3) is just another driver.

**What happens if you bend it.**

- *Request a clip not in any loaded bank* — the driver has nothing to play; the character freezes (C8.2).
  Ensure the clip is in a bank.
- *Blend clips on incompatible rigs* — poses don't combine sensibly. Blend clips authored for the same rig.
- *Snap instead of transition* — skipping the `Transition` makes motion pop. Use transitions between states.
