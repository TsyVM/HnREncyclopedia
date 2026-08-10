# Chapter 36 — Cameras & Camera Effects

> **Goal of this chapter:** decode the full camera system and its *effects* — not just the framing cameras,
> but the **camera shake** and event-driven reactions that make a jump feel airborne and a crash feel
> violent. This completes and extends the camera coverage of C26.3.

Chapter 26.3 introduced the `SuperCam` family; this chapter documents the *whole* of it — **41 verified
cameras** — plus the pieces that make cameras *react*: the shake (`SineCosShaker`) and the event wiring that
fires a dramatic angle when you jump and a jolt when you smash through glass. All grounded in the verified
RTTI set with confirmed vtable addresses.

**Key finding (✅ verified):** the camera system is **41 cameras** — driving (`BumperCam`, `ChaseCam`,
`FollowCam`, **`WrecklessCam`**, `ReverseCam`), on-foot (`WalkerCam`, `ComedyCam`), cinematic (`AnimatedCam`,
`RailCam`, `TrackerCam`, `ConversationCam`, `StaticCam`), and special (`HudMapCam`, `SuperSprintCam`,
`DebugCam`) — switched by `SuperCamCentral`, each with a `*Data` tuning companion. The **camera shake** is
**`SineCosShaker`** (0x00614FC0), which perturbs the camera on jumps, impacts, and breaking glass (C35).

---

## Deep-dive pages

- [C36.1 — The Full Camera Roster](01-camera-roster.md): all 41 cameras, categorized.
- [C36.2 — `SuperCamCentral` & Switching](02-switching.md): the manager, the `*Data` split, transitions.
- [C36.3 — Camera Shake: `SineCosShaker`](03-camera-shake.md): the jolt on jumps, crashes, and glass.
- [C36.4 — Event-Driven Camera Reactions](04-event-reactions.md): wiring gameplay events to camera effects.
- [C36.5 — Animated & Scripted Cameras](05-animated-cameras.md): `AnimatedCam`, `RailCam`, `CameraPlayer`.

---

## 36.1 The full camera roster (✅ verified)

All 41 cameras are `SuperCam` subclasses (C26.3), grouped by use:

```
Driving:   ChaseCam, BumperCam, FollowCam, WrecklessCam, ReverseCam
On-foot:   WalkerCam, ComedyCam
Cinematic: AnimatedCam, RelativeAnimatedCam, ConversationCam, RailCam, TrackerCam, StaticCam
Special:   HudMapCam (the 3-D minimap cam, C29), SuperSprintCam (the minigame), DebugCam, KullCam, PCCam
Manager:   SuperCamCentral, SuperCamController; CameraPlayer (plays animated cameras)
```

Notable ones C26.3 didn't name: **`WrecklessCam`** (a dramatic angle for reckless/high-speed driving and
jumps), **`RailCam`** (an on-rails camera following a set path), **`ReverseCam`** (frames reversing),
**`TrackerCam`** (tracks a target), and **`HudMapCam`** (the camera that renders the 3-D minimap, C29.1).
[C36.1](01-camera-roster.md).

## 36.2 `SuperCamCentral` & switching (✅ verified)

`SuperCamCentral` (C26.4) owns the active camera and switches between the 41 as context demands: enter a car →
`ChaseCam`; jump/drive recklessly → `WrecklessCam`; reverse → `ReverseCam`; talk → `ConversationCam`; get out
→ `WalkerCam`. Each camera has a **`*Data`** companion (`ChaseCamData`, `FollowCamData`, `TrackerCamData`…)
holding its tuning (distance, angle, lag), loaded via `CameraDataLoader` (C23.4). [C36.2](02-switching.md).

## 36.3 Camera shake: `SineCosShaker` (✅ verified)

The **camera shake** — the jolt when you land a jump, crash, or smash through glass — is **`SineCosShaker`**
(0x00614FC0). It perturbs the camera's position/rotation with a decaying **sine/cosine** oscillation: a sharp
initial displacement that wobbles and settles, driven by the shake's amplitude and frequency. This is the
"impact" feedback that makes collisions *felt* through the camera. [C36.3](03-camera-shake.md).

## 36.4 Event-driven camera reactions (✅ verified)

Cameras *react* to gameplay because the camera system listens for events (C23.3): entering `InAirEngineState`
(a jump, C35.3) → switch to a dramatic angle (`WrecklessCam`) and/or shake on landing; a crash or breaking a
`BreakableObjectDSG` (glass, C35.5) → `SineCosShaker` jolt; a mission cue (`SetConversationCam`, C14.6) →
`ConversationCam`. The physics/gameplay events (C35) drive the camera effects. [C36.4](04-event-reactions.md).

## 36.5 Animated & scripted cameras (✅ verified)

Cutscenes and scripted moments use **`AnimatedCam`**/`RelativeAnimatedCam` (keyframed camera moves played by
**`CameraPlayer`**, an `AnimationPlayer`, via channels, C34) and **`RailCam`** (following a set path/spline,
C13). These are the cinematic cameras the mission scripts cue (`SetAnimatedCameraName`, C14.6) for NIS
cutscenes (C17.4). [C36.5](05-animated-cameras.md).

---

## Key takeaways

- The camera system is **41 `SuperCam` cameras** — driving/on-foot/cinematic/special — switched by
  `SuperCamCentral`, each with a `*Data` tuning companion.
- **`WrecklessCam`** frames jumps/reckless driving; **`HudMapCam`** renders the 3-D minimap (C29);
  **`RailCam`**/`AnimatedCam` are cinematic.
- **Camera shake** is **`SineCosShaker`** — a decaying sine/cosine wobble that jolts the camera on jumps,
  crashes, and breaking glass (C35).
- Cameras **react to gameplay events** (C23.3): the physics states (C35 — jump, crash, drift) and mission
  cues (C14.6) drive camera switches and shakes.
- **Animated cameras** (`AnimatedCam`/`RailCam`) played by `CameraPlayer` via channels (C34) drive cutscenes
  (C17.4). All classes ✅ verified with ✅ vtable addresses; offsets ⏳.

**This completes the encyclopedia.** Return to the [chapter map](../README.md#chapters) or the [Legend](../Legend/README.md).
