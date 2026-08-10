# C25.3 — Controllers & the `CharacterManager`

**What it is.** The layer that decides *who drives* a character and the manager that runs them all — the
character counterparts to `VehicleController` and `VehicleCentral` (C24).

**How it works (✅ verified).** From `shar_dumps.csv`:

```
CharacterController : tRefCounted, radLoadObject, IRefCount
  CameraRelativeCharacterController : PhysicalController, CharacterController   — the player on foot
CharacterMappable / BipedCharacterMappable : Mappable, …                       — input → action mapping
CharacterManager : EventListener, LoadingManager::ProcessRequestsCallback      — loads & tracks characters
CharacterSheetManager : GameDataHandler                                        — character data/unlocks
```

A `Character` (C25.1) holds a `CharacterController`. For the player on foot, it's a
`CameraRelativeCharacterController` — movement is interpreted relative to the camera (push "up" and the
avatar walks away from the camera), the standard third-person control scheme. The `Mappable` classes
translate raw input into character actions. `CharacterManager` is the singleton that loads characters
(pulling their `.p3d` and `.cho`, C8) and tracks the active set — the character analogue of `VehicleCentral`
(C24.3).

**Why separate controller from character.** The same reason as vehicles (C24.2): one `Character` body can be
driven by different sources. The player's avatar uses a `CameraRelativeCharacterController`; an NPC uses an
AI-driven controller feeding the same `CharacterAi` FSM (C25.2). Swapping the controller changes who's in
charge without changing the character. This also enables the car hand-off: when the player enters a vehicle
(`GetIn`→`InCar`, C25.2), control shifts from the character controller to the vehicle controller (C24.2), and
back on exit. The two controller hierarchies (character and vehicle) are two ends of that hand-off.

**The manager's role.** `CharacterManager` owns character lifetime — spawning the ambient population (C25.5)
up to budget, loading mission NPCs, freeing distant pedestrians. Being an `EventListener` (C23.3), it reacts
to game events (mission started, area changed) to load the right characters. `CharacterSheetManager` handles
the persistent character data — costumes, unlocks (the `buyskin` objective, C16.3) — the character side of
the reward economy (C16.6).

**The singleton addresses (⏳).** `CharacterManager` and `CharacterSheetManager` are singletons whose
**addresses are ⏳** (C23.1) — a mod that wants to enumerate live characters needs the manager pointer,
recovered by diffing (C4.3). The *classes* are verified; the *instance addresses* are the open part, exactly
as with `VehicleCentral` (C24.3).

**What happens if you bend it.**

- *Assume the player and NPCs are different character objects* — they're the same `Character` (C25.1) with
  different controllers. Target the controller for behaviour, the character for the body.
- *Rely on a manager singleton address* — ⏳; recover it for your build (C4.3).
- *Edit character control without accounting for the car hand-off* — entering a vehicle shifts control to the
  vehicle controller (C24.2). Handle both sides of the transition.
