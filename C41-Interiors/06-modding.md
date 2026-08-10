# C41.6 — Modding Interiors

> Interiors are script-declared (`level.mfk`) with confirmed manager classes, so they're
> approachable from both the script side and the native side.

## Script-level (safest)
- **Add/replace a gag inside an interior:** author a `GagBegin…GagEnd` block under
  `GagSetInterior("<id>")` with your position, trigger radius, sound, and optional coin reward
  (C41.4). No code.
- **Retexture an interior:** swap the interior's `.p3d` textures (C5) via loose-file shadowing
  (C28/C3.6).
- **Repopulate:** change `AddAmbientCharacter` entries for the interior's NPCs (in `leveli.mfk`).

## Native-level (DonutsSDK + VanHooks)
- **Observe/alter the swap:** hook `InteriorManager` (`0x00613C48`) to log entries or change the
  destination.
- **Move a doorway:** relocate an `InteriorEntranceLocator` (`0x006070D4`).
- **Custom transition:** pair with the C40 fade hooks for a themed enter/exit.

## Adding a new interior (advanced)
Provide the interior geometry/lighting as assets, place an entrance locator that names it,
register it with the manager, and declare its gag content under `GagSetInterior("<newid>")`.
Then add it to `DonutsSDK/data/interiors.csv`. This is the full author→package→reference→load
pipeline (C39.4) applied to an interior space.

## Discipline
Per-build address re-verification (C28.7); reversible hooks; single-player/offline (C28.6).

## Cross-references
C41.4 (the script vocabulary), C40.6 (transition mods), C5/C3.6 (textures/shadowing), C39.4
(add-content pipeline), C28.5/28.7 (hooking).
