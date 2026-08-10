# Chapter 30 — GameFlow & the Load Sequence

> **Goal of this chapter:** answer "what happens between loading screens?" — decode the `GameFlow` context
> state machine that drives the game from boot to menu to gameplay, the `LoadingManager` that streams a
> level in, and how the engine transitions between these states.

Every time the screen fades to a loading bar and back, the game is walking a **state machine of contexts**.
This chapter decodes that machine from the verified RTTI set — **16 `Context` classes**, all with confirmed
vtable addresses (recovered in the SDK's latest data set) — and the managers that fill a level while you
wait.

**Key finding (✅ verified):** the game is always in exactly one **`Context`** (a state), driven by
**`GameFlow`**. The contexts form a clear graph: `EntryContext` → `BootupContext` (logos) →
`FrontEndContext` (menu) → `LoadingContext` (the loading screen) → `PlayingContext`/`GameplayContext`
(playing), with `PauseContext` overlaid. "Between loading screens" *is* the `LoadingContext`, where
`LoadingManager` streams the level's assets before handing off to gameplay.

---

## Deep-dive pages

- [C30.1 — The Context State Machine](01-context-state-machine.md): the 16 contexts and the `GameFlow` driver.
- [C30.2 — Boot to Menu](02-boot-to-menu.md): `EntryContext` → `BootupContext` → `FrontEndContext`.
- [C30.3 — The Loading Contexts](03-loading-contexts.md): what actually happens on the loading screen.
- [C30.4 — The `LoadingManager` & Streaming](04-loadingmanager-streaming.md): filling a level's residency.
- [C30.5 — Gameplay, Pause & the Frame](05-gameplay-pause-frame.md): `GameplayContext`, `PauseContext`, the update loop.

---

## 30.1 The context state machine (✅ verified)

The game's top-level state is a **`Context`**. The verified family, with vtable addresses:

```
Context : EventListener                 (0x006149E0)  — the base state
  ├ EntryContext        (0x006149BC)    — startup entry
  ├ ExitContext         (0x00614998)    — shutdown
  ├ BootupContext       (0x00614A04)    — logos (C20.2)
  ├ FrontEndContext     (0x0061494C)    — the main menu (C21)
  ├ LoadingContext      (0x006148F4)    — the LOADING SCREEN
  │   ├ LoadingGameplayContext   (0x0061473C)  — loading into gameplay
  │   ├ LoadingDemoContext       (0x006146E8)  — loading the demo
  │   └ LoadingSuperSprintContext(0x006146B8)  — loading the SuperSprint minigame
  ├ PlayingContext      (0x00614814)    — base "playing" state
  │   ├ GameplayContext          (0x0061476C)  — normal gameplay
  │   ├ DemoContext              (0x00614718)  — attract/demo mode
  │   └ SuperSprintContext       (0x00614694)  — the SuperSprint minigame
  └ PauseContext        (0x00614860)    — paused (overlay)
GameFlow : IRadTimerCallback  (0x00614634)  — drives the whole machine
```

`GameFlow` is the driver; each `Context` is a state with entry/update/exit behaviour (as an `EventListener`,
C23.3, it reacts to game events). [C30.1](01-context-state-machine.md).

## 30.2 Boot to menu (✅ verified)

The game starts in `EntryContext`, plays the logos in `BootupContext` (the FMV boot sequence, C20.2/C20.5),
then settles in `FrontEndContext` — the main menu, driven by `CGuiManagerFrontEnd` (C21.5). From the menu you
start a game, which transitions to a `LoadingContext`. [C30.2](02-boot-to-menu.md).

## 30.3 The loading contexts — "between loading screens" (✅ verified)

When you start or change a level, `GameFlow` enters a **`LoadingContext`** (or `LoadingGameplayContext`).
This is the answer to "what happens between loading screens": the game is *in a loading state*, showing
`CGuiScreenLoading` (C21.5), while `LoadingManager` (C30.4) streams the level's assets (C12.3) — terrain,
blocks, zones, characters, cars. When residency is satisfied, `GameFlow` transitions to `GameplayContext`.
[C30.3](03-loading-contexts.md).

## 30.4 The `LoadingManager` & streaming (✅ verified)

`LoadingManager : FileHandler::LoadFileCallback` (0x00613A7C) drives asset loading: it processes the level's
load requests (the `LoadP3DFile`/`LoadDisposableCar` calls, C14.2), pulls files through the VFS (C3.6), and
builds objects via the loader (C1.8). `GameplayManager` (0x00612D00) owns the running world. Streaming
residency (C12.3) is what a `LoadingContext` waits on. [C30.4](04-loadingmanager-streaming.md).

## 30.5 Gameplay, pause & the frame (✅ verified)

In `GameplayContext` the world updates each frame — physics (C26), AI (C25), missions (C16), rendering
(C10). Pausing overlays a `PauseContext` (the pause menu, `CGuiScreenPauseMission`, C21.5) that suspends the
gameplay update. The frame loop is where every runtime system (Part VII) ticks. [C30.5](05-gameplay-pause-frame.md).

---

## Key takeaways

- The game is a **`Context` state machine** driven by **`GameFlow`** — 16 verified contexts, each with a
  confirmed vtable address.
- The flow: `EntryContext` → `BootupContext` (logos) → `FrontEndContext` (menu) → **`LoadingContext`**
  (the loading screen) → `GameplayContext` (playing), with `PauseContext` overlaid.
- **"Between loading screens" is the `LoadingContext`**: `LoadingManager` streams the level's residency
  (C12.3) while `CGuiScreenLoading` is shown, then hands off to gameplay.
- Separate loading contexts exist for gameplay, demo, and SuperSprint — the game knows *what* it's loading.
- All classes ✅ from RTTI, now with ✅ vtable addresses; member offsets ⏳.

**Next:** [Chapter 31 — Police, Hit & Run & Wasps](../C31-Police-HitAndRun/C31-Police-HitAndRun.md).
