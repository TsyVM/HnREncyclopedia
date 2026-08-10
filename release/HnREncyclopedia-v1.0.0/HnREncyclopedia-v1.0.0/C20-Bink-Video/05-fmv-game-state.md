# C20.5 — FMV as a Game State

**What it is.** How playing a movie fits into the running game — not as a passive file, but as a **state** the
game enters, plays through, and exits, wired into the mission system and the audio. This closes the video
chapter by connecting FMV to the rest of the engine.

**How it works (✅ verified).** Three verified pieces tie FMV to the game:

- **The `fmv` mission objective** (C16.3, 6 uses) — a mission stage whose objective is "play this cutscene."
  When the stage runs, the game enters the movie state, plays the named `.rmv` through `binkw32.dll` (C20.4),
  and completes the objective when the movie ends. So cutscenes are *scheduled by missions*, like any other
  objective (C16).
- **`NISSoundPlayer`** (C19.2) — "NIS" is **Non-Interactive Sequence**, Radical's term for a cutscene. This
  sound player handles the cutscene's audio, coordinating it with the video. (The in-engine cutscenes use the
  same NIS concept via `choreo::`, C25.4; the FMV path uses Bink's own interleaved audio, C20.1, with
  `NISSoundPlayer` managing the game-side integration.)
- **The movie state itself** — while a movie plays, normal gameplay is suspended: input maps to "skip," the
  world isn't simulated, and the movie owns the screen. When the movie ends (or is skipped), the game returns
  to the state that launched it — the next mission stage, or the menu after the logos.

**Why FMV is a state, not just playback.** A movie has to *interrupt* the game cleanly and *resume* it
cleanly: suspend simulation, take over rendering, handle skip, restore control. Modelling this as an explicit
game state (enter → play → exit) is the robust way — the same "flow as a state" pattern used for loading
screens and menus. The mission system (C16) launches the state via the `fmv` objective; the state plays the
Bink file (C20.4); the state exits back to the mission. This is why FMV integrates so cleanly with missions:
it's just another objective that happens to run a movie instead of a gameplay task.

**Logos as a boot state.** The startup logos (C20.2 — Fox, Radical, VU, Gracie) are the same movie state,
sequenced *before* the menu rather than by a mission: the boot flow plays them in order, each a movie state,
then transitions to the front-end (C21). This is why they're skippable the same way cutscenes are — they use
the identical state machinery.

**The whole video picture.** Putting C20 together: FMV is **16 `.rmv` files** (C20.2), **15 Bink** (C20.1) and
one `xobX` anomaly (C20.3), decoded by **`binkw32.dll`** (C20.4), and played as a **game state** launched by
the `fmv` mission objective (C16.3) or the boot sequence, with audio via `NISSoundPlayer` (here). Every tie is
verified; the codec internals and the `credits.rmv` container are the ⏳ parts.

**What happens if you bend it.**

- *Trigger an `fmv` objective with a missing/invalid movie* — the state has nothing to play and may hang or
  skip. Ensure the `.rmv` exists and is valid Bink (C20.4).
- *Rely on the movie-player/NIS class offsets* — the classes are ✅, offsets ⏳. Diff (C4.3).
- *Expect the world to simulate during a movie* — the movie state suspends gameplay. Don't depend on
  world updates while an FMV plays.

**Next:** [Chapter 21 — Scrooby UI](../C21-Scrooby-UI/C21-Scrooby-UI.md).
