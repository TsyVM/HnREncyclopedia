# C40.6 — Modding Transitions

> Every transition class has a confirmed vtable, so the fade, the iris wipe, and the sequencer
> are all hookable with DonutsSDK + VanHooks (C28.5/C28.7).

## Common mods
- **Faster / slower interior fade.** Hook the `Fader`'s update to scale its ramp duration, or
  the `EVENT_ENTER_INTERIOR_TRANSITION_START` handler to pass a different time.
- **Instant swaps (no black box).** Suppress the fade (make the ramp immediate) — but keep the
  swap gated to END so you don't reveal an unloaded interior (C40.2).
- **Recolour the fade.** Change the fader quad's colour for a white/coloured flash.
- **Custom wipe.** Swap the iris-wipe texture/shape, or trigger `SetIrisWipe` from your own
  mission script for themed transitions.
- **Custom menu flow.** Assemble a `GuiSFX` chain (C40.4) from the confirmed effect classes.

## Recipe (fade timing)
```cpp
// Identify the Fader by its verified vtable (0x0060B240), hook its per-frame update,
// and scale the alpha-ramp delta. Reversible (VanHooks remove).
const auto* f = shar::db::find_class("Fader");           // 0x0060B240
// ...hook_vtable on the update slot; in the detour, adjust the ramp, call original.
```

## Discipline
- Recover slot indices per build (C28.7); addresses are build-specific.
- Keep the swap synchronized to the END event — never lift the cover early.
- Reversible, single-player, offline (C28.6).

## Cross-references
C28.5/C28.7 (hooking + SAHRDiag), C40.1–40.5 (the classes to hook), C41 (the interior swap).
