# Chapter 34 — Animation Channels & Controllers

> **Goal of this chapter:** decode the low-level substrate under *all* animation — the **channel** system.
> Every animated value in the game (a joint's rotation, a light's colour, a camera's position, a scrolling
> texture) is a keyframed **channel**, driven onto its target by a **controller**. This is the backend of
> C8, C17, and C33.

Whenever anything in SHAR *changes over time* — a character's pose (C8/C17), a light flickering (C33.2), a
billboard pulsing (C33.5), clouds scrolling (C33.3), a camera moving (C26.3) — it's a **channel**: a stream
of keyframes for one typed value. This chapter decodes the channel system from the verified RTTI set (14
channel types, with confirmed vtable addresses) — the animation substrate everything else animates on.

**Key finding (✅ verified):** animation is built from **typed keyframe channels** — a base `tChannel` with
**14 typed variants** (`tFloat1Channel`, `tQuaternionChannel`, `tColourChannel`, `tBoolChannel`,
`tEventChannel`, `tVector3DOFChannel`, …), including a **compressed rotation** channel
(`tCompressedQuaternionChannel`). **Controllers** (`Scenegraph::TransformAnimationController`,
`tLightAnimationController`, …) sample channels each frame and write the result onto their target.

---

## Deep-dive pages

- [C34.1 — The Channel System](01-channel-system.md): what a channel is; keyframes and sampling.
- [C34.2 — The Typed Channels](02-typed-channels.md): the 14 channel types and what each animates.
- [C34.3 — Compressed Quaternions](03-compressed-quaternions.md): why rotation gets its own compressed channel.
- [C34.4 — Controllers](04-controllers.md): how channels reach their targets.
- [C34.5 — Channels Everywhere](05-channels-everywhere.md): skeletons, lights, transforms, textures, cameras.

---

## 34.1 The channel system (✅ verified)

A **channel** is the atom of animation: a keyframed stream of one typed value over time. The base and the
sampling model:

```
tChannel (base)   — a sequence of keyframes for one value; sampled by time to produce the current value
```

To animate anything, you store its value at keyframe times and **interpolate** between them at the current
time. A channel *is* that: keyframes + interpolation for one value. Everything animated in the game is one or
more channels — a joint's rotation is a quaternion channel, a light's brightness a float channel, a texture's
scroll a vector channel. [C34.1](01-channel-system.md).

## 34.2 The typed channels (✅ verified)

There is one channel type per kind of value — 14 verified types:

| Channel | Animates |
|---|---|
| `tFloat1Channel` / `tFloat2Channel` | a scalar / a pair (e.g. UV scroll) |
| `tVector1DOFChannel` / `2DOF` / `3DOFChannel` | 1-, 2-, 3-component vectors (positions, scales) |
| `tQuaternionChannel` | a rotation |
| `tCompressedQuaternionChannel` | a rotation, compressed (C34.3) |
| `tColourChannel` | an RGBA colour (light/material colour) |
| `tBoolChannel` | an on/off value (visibility) |
| `tIntChannel` | an integer |
| `tStringChannel` | a string (e.g. a swapped name) |
| `tEventChannel` | discrete events fired at keyframe times |
| `tEntityChannel` | a referenced entity over time |

Typed channels mean each value animates with the right interpolation — quaternions slerp, colours blend,
bools step, events fire. [C34.2](02-typed-channels.md).

## 34.3 Compressed quaternions (✅ verified)

Rotation gets **two** channels — `tQuaternionChannel` and `tCompressedQuaternionChannel` — because rotation
data dominates skeletal animation (every joint, every frame) and a full quaternion (4 floats = 16 bytes) is
expensive. The compressed variant stores rotations in far fewer bytes, trading a little precision for a large
size saving across a character's dozens of joints over hundreds of frames. [C34.3](03-compressed-quaternions.md).

## 34.4 Controllers (✅ verified)

A channel holds the *data*; a **controller** applies it to a *target* each frame:

```
Scenegraph::TransformAnimationController  — animates a scene-graph node's transform (C10.3)
tLightAnimationController                 — animates a light (C33.2)
tBillboardQuadGroupAnimationController    — animates billboards (C33.5)
choreo::AnimationDriver / *Driver         — drive character rigs (C17.2)
```

Each frame the controller samples its channel(s) at the current time and writes the value onto its target's
property. [C34.4](04-controllers.md).

## 34.5 Channels everywhere (✅ verified)

The channel system is the *one* animation substrate everything reuses:

- **Skeletons** (C8/C17): joint rotations are quaternion channels; the choreo drivers (C17.2) blend them.
- **Lights** (C33.2): colour/intensity channels via `tLightAnimationController`.
- **Transforms** (C10.3): node position/rotation/scale via `TransformAnimationController`.
- **Textures**: UV-scroll (the moving clouds, C33.3) via float/vector channels.
- **Cameras** (C26.3): animated cameras are position/rotation channels played by `CameraPlayer`.

[C34.5](05-channels-everywhere.md).

---

## Key takeaways

- Animation's atom is the **channel**: keyframes + interpolation for one typed value, sampled by time.
- There are **14 typed channels** (float/vector/quaternion/colour/bool/int/string/event/entity), so each
  value animates correctly (quaternions slerp, events fire, bools step).
- Rotation has a **compressed** channel (`tCompressedQuaternionChannel`) because skeletal rotation data is
  the bulk of animation.
- **Controllers** sample channels and write them onto targets (transforms, lights, billboards, rigs).
- It's **one substrate**: skeletons (C8/C17), lights (C33), transforms (C10), textures (C33.3), and cameras
  (C26) all animate on channels. All classes ✅ verified with ✅ vtable addresses; offsets ⏳.

**This completes the runtime coverage.** Return to the [chapter map](../README.md#chapters) or the
[Legend](../Legend/README.md).
