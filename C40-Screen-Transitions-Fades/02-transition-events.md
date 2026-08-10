# C40.2 — The Interior Transition Event Protocol

> The black box is **event-driven**. The engine brackets each interior enter/exit with START and
> END events so the fade lasts exactly as long as the swap.

## The events (✅ verified strings in the exe)
```
CGuiManagerInGame <= EVENT_ENTER_INTERIOR_TRANSITION_START.
CGuiManagerInGame <= EVENT_ENTER_INTERIOR_TRANSITION_END.
CGuiManagerInGame <= EVENT_EXIT_INTERIOR_START.
CGuiManagerInGame <= EVENT_EXIT_INTERIOR_END.
```
These are dispatched to `CGuiManagerInGame` (the in-game UI manager, C38.1).

## The flow (enter)
1. Player triggers `ActionButton::EnterInterior` (C41) at an `InteriorEntranceLocator`.
2. **`EVENT_ENTER_INTERIOR_TRANSITION_START`** → the GUI raises the `Fader` (fade to black) and
   input is gated.
3. The `InteriorManager` swaps the world for the interior and repositions the player at the
   interior origin.
4. **`EVENT_ENTER_INTERIOR_TRANSITION_END`** → the fader fades back in; control returns.

Exit mirrors it with `EVENT_EXIT_INTERIOR_START/END`.

## Why events, not a blocking call
The swap includes a load; a blocking fade would freeze the frame. The START/END protocol lets
the fade animate on the render thread while the load proceeds, and the END event fires only when
the interior is resident — so the box is never lifted early onto an unloaded scene.

## What happens if you bend it
Hooking the START handler lets you change what the box does (colour/time) or add your own work
during the covered window; suppressing it yields an instant swap. Never lift the box before END
or you reveal a half-loaded interior.

## Cross-references
C41 (InteriorManager & the swap), C40.1 (the Fader), C38.1 (`CGuiManagerInGame`), C30 (loading).
