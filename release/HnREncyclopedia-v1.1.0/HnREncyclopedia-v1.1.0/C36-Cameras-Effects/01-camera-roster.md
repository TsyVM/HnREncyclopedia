# C36.1 — The Full Camera Roster

**What it is.** The complete set of cameras — 41 `SuperCam` subclasses (C26.3), one for every way the game
frames the action. Where C26.3 named the common ones, this page is the full roster, categorized by use.

**How it works (✅ verified).** Every camera derives from `SuperCam` (C26.3), grouped by purpose:

**Driving cameras** — frame the car while driving:
```
ChaseCam       — the default follow-behind view
BumperCam      — bumper/hood (first-person driving)
FollowCam      — follows the car
WrecklessCam   — a dramatic angle for reckless/high-speed driving and jumps (C35.3)
ReverseCam     — frames the car while reversing (C35.1 ReverseEngineState)
```

**On-foot cameras** — frame the character:
```
WalkerCam      — the third-person on-foot camera (player walking)
ComedyCam      — a comedic framing (WalkerCam subclass)
```

**Cinematic cameras** — scripted/authored shots:
```
AnimatedCam / RelativeAnimatedCam  — keyframed camera moves (C36.5)
ConversationCam — frames dialogue (C14.6)
RailCam        — follows a set path/rail (C36.5)
TrackerCam     — tracks a moving target
StaticCam      — a fixed camera at a placed locator (StaticCamLocator)
```

**Special cameras**:
```
HudMapCam      — renders the 3-D minimap (C29.1)
SuperSprintCam — the top-down SuperSprint minigame view (C30.5)
DebugCam       — the developer free-fly camera
KullCam / PCCam — specialised/platform cameras
```

Plus the managers: `SuperCamCentral` (switching, C36.2), `SuperCamController` (input), and `CameraPlayer`
(plays animated cameras, C36.5).

**Why so many cameras.** A game that is driving *and* on-foot *and* cutscene-heavy *and* has minigames needs
a camera tuned for each situation — and each is a small, focused behaviour better as its own class than as a
mode on one mega-camera (the same reasoning as the engine states, C35.1, and the GameFlow contexts, C30.1).
`ChaseCam` trails a car; `WalkerCam` orbits a character; `ConversationCam` composes a two-shot; `RailCam`
glides along a track; `HudMapCam` looks straight down for the minimap. Adding a new framing is adding a
`SuperCam` subclass, and the switcher (C36.2) treats them all uniformly. The 41 cameras are the game's entire
visual grammar — every moment you play is framed by one of them.

**Reading the roster.** The camera in use tells you the game's mode: `ChaseCam`/`BumperCam` = driving,
`WalkerCam` = on foot, `ConversationCam` = a story beat, `WrecklessCam` = you're doing something dramatic,
`SuperSprintCam` = the minigame. This mirrors the GameFlow contexts (C30) and engine states (C35) — the active
camera reflects the active gameplay state, because `SuperCamCentral` switches it in response to those states
(C36.4).

**What happens if you bend it.**

- *Rely on a camera member offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Expect one camera to serve every situation* — the system is many focused cameras switched by context
  (C36.2). Add a framing as a subclass.
- *Confuse a camera with its data* — the behaviour is the `SuperCam`; its tuning is the `*Data` (C36.2). Edit
  the right one.
