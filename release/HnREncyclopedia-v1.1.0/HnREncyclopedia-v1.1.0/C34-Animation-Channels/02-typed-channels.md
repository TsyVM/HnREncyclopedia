# C34.2 — The Typed Channels

**What it is.** The 14 concrete channel types — one per kind of value the game animates. Typing the channel
by value is what lets each animate *correctly*: a rotation slerps, a colour blends, a boolean steps, an event
fires.

**How it works (✅ verified).** The complete verified set, grouped by what they animate:

```
Scalars & vectors:
  tFloat1Channel        — one float (brightness, alpha, a scroll offset)
  tFloat2Channel        — two floats (a 2-D UV scroll)
  tVector1DOFChannel    — a 1-DOF vector value
  tVector2DOFChannel    — a 2-DOF vector
  tVector3DOFChannel    — a 3-DOF vector (position, scale)
Rotation:
  tQuaternionChannel            — a rotation (4-float quaternion)
  tCompressedQuaternionChannel  — a rotation, compressed (C34.3)
Colour & flags:
  tColourChannel        — an RGBA colour (light, material, sprite tint)
  tBoolChannel          — an on/off value (visibility toggles)
  tIntChannel           — an integer (a discrete index/state)
Discrete/reference:
  tStringChannel        — a string over time (a swapped name/label)
  tEventChannel         — fires discrete events at keyframe times
  tEntityChannel        — references an entity over time
```

Each type carries the right **interpolation**: floats and vectors interpolate linearly; quaternions
**slerp** (spherical, so rotation is smooth and constant-speed, not wobbling); colours blend per component;
**bools and ints step** (they hold a value until the next keyframe — you can't half-toggle visibility);
**events don't interpolate at all** — a `tEventChannel` *fires* at its keyframe times (a footstep sound, a
"spawn now" trigger); strings and entity references likewise step/switch.

**Why a type per value.** Different values *mean* different things over time, and interpolating them the same
way is wrong. Slerping a quaternion gives smooth rotation; lerping it gives a speed-varying wobble. Stepping a
bool is correct; interpolating it is meaningless (there's no "0.5 visible"). Firing an event at its time is
right; interpolating an event is nonsensical. By making the channel *typed*, the engine guarantees each value
animates with the correct math — the type *is* the interpolation rule. This is the same "type carries
behaviour" design as the shader params (C6, typed by chunk id) and the mission objectives (C16, typed by
name): the type determines how the value is handled.

**The event channel — animation that *does* things.** `tEventChannel` is special: it doesn't animate a
*value*, it fires *events* at keyframe times. This is how animation triggers gameplay — a footstep animation
fires a footstep-sound event at the moment the foot lands (C8.1 foot plant), an attack animation fires a
"damage now" event at the strike frame, a cutscene fires a "next line" event. So animation isn't just visual
motion; via event channels it drives *timing* across systems — the animation *is* the clock for the events
synced to it. This is why a kick (C32.1) hurts at the right frame, and dialogue (C19.4) syncs to mouth
movement.

**What happens if you bend it.**

- *Use the wrong channel type* — a rotation in a vector channel won't slerp; a toggle in a float channel
  won't step. Match the channel type to the value.
- *Interpolate an event channel* — events fire, they don't blend. Use `tEventChannel` for discrete triggers.
- *Rely on a channel member offset* — types/vtables ✅, offsets ⏳. Diff (C4.3).
