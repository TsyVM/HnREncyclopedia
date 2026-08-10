# C40.1 — The `Fader` & the Black Box

> `Fader` (`0x0060B240`) is the screen-covering fade you see as a "black box" whenever the game
> hides a world swap — most visibly entering and leaving interiors.

## What it is
A full-screen coloured quad (normally black) whose opacity is animated from 0 → 1 → 0. While it
is opaque, whatever changes behind it — a level/interior swap, a teleport, a mission reset — is
invisible, so the cut looks like a smooth fade instead of a jarring pop. In the SAHRDiag live
capture the class was resident as `Fader ×3` (a small pool of faders for overlapping uses).

## How it works
1. A caller (the interior transition, C40.2; a mission script; a load) asks the fader to
   **fade out** — ramp alpha to opaque over a duration.
2. When opaque, the caller does the hidden work (swap the world/interior, reposition the
   player).
3. The caller asks the fader to **fade in** — ramp alpha back to transparent, revealing the new
   scene.

The fader draws late in the frame (over the world and often over the HUD) so nothing shows
through.

## Why it's built this way
Decoupling "cover the screen" (the fader) from "what happens while covered" (the interior swap,
the reset) lets one reusable fader serve every hidden transition. It also gives a natural place
to gate input and pause simulation during the swap.

## What happens if you bend it
- Shorten/lengthen the fade → snappier or more cinematic transitions.
- Change the colour → a white flash instead of black.
- Skip it → instant, visible swaps (can look glitchy as the interior pops in).
All reachable by hooking the fader's update/apply (C40.6).

## Cross-references
C40.2 (the events that drive it), C41 (the interior swap it hides), C33 (how the quad renders).
