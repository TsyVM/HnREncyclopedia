# C23.3 — Namespaces & Families

**What it is.** The organisation of the 1,207-class set into namespaces and prefix families, each mapping to
one subsystem this book documents. Reading the family a class belongs to tells you which chapter explains it.

**How it works (✅ verified counts).** Grouping the class names by namespace/prefix:

| Family | Classes | Subsystem | Chapter |
|---|--:|---|---|
| `CGui*` | 74 | UI screens, menus, HUD | C21 |
| `choreo::` | 46 | choreography & animation | C17 |
| `sim::` | 39 | physics & collision | C26 |
| `ActionButton::` | 36 | context actions (talk, enter, use) | C17/C25 |
| `Fe*` | 31 | front-end (menus, gallery) | C21 |
| `GuiSFX::` | 22 | UI transitions/effects | C21 |
| `Scrooby::` | 11 | the Scrooby UI engine | C21 |
| `Hud*` | 9 | in-game HUD elements | C21/C29 |
| `Sound`, `radmusic`, `poser`, `Scenegraph` | — | audio, posing, scene graph | C10/C17/C19 |

Beyond namespaces, *role* families cut across: **117** classes derive from `EventListener` (the event/
messaging system — objects that react to game events), **386** from `tRefCounted` (lifetime). So a class has
two coordinates: its *namespace* (which subsystem) and its *role bases* (what capabilities it has —
listens to events, is refcounted, is drawable, is a scene entity).

**Why namespaces map to subsystems.** Radical organised the code by subsystem, and the namespaces preserve
that: everything UI is `CGui*`/`Fe*`/`Scrooby::`, everything physics is `sim::`, everything animation-staging
is `choreo::`. This is a gift to reverse engineering — the namespace of a class you meet at runtime tells you
its purpose and its chapter before you know anything else about it. It also reveals the *weight* of each
subsystem: the UI (`CGui*` + `Fe*` + `GuiSFX::` + `Scrooby::` = ~130 classes) is the single largest, which
fits a console game with extensive menus, a card gallery, and a mission front-end.

**The `EventListener` web.** That 117 classes listen to events shows the runtime is **event-driven**:
missions, HUD, AI, and UI all react to a shared event stream (mission stage changed, vehicle entered, damage
taken). This is why the mission system (C16) can be data-defined — the objectives and conditions are event
listeners watching for the events that satisfy or fail them. Understanding the event web is understanding how
the game's systems communicate.

**What happens if you bend it.**

- *Guess a class's purpose from its name alone* — the namespace is more reliable; a `CGui*` class is UI
  regardless of what it's named. Use the family.
- *Ignore the role bases* — two `CGui*` classes differ by whether they're `EventListener`s or
  `LoadingManager` callbacks. The bases tell you the capability. Read them.
- *Assume namespace boundaries are firm* — some classes bridge (a `CGuiScreenVehicleGallery` touches both
  UI and vehicles). Cross-references are real; follow the inheritance.
