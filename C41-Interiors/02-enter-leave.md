# C41.2 — Entering & Leaving

> The on-foot flow of walking into a building and back out, and how it hooks the C40 fade.

## Entering (✅ verified flow)
1. On foot, walk onto an `InteriorEntranceLocator` (C41.1). The game offers
   **`ActionButton::EnterInterior`** (`0x0061723C`) — the context prompt.
2. Confirm → **`EVENT_ENTER_INTERIOR_TRANSITION_START`** fires to `CGuiManagerInGame`; the
   `Fader` raises the black box (C40.1) and input is gated.
3. `InteriorManager` swaps the exterior for the interior and places you at the interior origin.
4. **`EVENT_ENTER_INTERIOR_TRANSITION_END`** → the fade lifts; you're inside.

## Leaving (✅ verified)
Reaching the `InteriorExit` (or meeting a `LeaveInteriorCondition`) fires
`EVENT_EXIT_INTERIOR_START`, raises the fade, swaps back to the street, and lifts on
`EVENT_EXIT_INTERIOR_END`. `GetOutOfCarCondition` is the related on-foot gate used by some
mission logic.

## Vehicles and interiors
You enter interiors **on foot**, not by car — so entering typically implies you've already
exited any vehicle (C42). The "black box when entering/exiting a vehicle" the player notices is
this same `Fader`/transition machinery, reused wherever the game must hide a swap or reset.

## Why the START/END bracket
The swap includes bringing up the interior's assets; START/END lets the fade animate while that
happens and guarantees the box only lifts once the interior is ready (C40.2).

## What happens if you bend it
Suppress the fade for instant entry (keep the swap gated to END); change the entrance action's
prompt; script a forced enter/leave. All via the confirmed classes + C40 hooks.

## Cross-references
C40.1/40.2 (fade + events), C41.1 (the manager/locators), C42 (getting out of the car first).
