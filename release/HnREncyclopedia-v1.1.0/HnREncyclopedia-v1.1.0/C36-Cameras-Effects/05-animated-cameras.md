# C36.5 — Animated & Scripted Cameras

**What it is.** The cinematic cameras — the scripted, keyframed camera moves that play during cutscenes and
special moments, and the on-rails cameras that glide along a path. These are the cameras that *aren't*
following gameplay but performing an authored shot.

**How it works (✅ verified).**

```
AnimatedCam / RelativeAnimatedCam  — a keyframed camera move (position/rotation over time)
CameraPlayer : SimpleAnimationPlayer, AnimationPlayer  — plays a camera animation (via channels, C34)
RailCam        — a camera that follows a set path/rail (a spline, C13)
TrackerCam     — a camera that tracks a moving target
StaticCam / StaticCamLocator  — a fixed camera at a placed point
```

An **`AnimatedCam`** plays a *keyframed* camera move — the camera's position and rotation are animation
**channels** (C34, `tVector3DOFChannel` for position, `tQuaternionChannel` for rotation) played by
**`CameraPlayer`** (which is an `AnimationPlayer`, C34.4 — it samples the channels each frame and writes them
to the camera). So a scripted camera sweep *is* animation, on the same channel substrate as everything else
(C34.5): the camera is just another target a controller animates. **`RailCam`** follows a defined path (a
rail/spline) — the camera glides along the track while looking at a target, the classic "cinematic dolly"
shot. **`StaticCam`** is fixed at a locator (`StaticCamLocator`, C8.4) — a security-camera-style fixed angle.

**Why scripted cameras are channel animations.** Reusing the channel/animation system (C34) for cameras —
rather than a bespoke camera-scripting format — means a camera move is authored the same way as a character
animation (keyframes on channels, C34.1) and played the same way (a `CameraPlayer`/`AnimationPlayer` sampling
channels, C34.4). One animation system serves skeletons, lights, transforms, *and* cameras (C34.5). This is
the economy of the unified channel substrate: a cutscene camera sweep needs no new machinery, just a camera
target for the existing animation system. It also means camera moves are authored in the same tools as
character animation, exported as the same channel data.

**The cutscene tie (C17.4).** These cameras are what the NIS in-engine cutscenes (C17.4) use: an NIS
choreographs `choreo::` puppets (C17) *and* runs a `CameraPlayer` on an `AnimatedCam` for the scripted camera,
synced by `NISEvent`s (C17.4) on the timeline. The mission scripts cue them with `SetAnimatedCameraName`/
`SetAnimCamMulticontName` (C14.6). So a story cutscene is: characters posed by choreography (C17), framed by
an animated camera (here), scored by dialogue/audio (C19) — all channel-animated (C34) and sequenced by the
NIS timeline (C17.4). The animated cameras are the *cinematography* of the cutscene system.

**Scripted vs. reactive cameras.** This closes the chapter's arc: the gameplay cameras (C36.1) *react* to
what you do (event-driven, C36.4) — they follow, shake, and switch by gameplay state; the scripted cameras
(here) *perform* an authored shot (channel-animated) — they ignore gameplay and play their keyframes. It's the
same reactive-vs-authored split as ambient animation vs. choreography (C17), traffic vs. mission cars (C24.3),
and the road graph vs. path segments (C13): the engine provides a *reactive* system for moment-to-moment play
and an *authored* system for designed set-pieces, and cameras have both. Which one is active depends on the
context — driving uses reactive cameras, a cutscene uses scripted ones — switched by `SuperCamCentral` (C36.2).

**What happens if you bend it.**

- *Rely on an `AnimatedCam`/`CameraPlayer` member offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Expect a scripted camera to follow gameplay* — it plays its keyframes, ignoring the action. Use a reactive
  camera (C36.1) for gameplay, a scripted one for cutscenes.
- *Author a camera move in a non-channel format* — the system plays channels (C34). Author camera moves as
  channel animations.

**This completes the encyclopedia's camera and effects coverage.** Return to the
[chapter map](../README.md#chapters) or the [Legend](../Legend/README.md).
