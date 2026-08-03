# C34.4 — Controllers

**What it is.** The bridge from a channel's *data* to its *effect*: a **controller** samples one or more
channels each frame and writes the result onto a target's property. Channels hold the animation; controllers
apply it.

**How it works (✅ verified).** The verified controller family, each targeting a different kind of thing:

```
Scenegraph::TransformAnimationController  — writes a channel onto a scene-graph node's transform (C10.3)
tLightAnimationController                 — writes onto a light's colour/intensity (C33.2)
tBillboardQuadGroupAnimationController    — writes onto a billboard group (C33.5)
choreo::AnimationDriver / *Driver         — write onto a character rig's joints (C17.2)
CameraPlayer / SimpleAnimationPlayer      — write onto a camera / generic target (C26.3)
```

The pattern is uniform: each frame, the controller (1) computes the current time, (2) **samples** its
channel(s) at that time (C34.1), and (3) **writes** the sampled value onto its target's property. A
`TransformAnimationController` samples a position/rotation channel and writes it to a node's matrix (C10.3),
moving the node; a `tLightAnimationController` samples a colour channel and writes it to a light (C33.2),
making it flicker; a `choreo::AnimationDriver` samples a joint's quaternion channel and writes it to the rig
(C17.2), posing the character.

**Why separate controllers from channels.** It's the data/behaviour split again (seen in cameras C26.4,
shaders C6). A **channel** is *portable data* — the same rotation-over-time channel could drive any joint, any
node. A **controller** is the *binding* — "apply *this* channel to *that* target's *that* property." Separating
them means one channel can be reused across targets, and a controller can be re-pointed at a different channel
without changing either. It also cleanly divides the work: the channel system knows *values over time*, the
controller knows *targets and properties*, and neither needs the other's internals. This is why there's a
controller *type per target kind* (transform, light, billboard, rig) — each knows how to write onto its
specific target, while sharing the same channel-sampling underneath.

**Controllers as the animation frame.** Each frame, all the active controllers sample their channels and
write their targets — that *is* the animation step of the frame loop (C30.5). A scene with 50 animated
characters, a dozen flickering lights, scrolling cloud textures (C33.3), and a moving camera is hundreds of
controllers sampling thousands of channels and writing their targets. The controllers are the *drivers* of the
frame's animation; the channels are the *scripts* they read. Understanding this — controllers pull values from
channels and push them onto targets — is understanding how the whole animated world updates.

**What happens if you bend it.**

- *Point a controller at a channel of the wrong type* — a transform controller fed a colour channel writes
  nonsense. Match the channel type (C34.2) to the controller/target.
- *Rely on a controller member offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Expect a channel to animate without a controller* — a channel is inert data; it needs a controller to
  reach a target. Both are required.
