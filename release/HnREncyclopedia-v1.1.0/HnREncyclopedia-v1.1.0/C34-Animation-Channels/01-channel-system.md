# C34.1 — The Channel System

**What it is.** The atom of all animation in the game: a **channel** — a keyframed stream of one typed value,
sampled by time to produce its current value. Every animated thing, from a blinking eye to a moving camera,
is built from channels.

**How it works (✅ verified).** `tChannel` is the base. A channel stores a value at a set of **keyframe
times** and, when asked for the value at the *current* time, **interpolates** between the surrounding
keyframes. That's the whole idea:

```
channel: [ (t0, v0), (t1, v1), (t2, v2), … ]      keyframes
sample(t): find the keyframes around t, interpolate → current value
```

To animate a joint's rotation, you store its rotation at a few keyframe times and interpolate between them
each frame — smooth motion from a handful of key poses. To animate a light's brightness, a float channel of
brightness values. To scroll a texture, a channel of UV offsets. The channel doesn't know *what* it animates —
it just produces a value over time; the **controller** (C34.4) decides where that value goes.

**Why keyframes + interpolation.** It's the universal animation technique: store *key* values sparsely (an
animator sets a few poses), and *compute* the in-between values by interpolation. This is vastly cheaper than
storing every value at every frame — a 5-second animation at 30fps is 150 frames, but might have only a dozen
keyframes, the rest interpolated. It's also how animation is *authored* — animators think in key poses, not
per-frame values. The channel is the runtime form of that: the keys the animator set, plus the interpolation
that fills the gaps.

**Why "channel."** The name comes from the idea of a single *stream* (channel) of one value — like an audio
channel carries one signal. A character's animation isn't one channel; it's *many* — one per joint (rotation),
plus root motion, plus event triggers. Bundling the channels for one animation is a "clip" or "bank" (C17.2).
So the hierarchy is: **channel** (one value over time) → **animation/clip** (many channels — a full pose over
time) → **bank** (many clips, C17.2). The channel is the bottom, and this chapter is about that bottom layer
that C8 and C17 build on.

**The sampling is the frame's animation work.** Each frame, for every animated thing, the engine samples its
channels at the current time. A character with 30 joints animating is 30 quaternion channels sampled per
frame; the blended result (C17.2) poses the skeleton (C8), which deforms the mesh (C8.3). Multiply across
every animated character, light, camera, and effect, and channel sampling is a significant part of the frame —
which is why rotation, the bulk of it, gets a *compressed* channel (C34.3) to keep the data small and the
sampling fast.

**What happens if you bend it.**

- *Rely on a `tChannel` member offset* — class/vtable ✅, offset ⏳. Diff (C4.3).
- *Store per-frame values instead of keyframes* — you bloat the data and lose the authoring model. Keyframe
  and interpolate.
- *Sample with the wrong interpolation for the type* — a quaternion linearly interpolated (not slerped)
  wobbles; a bool interpolated is nonsense. Use the typed channel (C34.2).
