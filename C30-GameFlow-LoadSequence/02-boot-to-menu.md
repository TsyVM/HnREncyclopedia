# C30.2 — Boot to Menu

**What it is.** The first stretch of the state machine: from launching the executable to sitting at the main
menu, ready to play. Three contexts, in order, each verified.

**How it works (✅ verified).** The sequence:

1. **`EntryContext`** (0x006149BC) — the very first state. The engine initialises: RadCore starts, the
   RadSound HAL (C18.5) comes up, the VFS mounts the archives (C3.6), the class system is ready. This is the
   pre-anything state before a single frame is drawn.
2. **`BootupContext`** (0x00614A04) — the logo sequence. The licensor/studio FMVs (Fox, Radical, VU, Gracie,
   C20.2) play as movie states (C20.5), driven by `CGuiManagerBootUp` (C21.5). This is where the legally
   required attributions run before the player reaches anything interactive.
3. **`FrontEndContext`** (0x0061494C) — the main menu. Driven by `CGuiManagerFrontEnd` (C21.5), showing the
   Scrooby front-end screens (C21): new game, load game, options, galleries. The game idles here until the
   player acts — or, if they idle too long, transitions to `DemoContext` (attract mode, C30.1).

From `FrontEndContext`, choosing to start or load a game fires the event that moves `GameFlow` into a
`LoadingContext` (C30.3).

**Why a distinct boot chain.** Separating entry, boot, and front-end into three contexts matches three
distinct jobs: *initialise the engine* (entry), *show legal/branding video* (boot), *present the menu*
(front-end). Each has different needs — entry draws nothing, boot plays video and must be skippable, the menu
is fully interactive UI. Making them separate contexts means each is self-contained and the transitions are
clean: engine-ready moves entry→boot, video-done moves boot→front-end, start-game moves front-end→loading.
It also means the boot logos can't be reached from gameplay (you don't re-watch logos mid-game) because
there's no transition back — the graph only flows forward from boot.

**The attract-mode loop.** `FrontEndContext` → (idle timeout) → `DemoContext` → (input) → `FrontEndContext`
is the attract loop every arcade-descended game has: leave the menu alone and it plays demo footage
(`DemoContext`, a `PlayingContext` subclass running scripted `demo.mfk` content, C14), returning to the menu
on any input. This is why the game "plays itself" if you walk away at the menu — it's a defined state
transition, not a screensaver.

**What happens if you bend it.**

- *Skip or reorder the logo FMVs* — they're `BootupContext` content with licensing weight (C20.2). Handle
  with care.
- *Rely on a boot/menu context offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Break the front-end→loading transition* — the menu can't start a game. Keep the start-game event wired to
  the loading context.
