# C30.5 — Gameplay, Pause & the Frame

**What it is.** The states where you actually play — `GameplayContext` and its siblings — and how the frame
loop ticks the whole runtime inside them, plus how `PauseContext` suspends it. This closes the chapter by
connecting the top-level state machine to every runtime system (Part VII).

**How it works (✅ verified).** In `GameplayContext` (0x0061476C, a `PlayingContext`), the game runs its
frame loop. Each frame, inside this one context, the runtime systems tick in order:

1. **Input** → controllers (C24.2/C25.3) read the player.
2. **AI** → `CharacterAi` (C25.2), `ChaseAI` (C31), traffic (C24.3) decide actions.
3. **Missions** → the `Mission` machine (C16/C26.1) advances stages on events.
4. **Physics** → `sim::` (C26.5) integrates, collision (C26.6) resolves.
5. **Streaming** → `LoadingManager` (C30.4) streams nearby zones (C12.3).
6. **Audio** → the sound frame (C19.5) mixes.
7. **Render** → the scene graph (C10.6) draws, then the HUD/UI (C21) composites.

Every runtime chapter (Part VII) is one step of this loop, and they all run *because* the game is in
`GameplayContext`. The context is the container; the systems are its contents.

**Pause as an overlay (✅ verified).** `PauseContext` (0x00614860) is entered on pause. It **suspends the
gameplay update** — physics, AI, missions, and streaming stop advancing — while presenting the pause menu
(`CGuiScreenPauseMission`, C21.5) and the full-screen map (`ViewMap`, C29.4). The world is frozen but still
drawn (you see the paused scene behind the menu). Unpausing returns to `GameplayContext` and the loop
resumes. Making pause its own context is what cleanly stops *everything* at once — one state change suspends
the whole runtime, rather than each system checking a pause flag.

**The three playing contexts.** `GameplayContext` (normal play), `DemoContext` (attract mode, C30.2), and
`SuperSprintContext` (the top-down racing minigame) all subclass `PlayingContext` and run variants of this
loop. `SuperSprintContext` runs a different camera and rules (a bird's-eye race); `DemoContext` runs scripted
input instead of the player's. Sharing `PlayingContext` means they share the world update machinery and
differ only in control and presentation — the same "one base, specialised leaves" design as the DSG entities
(C23.2) and the cameras (C26.3).

**Why the frame lives in the context.** Anchoring the frame loop in `GameplayContext` means the loop only
runs when you're actually playing — not during loading (the loading context runs a different, load-focused
loop) or the menu (the front-end runs UI). This is why pausing, loading, and menuing cleanly stop gameplay:
they're *different contexts*, and the gameplay frame loop simply isn't running in them. The context state
machine (C30.1) is thus the master switch for the entire runtime: which systems tick depends entirely on
which context is active.

**What happens if you bend it.**

- *Rely on a context/manager member offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Expect gameplay to update during pause or loading* — it doesn't; those are other contexts. Systems tick
  only in `GameplayContext`.
- *Add per-frame work without accounting for the loop order* — a system that reads stale data ran before its
  producer. Respect the frame order (input→AI→mission→physics→stream→audio→render).

**Next:** [Chapter 31 — Police, Hit & Run & Wasps](../C31-Police-HitAndRun/C31-Police-HitAndRun.md).
