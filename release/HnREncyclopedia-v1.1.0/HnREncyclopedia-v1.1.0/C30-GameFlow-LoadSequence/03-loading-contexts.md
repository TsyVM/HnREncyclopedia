# C30.3 — The Loading Contexts

**What it is.** The direct answer to "what happens between loading screens?" — the `LoadingContext` family,
the states the game occupies *while the loading bar is on screen*. This is not dead time; it's a working
state streaming a level into memory.

**How it works (✅ verified).** When you start a game, change level, or enter a minigame, `GameFlow`
transitions into a loading context — verified with their vtable addresses:

```
LoadingContext (0x006148F4)
  ├ LoadingGameplayContext    (0x0061473C)  — loading a normal gameplay level
  ├ LoadingDemoContext        (0x006146E8)  — loading the demo/attract content
  └ LoadingSuperSprintContext (0x006146B8)  — loading the SuperSprint minigame
```

While in a loading context, three things happen at once:

1. **The loading screen is shown** — `CGuiScreenLoading` / `CGuiScreenLoadingFE` (C21.5), a Scrooby screen
   (C21) with progress feedback.
2. **`LoadingManager` streams the assets** (C30.4) — it processes the level's load list (the
   `LoadP3DFile`/`LoadDisposableCar` calls, C14.2), pulling terrain, world blocks, streamed zones/roads
   (C12.3), characters (C8), and cars (C7/C15) through the VFS (C3.6) and building them via the loader (C1.8).
3. **`GameFlow` waits** — the loading context doesn't advance until residency is satisfied (the required
   assets are loaded).

When loading completes, `GameFlow` transitions `LoadingContext` → `GameplayContext` (C30.5) and the world
appears. That fade-in from the loading bar *is* this transition.

**Why separate loading contexts per target.** There's a distinct loading context for *gameplay*, *demo*, and
*SuperSprint* because each loads a **different asset set** and hands off to a **different playing context**.
`LoadingGameplayContext` → `GameplayContext`; `LoadingSuperSprintContext` → `SuperSprintContext`. The loading
context knows *what it's loading and where it's going*, so it can request the right assets and target the
right next state. This is cleaner than one generic loader with mode flags — the context *is* the mode, and
the transition target is implied by which loading context you're in.

**Why loading is a whole state.** Loading a level is not instantaneous on 2003 hardware — it's tens of MB of
terrain, blocks, and characters streamed from disc (C12). Making it an explicit state (rather than a blocking
call) lets the engine keep drawing the loading screen and its progress, keep the audio going, and stay
responsive to a cancel — all while the `LoadingManager` works in the background. The loading screen you watch
is the `LoadingContext` doing exactly this: presenting UI while streaming underneath.

**What happens if you bend it.**

- *Assume loading is instant/blocking* — it's a streaming state (C30.4). A mod that adds heavy assets extends
  the time spent in the loading context. Budget accordingly (C12.3).
- *Rely on a loading-context offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Route a level to the wrong loading context* — it loads the wrong asset set and targets the wrong playing
  state. Match the loading context to the target mode.
