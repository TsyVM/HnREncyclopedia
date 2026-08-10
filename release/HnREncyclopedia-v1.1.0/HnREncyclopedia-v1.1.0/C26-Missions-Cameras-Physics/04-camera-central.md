# C26.4 — Camera Central & Switching

**What it is.** The layer that decides *which* camera is active and switches between the `SuperCam`
subclasses (C26.3) — `SuperCamCentral` — plus the input controller and the `*Data` tuning companions.

**How it works (✅ verified).** From `shar_dumps.csv`:

```
SuperCamCentral : EventListener, GameDataHandler     — owns the active camera, switches it
SuperCamController : Mappable, tRefCounted, …        — maps input to camera control
ChaseCamData, BumperCamData, ConversationCamData, … — per-camera tuning data (one per SuperCam type)
```

`SuperCamCentral` holds the current `SuperCam` (C26.3) and switches it in response to game events (being an
`EventListener`): enter a car → switch to `ChaseCam`; start a conversation → switch to `ConversationCam`
(driven by `SetConversationCam`, C14.6); get out → switch to a `WalkerCam`. The switch is a single pointer
change plus a transition, because every camera shares the `SuperCam` base. `SuperCamController` translates
player input (look around, change view) into camera adjustments.

**The `*Data` split.** Each camera type has a companion **`*Data`** class — `ChaseCamData`,
`ConversationCamData`, `BumperCamData`. This separates the camera's *behaviour* (the `SuperCam` subclass,
code) from its *tuning* (the `*Data`, values): how far the `ChaseCam` trails, the `ConversationCam`'s framing
distance, the `BumperCam`'s offset. It is the same behaviour/data split as elsewhere — a `Vehicle` (behaviour)
tuned by a `.con` (data, C24.4), a shader (C6) with its parameters. The `*Data` is loaded from camera chunks
(via `CameraDataLoader`, C23.4), so a designer tunes cameras by editing data, not code.

**Why centralise switching.** Cameras must switch cleanly and exclusively — exactly one is active, and
transitions must not jar. Centralising that in `SuperCamCentral` means one object owns the rule "what should
the camera be right now?" and one place handles the blend between cameras. Scattering switching across the
game (each system grabbing the camera) would produce conflicts and hard cuts. The central manager is the
camera equivalent of `VehicleCentral` (C24.3) and `CharacterManager` (C25.3) — a single owner of a shared,
exclusive resource.

**The singleton address (⏳).** `SuperCamCentral` is a singleton; its **address is ⏳** (C23.1). A mod that
wants to force a camera or read the active one needs that pointer, recovered by diffing (C4.3). The class and
the switching mechanism are verified; the instance address is the open part.

**What happens if you bend it.**

- *Rely on the `SuperCamCentral` address* — ⏳; recover it for your build (C4.3).
- *Edit camera behaviour when you meant tuning* — distance/framing live in the `*Data` (C23.4), not the
  `SuperCam` code. Edit the data for tuning.
- *Force a camera switch mid-transition* — let `SuperCamCentral` own switching so blends stay clean. Don't
  grab the camera from outside the manager.
