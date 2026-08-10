# C36.2 — `SuperCamCentral` & Switching

**What it is.** The manager that decides *which* of the 41 cameras (C36.1) is active and switches between them
as the game changes state — plus the `*Data` companions that tune each. It's the camera counterpart to
GameFlow (C30) — a state machine of cameras.

**How it works (✅ verified).** From the verified set (extending C26.4):

```
SuperCamCentral : EventListener, GameDataHandler  — owns the active camera, switches it
SuperCamController : Mappable                      — maps input to camera control (look, adjust)
CameraDataLoader                                   — loads camera *Data from Pure3D chunks (C23.4)
*Data companions: ChaseCamData, BumperCamData, FollowCamData, ConversationCamData,
                  WalkerCamData, TrackerCamData, FollowCamDataChunk, WalkerCamDataChunk
```

**`SuperCamCentral`** holds the current `SuperCam` and switches it in response to game events (it's an
`EventListener`, C23.3): enter a car → `ChaseCam`; drive recklessly or jump → `WrecklessCam` (C36.4);
reverse → `ReverseCam`; talk → `ConversationCam`; exit the car → `WalkerCam`; open the minigame →
`SuperSprintCam`. The switch is a pointer change plus a **transition** (a blend from the old camera to the
new, so it doesn't hard-cut). `SuperCamController` handles player camera input (looking around, adjusting the
view).

**The `*Data` split.** Every camera type has a **`*Data`** companion holding its *tuning* — separate from its
*behaviour* (the `SuperCam` subclass). `ChaseCamData` holds how far the chase camera trails, its height and
lag; `ConversationCamData` its framing distance; `TrackerCamData` its tracking speed. This is the same
behaviour/data split as vehicles (a `Vehicle` tuned by a `.con`, C24.4), shaders (C6), and camera contexts
throughout the engine: the code is the subclass, the numbers are the data, loaded via `CameraDataLoader`
(C23.4) from Pure3D camera chunks. So *tuning* a camera (making the chase view pull back further) is editing
its `*Data`, not its code — a data edit.

**Why centralise switching.** Exactly one camera must be active at a time, transitions must be smooth, and the
choice depends on global game state (are you driving? talking? jumping?). Centralising this in
`SuperCamCentral` means one object owns "what should the camera be right now?" and one place handles the blend
— rather than every system grabbing the camera and fighting over it. This is the shared-exclusive-resource
manager pattern (like `CoinManager` C32.3, `VehicleCentral` C24.3): the active camera is a shared, exclusive
resource, and one manager owns it. The switcher is effectively a camera state machine, mirroring the engine
states (C35.1) and GameFlow contexts (C30.1) it reacts to.

**The singleton (⏳).** `SuperCamCentral` is a singleton; its **instance address is ⏳** (C23.1). A mod that
wants to force a camera or read the active one needs that pointer (recover by diffing, C4.3). The class and
switching mechanism are ✅ verified (with vtable); the instance pointer is the open part.

**What happens if you bend it.**

- *Edit camera behaviour when you meant tuning* — distance/angle/lag live in the `*Data` (C23.4), not the
  camera code. Edit the data for tuning.
- *Rely on the `SuperCamCentral` singleton address* — ⏳; recover per build (C4.3).
- *Force a camera switch outside the manager* — you can cause hard cuts or conflicts. Let `SuperCamCentral`
  own switching so blends stay clean.
