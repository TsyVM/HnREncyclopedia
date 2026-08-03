# C34.5 — Channels Everywhere

**What it is.** The realisation that the channel system (C34.1–C34.4) is the *one* animation substrate the
entire game reuses. Skeletons, lights, transforms, textures, cameras, UI — everything that changes over time
animates on channels. This page ties the substrate to every system that stands on it.

**How it works (✅ verified — the reuse).** The same channels + controllers drive every animated system:

- **Skeletons & characters** (C8, C17) — each joint's rotation is a `tQuaternionChannel` (usually compressed,
  C34.3); the `choreo::` drivers (C17.2) sample and blend them to pose the rig (C8.1), which deforms the mesh
  (C8.3). Character animation *is* channels, blended.
- **Lights** (C33.2) — a flickering or pulsing light is a `tColourChannel`/`tFloat1Channel` driven by
  `tLightAnimationController`. Dynamic lighting on fixed-function hardware is channel-animated light values.
- **Scene-graph transforms** (C10.3) — a moving platform, a rotating windmill, an opening door is a
  position/rotation channel driven by `Scenegraph::TransformAnimationController` onto the node's matrix.
- **Textures** (C33.3) — the scrolling clouds (`l3_Cloudmove`) and other flowing textures are UV-offset
  `tFloat2Channel`/vector channels. Texture animation is channels on UVs.
- **Cameras** (C26.3) — an `AnimatedCam` is position/rotation channels played by `CameraPlayer`. Scripted
  camera moves (`SetAnimatedCameraName`, C14.6) are channel-driven.
- **Billboards & UI** (C33.5, C21) — pulsing sprites, animated HUD elements are channels on their transforms
  and colours.
- **Events & timing** (C34.2) — `tEventChannel`s fire footsteps, hit frames, and dialogue cues synced to the
  animations they ride on.

**Why one substrate for everything.** Building *one* animation system (channels + controllers) and reusing it
for every animated thing — rather than a separate animator per system — is the defining economy of the engine's
animation design. It means: one keyframe/interpolation implementation (C34.1), one set of typed value handlers
(C34.2), one compression scheme (C34.3), reused everywhere. A new animated thing (a new light effect, a new
moving prop) needs only a channel and the right controller — no new animation code. It also means animators and
tools work in one paradigm (keyframes on channels) whether they're animating a character, a light, or a camera.
This unification is why the `choreo::` character system (C17), the `tLight` lighting (C33.2), and the scene-graph
transforms (C10.3) all share the same underlying channels — they're facets of one substrate.

**The whole animation picture.** Putting C8, C17, C33, and this chapter together: **channels** (C34) are the
atoms — keyframed typed values; **controllers** (C34.4) apply them to targets; **clips/banks** (C17.2) bundle
channels into poses; **choreo drivers** (C17.2) blend clips onto **rigs** (C8.1/C17.1); and the results animate
**skeletons** (C8), **lights** (C33.2), **transforms** (C10.3), **textures** (C33.3), and **cameras** (C26.3).
From one keyframed value to a fully animated world, it's channels all the way down. This is the backend the
user never sees but that moves everything that moves.

**What happens if you bend it.**

- *Assume each system has its own animation* — they share the channel substrate. Edit a channel and you edit
  animation uniformly, wherever it's applied.
- *Rely on a channel/controller member offset* — the types/vtables ✅, offsets ⏳. Diff (C4.3).
- *Animate a value the wrong type* — use the matching typed channel (C34.2) so it interpolates correctly.

**This completes the encyclopedia's runtime coverage.** Return to the [chapter map](../README.md#chapters) or
browse the [Legend](../Legend/README.md).
