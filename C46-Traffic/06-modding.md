# C46.6 — Modding Traffic

> Traffic is script-defined (traffic groups + `SetMaxTraffic`) with confirmed runtime classes, so
> it's moddable from both sides.

## Script-level (in `leveli.mfk` / mission scripts)
- **Re-cast the mix:** edit each `CreateTrafficGroup … CloseTrafficGroup` block — change models and
  weights (e.g. make sports cars common). New models must be loaded vehicles with a `.con` (C15/C44.2).
- **Density:** raise/lower `SetMaxTraffic` (C46.4), minding the vehicle/actor pools (C39).
- **Per-mission feel:** adjust the `SetMaxTraffic` a mission sets.

## Native-level (DonutsSDK + VanHooks)
- Hook `TrafficVehicle` / `TrafficLocomotion` (confirmed vtables) to change traffic speed,
  aggression, or spawning.
- Read live traffic via `shar::identify` and the runtime offsets (C28.7).

## Cautions
- New vehicle models must be packaged/loaded or they won't spawn (C39.4).
- Big density increases press the vehicle/actor pools and the road network — measure first (C39.6).
- Reversible, single-player/offline (C28.6).

## Cross-references
C46.1/46.4 (groups & cap), C15 (vehicle `.con`), C39 (limits), C28.5/28.7 (hooking + identify), C13 (roads).
