# C38.1 — The Menu Object Stack

> The whole UI is five layers of confirmed classes plus a Scrooby layout. Know this stack and every menu in the
> game — including the one you want to add — has an obvious place to live.

## The five layers (✅ verified vtables)

| Layer | Class | vtable VA | Role |
|---|---|---|---|
| System | `CGuiSystem` | `0x0061062C` | the single UI system; owns the managers, pumps update/draw |
| Manager | `CGuiManager` | `0x00610C48` | one per GameFlow context; owns and stacks screens |
| Screen | `CGuiScreen` | `0x00610A74` | a full-screen page (MainMenu, Options, Pause, HUD…) |
| Menu | `CGuiMenu` | `0x00610C08` | a selectable list inside a screen |
| Item | `GuiMenuItem` | `0x00610BDC` | one selectable row (text / sprite) |
| (base) | `CGuiEntity` | `0x00610C84` | common base for screens/menus/items |
| (backing) | `FeProject` / `FeScreen` | `0x005F451C` / `0x005F4190` | the Scrooby layout resources (C21) |

## The managers — one per context (✅ verified)

`CGuiManager` is abstract; the game runs a concrete manager per GameFlow context (C30). All are confirmed
classes:

| Manager | Context | Owns |
|---|---|---|
| `CGuiManagerBootUp` | boot / legal / intro | splash, license, intro-transition screens |
| `CGuiManagerFrontEnd` | title / menus | main menu, options, load, mission-select |
| `CGuiManagerInGame` | gameplay + pause | HUD, pause, pause-settings screens |
| `CGuiManagerMiniGame` | 2-player bonus | mini HUD/menu/pause |
| `CGuiManagerLanguage` | first-run locale | language selection |
| `CGuiManagerBackEnd` | shutdown / teardown | end screens |

**This is the single most important fact for menu modding:** *which manager owns your screen decides where and
when it appears.* A "Mods" menu on the title screen belongs to `CGuiManagerFrontEnd`; the same menu in the
pause menu belongs to `CGuiManagerInGame`. That is why front-end and pause menus are mirrored (C37.5) — they
live under different managers.

## The screen — a `CGuiEntity` with a lifecycle

Every screen derives `CGuiEntity` (`0x00610C84`) and adds the screen behaviour: enter, exit, update, draw, and
input handling as virtual methods (C38.2). A screen typically owns one or more `CGuiMenu`s and binds to a
`FeScreen` for its visuals.

## The menu and its items

`CGuiMenu` (`0x00610C08`, plus `CGuiMenu2D` and `CGuiMenuPrompt` variants) holds an ordered list of
`GuiMenuItem`s (`0x00610BDC`). The item has typed variants seen live in the SAHRDiag capture (C28.7):

- `GuiMenuItemText` — a text row (label from the localized string table, C22).
- `GuiMenuItemSprite` — a row backed by a sprite/icon.

Selecting an item fires its action — which, for a navigation item, asks the manager to push another screen.

## The Scrooby backing (✅ verified)

The *visuals* of a screen are authored, not coded: a **Scrooby** project (`FeProject` `0x005F451C`) contains
`FeScreen`s (`0x005F4190`) — the `.pag`/`.fe` layout resources documented in C21. A `CGuiScreen` binds to a
`FeScreen` for its background, frames, and text placement. This split (behaviour in the class, layout in
Scrooby) is exactly why adding a menu is two jobs: **a class** and **a layout**.

## How it all fits

```
CGuiSystem
  ├─ CGuiManagerFrontEnd ── stack ─► CGuiScreenMainMenu ─► CGuiScreenOptions ─► CGuiScreenDisplay
  │                                     │ owns
  │                                     └─ CGuiMenu ─► [ GuiMenuItemText "Play", "Options", "Quit", … ]
  └─ CGuiManagerInGame  ── stack ─► CGuiScreenPause ─► CGuiScreenPauseOptions ─► …
        backing:  FeProject ─► FeScreen (Scrooby layout, C21)
```

To add your menu you insert a new `GuiMenuItem` into one of those `CGuiMenu`s, and (optionally) a new
`CGuiScreen` for it to open — the next pages.

## Cross-references

- **C21 — Scrooby UI**: the `FeProject`/`FeScreen` layout side.
- **C30 — GameFlow**: the contexts that decide which manager is live.
- **C37.1** — the concrete settings screens built on this stack.
