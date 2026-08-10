# C36.4 — Event-Driven Camera Reactions

**What it is.** Why the camera *reacts* to what you do — pulling back when you jump, jolting when you crash,
framing a conversation when a mission cues it. The camera isn't passive; it listens to gameplay events and
responds. This page is how the physics/gameplay systems (C35) drive the camera.

**How it works (✅ verified).** `SuperCamCentral` (C36.2) is an **`EventListener`** (C23.3) — it subscribes to
the game's event stream and switches cameras or fires effects in response. The verified event→camera wiring:

- **Jump** — entering `InAirEngineState` (C35.3) fires an event; `SuperCamCentral` can switch to a dramatic
  angle (`WrecklessCam`, C36.1) to emphasise the air, and on landing fire a `SineCosShaker` (C36.3) for the
  impact.
- **Crash / hard impact** — a big collision (C26.6) fires an event → `SineCosShaker` jolt (C36.3), scaled to
  the impact force.
- **Smashing glass** — breaking a `BreakableObjectDSG` (C35.5) fires an event → `SineCosShaker` shake + the
  debris/sound (C33.5).
- **Reckless driving** — sustained high-speed/reckless driving → `WrecklessCam` for a more dynamic angle.
- **Reversing** — entering `ReverseEngineState` (C35.1) → `ReverseCam` to frame backward.
- **Conversation / mission cue** — `SetConversationCam`/`SetAnimatedCameraName` (C14.6) → `ConversationCam`/
  `AnimatedCam`.
- **On foot** — exiting the vehicle (`GetOut`, C25.2) → `WalkerCam`.

So the camera's behaviour is *reactive*: the engine states (C35), collisions (C26.6), breakables (C35.5), and
mission scripts (C14.6) all emit events, and the camera system listens and responds.

**Why event-driven cameras.** The camera should reflect what's happening *without* every gameplay system
having to know about cameras. Making `SuperCamCentral` an `EventListener` decouples them: the vehicle physics
fires "I'm airborne" (C35.3) without knowing a camera exists; the camera system hears it and reacts. This is
the same event architecture as missions (C26.1), the Hit & Run meter (C31.1), and the whole runtime (C23.3):
systems communicate by events, so they stay independent. The camera is a *consumer* of the gameplay event
stream — one of many listeners (the HUD, the audio, the missions are others) that react to the same events. A
crash event drives the camera shake, the crash sound, the damage, and any mission `damage` condition (C16.4),
all independently.

**The jump, end to end.** Putting the systems together, hitting a ramp is: the vehicle enters
`InAirEngineState` (C35.3, physics) → fires an "airborne" event → `SuperCamCentral` (listening) switches to a
dramatic angle and starts tracking air time → the car arcs under gravity (C35.4) → lands (collision, C26.6) →
fires an "impact" event → `SineCosShaker` jolts the camera (C36.3), the suspension compresses (C35.4), a
landing sound plays (C19), and rumble fires (C33.5). One player action, a cascade of event-driven reactions
across physics, camera, audio, and haptics — which is exactly the "camera effect when a car jumps" the
systems deliver.

**What happens if you bend it.**

- *Expect the camera to react without the event* — it's event-driven; if the gameplay event doesn't fire, the
  camera doesn't react. The wiring is through events (C23.3).
- *Rely on the reaction offsets* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Add a new dramatic moment and forget the camera* — fire an event the camera can listen for, or the moment
  won't get its camera reaction. Wire it into the event stream.
