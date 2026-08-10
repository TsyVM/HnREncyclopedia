# C44.6 — Modding Level Init

> `leveli.mfk` is plain text, so most "how the level starts" mods are one-line edits — no code.

## Common edits
- **Start in a different car:** change `InitLevelPlayerVehicle("famil_v", …)` to another loaded
  vehicle model (with a `.con`, C15).
- **Move the start:** change the start locator name.
- **Denser / lighter crowds:** edit the ped groups (C45) and raise `PreallocateActors` (C44.4/C39)
  to allow more.
- **More/less traffic:** edit `SetMaxTraffic` and the traffic groups (C46).
- **Tougher police:** raise `SetNumChaseCars`, lower `SetHitAndRunDecay`.
- **Turn off tutorials:** `EnableTutorialMode( 0 )`.
- **Custom coin model:** change `SetCoinDrawable(...)` (C32).

## Discipline
- Anything you add must be **loaded** (its model packaged, C44.2/C39.4) or the spawn silently fails.
- Keep `CreatePedGroup … AddPed … ClosePedGroup` / `CreateTrafficGroup … CloseTrafficGroup`
  blocks well-formed (open → add → close).
- Watch the actor pool (C44.4) — denser crowds need a bigger reservation, paid from the static
  heap (C39.3).
- Back up the file; single-player/offline (C28.6).

## Cross-references
C45/C46 (crowd & traffic edits), C44.4/C39 (actor pool), C15 (car `.con`), C32 (coins), C28 (modding).
