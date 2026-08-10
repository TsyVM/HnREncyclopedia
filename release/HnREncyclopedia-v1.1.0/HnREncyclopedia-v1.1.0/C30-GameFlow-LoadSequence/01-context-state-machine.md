# C30.1 — The Context State Machine

**What it is.** The top-level architecture of the running game: a **state machine** where each state is a
`Context` and the driver is `GameFlow`. Understanding it explains every screen transition — boot, menu,
loading, gameplay, pause — as one uniform mechanism.

**How it works (✅ verified).** `Context : EventListener` is the base state; `GameFlow : IRadTimerCallback`
runs the machine on a timer. The game is always in exactly one active context, and transitions swap it.
Verified vtable addresses make each state identifiable at runtime:

```
GameFlow (0x00614634) ── holds ──► current Context
Context (0x006149E0)
  EntryContext (0x006149BC)   ExitContext (0x00614998)
  BootupContext (0x00614A04)  FrontEndContext (0x0061494C)
  LoadingContext (0x006148F4) → LoadingGameplay/Demo/SuperSprint contexts
  PlayingContext (0x00614814) → GameplayContext / DemoContext / SuperSprintContext
  PauseContext (0x00614860)
```

Each context, being an `EventListener` (C23.3), reacts to events and manages its own entry, update, and exit.
A transition is: exit the current context, enter the next. `GameFlow` decides when — the menu's "start game"
event moves `FrontEndContext` → `LoadingContext`; load-complete moves `LoadingContext` → `GameplayContext`;
pause overlays `PauseContext`.

**Why a context state machine.** A game has fundamentally different modes — showing logos, in a menu,
loading, playing, paused — and each wants different input handling, rendering, and update logic. A state
machine captures this exactly: one active state, well-defined transitions, no ambiguity about "what mode am I
in?" It's the same pattern as the character AI FSM (C25.2), the mission stage machine (C16.2), and the camera
switcher (C26.4) — SHAR uses state machines throughout, and `GameFlow` is the top-level one that contains all
the others. When you're in `GameplayContext`, the character FSMs, mission machine, and camera switcher all
run *inside* that one context; when you pause, `PauseContext` suspends them.

**The three families of state.** The contexts group into three kinds:

- **Transitional** — `EntryContext`, `ExitContext`, `LoadingContext*` — brief states that move you between
  the real modes (startup, shutdown, loading).
- **Front-end** — `BootupContext`, `FrontEndContext`, `SuperSprintFEContext` — menus and non-gameplay UI.
- **Playing** — `PlayingContext` and its subclasses (`GameplayContext`, `DemoContext`,
  `SuperSprintContext`) — the actual interactive game, plus `PauseContext` as an overlay.

That `PlayingContext` has subclasses for *gameplay*, *demo* (the attract-mode footage that plays if you idle
at the menu), and *SuperSprint* (a top-down racing minigame) shows the game reuses the playing machinery for
three different experiences.

**What happens if you bend it.**

- *Rely on a context member offset* — the classes and vtables are ✅, member offsets ⏳. Diff (C4.3).
- *Assume you can be in two contexts at once* — it's one active context (with `PauseContext` as a defined
  overlay). Model modes as states, not overlaps.
- *Force a transition the machine doesn't define* — e.g. gameplay→menu without an exit — leaves state
  half-torn-down. Respect the entry/exit of each context.
