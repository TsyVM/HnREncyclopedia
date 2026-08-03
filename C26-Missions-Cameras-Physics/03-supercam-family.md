# C26.3 — The `SuperCam` Family

**What it is.** The camera system: every camera in the game is a `SuperCam` subclass, and there are 18 of
them, one per way the game wants to frame the action. This is the runtime of the mission camera verbs (C14.6).

**How it works (✅ verified).** From `shar_dumps.csv`, the `SuperCam` family:

```
SuperCam : tRefCounted, radLoadObject, IRefCount
  ├ ChaseCam         — the default follow-behind driving camera
  ├ BumperCam        — bumper / hood view
  ├ FollowCam        — follows a target
  ├ ConversationCam  — frames two characters talking (SetConversationCam, C14.6)
  ├ AnimatedCam      — plays a scripted keyframed camera move (SetAnimatedCameraName, C14.6)
  ├ WalkerCam        — on-foot camera
  │   └ ComedyCam    — comedic framing (derives from WalkerCam)
  ├ DebugCam         — developer free camera
  └ … (18 total)
```

Each is a distinct framing behaviour: `ChaseCam` trails a driving car, `BumperCam` sits on the bumper,
`ConversationCam` composes a two-shot for dialogue, `AnimatedCam` follows an authored spline. They all share
the `SuperCam` base, so the camera system can hold "the current camera" as a `SuperCam*` and switch which
subclass it points to (C26.4) without the rest of the game caring which kind is active.

**Why so many camera types.** A game that is both driving *and* on-foot *and* cutscene-heavy needs many
framings, and each is a small behaviour better expressed as its own class than as a mode flag on one giant
camera. `ChaseCam` and `BumperCam` are driving views; `WalkerCam`/`ComedyCam` are on-foot; `ConversationCam`
and `AnimatedCam` are cinematic. Making each a `SuperCam` subclass means adding a new framing is adding a
class, and the switching logic (C26.4) is uniform. The 18 cameras are the game's whole visual language —
every moment you play is framed by one of them.

**The tie to scripts.** The mission camera verbs you decoded (C14.6) select and drive these classes:
`SetConversationCam` activates a `ConversationCam`, `SetAnimatedCameraName` runs an `AnimatedCam` along a
named animated-camera asset, `SetCamBestSide` tunes framing. So a mission's cinematography (C14.6) is a
sequence of `SuperCam` activations, and the camera classes here are what those verbs construct. The
`CameraPlayer` class (an `AnimationPlayer`) plays back the keyframed camera animations that `AnimatedCam`
uses — the camera analogue of a character playing an animation clip (C25.4).

**What happens if you bend it.**

- *Rely on a `SuperCam` subclass offset* — classes ✅, offsets ⏳. Diff (C4.3).
- *Over-cut between cameras in fast action* — switching framings mid-drive disorients; use `ChaseCam` for
  driving, `ConversationCam` for talk (C14.6). Match the camera to the moment.
- *Expect one camera to do everything* — the system is many small cameras switched by `SuperCamCentral`
  (C26.4). Add a framing as a subclass, don't overload one.
