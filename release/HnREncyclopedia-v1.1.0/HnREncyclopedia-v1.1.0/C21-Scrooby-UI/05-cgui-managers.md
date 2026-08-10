# C21.5 — `CGui` Managers & Screens

**What it is.** The game's UI *logic* layer, sitting above Scrooby's rendering (C21.4): the `CGuiManager`s
that decide which screen is shown in which context, and the 60 `CGuiScreen` subclasses that implement each
screen's behaviour. This is the largest single class family in the game.

**How it works (✅ verified).** From `shar_dumps.csv`:

```
CGuiManager : CGuiEntity, Scrooby::GotoScreenCallback, EventListener   (base)
  ├ CGuiManagerFrontEnd    — the main menu / front-end
  ├ CGuiManagerInGame      — the in-game HUD & pause
  ├ CGuiManagerBackEnd     — the back-end (post-game, save)
  ├ CGuiManagerBootUp      — the boot sequence (logos, C20.2)
  ├ CGuiManagerLanguage    — language selection (C22)
  └ CGuiManagerMiniGame    — minigame UI
CGuiScreen : CGuiWindow, CGuiEntity   (base — 60 subclasses)
  CGuiScreenMissionSelect, CGuiScreenPauseMission, CGuiScreenVehicleGallery,
  CGuiScreenCardGallery, CGuiScreenMissionSuccess, CGuiScreenLoadGame, …
```

**One manager per context.** The seven `CGuiManager`s split the UI by *when* it's active: boot (logos),
front-end (menus), in-game (HUD/pause), back-end, language, minigame. Each is a `Scrooby::GotoScreenCallback`
(it can switch screens) and an `EventListener` (C23.3 — it reacts to game events). The manager decides which
Scrooby screen (C21.1) to display and drives its logic. When you pause mid-mission, `CGuiManagerInGame`
brings up `CGuiScreenPauseMission`; at the main menu, `CGuiManagerFrontEnd` shows the menu screens.

**60 screens.** Each `CGuiScreen` subclass is one screen's behaviour — what its buttons do, what data it
shows, how it transitions. The names read as a table of contents of the game's UI:
`CGuiScreenMissionSelect` (pick a mission, C16), `CGuiScreenVehicleGallery` (browse cars, C24),
`CGuiScreenCardGallery` (the collectible cards), `CGuiScreenMissionSuccess`/`MissionOver` (mission results),
`CGuiScreenLoadGame`/`AutoLoad` (saves, C27). The screen class is the *logic*; the Scrooby page (C21.1) is
its *appearance* — the same logic/presentation split as missions (C16) vs. their cameras (C14.6).

**Why this is the biggest family.** A console game with a front-end, a HUD, a pause menu, galleries, a card
collection, mission select, save/load, and language selection needs a lot of screens — and each is enough
behaviour to warrant its own class. 60 screens + 7 managers + the `Scrooby::`/`Fe` render layer (43) is ~110
UI classes, the single largest subsystem (C23.3). This reflects a real property of the game: it is
menu-heavy, with extensive galleries and collections, so the UI is a substantial fraction of the whole
codebase.

**The manager as a state machine.** A `CGuiManager` is effectively a screen state machine: it holds the
current `CGuiScreen`, handles input, and transitions to the next screen on events (`GotoScreenCallback`).
This mirrors the mission stage machine (C16.2) and the character AI FSM (C25.2) — the same "one active state,
event-driven transitions" pattern, applied to UI. Navigating menus *is* walking this state machine.

**What happens if you bend it.**

- *Rely on a `CGui` member offset or the manager singleton address* — classes ✅ (67), offsets/addresses ⏳.
  Diff (C4.3).
- *Add a screen page without a `CGuiScreen` to drive it* — it renders but does nothing. The page is
  appearance; the screen class is behaviour. You need both.
- *Confuse the manager and the screen* — the manager owns *which* screen; the screen owns *its* logic. Target
  the right one.
