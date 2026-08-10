# C38.4 — Adding a Whole New Screen

> A real menu of your own — a page with its own list of options you invented. This means a new `CGuiScreen`, a
> layout for it, and registering it with the manager so it can be pushed.

## The three jobs

1. **A screen object** — something that behaves like a `CGuiScreen` (`0x00610A74`): enters, updates, draws,
   handles input, exits.
2. **A layout** — the visuals, from Scrooby (`FeScreen` `0x005F4190`, C21): background, frames, text anchors.
3. **Registration + transition** — the screen must be known to a `CGuiManager` (`0x00610C48`) so an item
   (C38.3) can push it onto the stack.

There are two ways to get the screen object, trading effort for cleanliness.

### Approach A — repurpose an existing screen (easiest)

Reuse a simple stock screen as your canvas. `CGuiScreenMessage`, `CGuiScreenPrompt`, or one of the settings
screens already know how to lay out a menu of items and take input. Hook its build method to replace its items
with **yours**, and its title/text to your labels. You inherit all the lifecycle and layout for free; you only
supply content. Best when your menu is "a list of toggles/actions" — which most mod menus are.

### Approach B — a genuine new `CGuiScreen` subclass (cleanest)

Author a new class that presents as a `CGuiScreen`: build a vtable whose lifecycle slots (C38.2) point at your
functions, allocate an instance, and bind it to a Scrooby `FeScreen` you added to the front-end project (a new
`.pag` page, C21). This is a true new screen with no host to share behaviour with — more work (you implement
enter/update/draw/input), but no risk of disturbing a stock screen.

## Registering & transitioning

However you obtain the screen, it becomes reachable the same way:

1. **Get the live manager.** For a title-screen menu, the `CGuiManagerFrontEnd`; for pause, the
   `CGuiManagerInGame` (C38.1). DonutsSDK can locate the live manager instance by vtable (C28.7).
2. **Push on selection.** From your injected item's action (C38.3), call the manager's *push-screen* path with
   your screen. The manager runs your screen's enter transition and gives it focus.
3. **Pop on back.** Your screen's input handler requests a pop (or the manager's standard back handling does)
   when the player exits, returning to the menu beneath.

```cpp
// From the item action (C38.3):
void open_my_screen() {
    void* mgr = gui::current_manager();     // CGuiManagerInGame / FrontEnd (by vtable, C28.7)
    void* scr = my::build_mods_screen();    // Approach A (repurpose) or B (new subclass)
    gui::push_screen(mgr, scr);             // thin helper over CGuiManager's push path
}
```

`gui::push_screen` / `gui::current_manager` are helpers over the confirmed `CGuiManager` layout; recover the
push method's slot with SAHRDiag (C28.7).

## Giving it content

Your screen holds a `CGuiMenu` (`0x00610C08`) of `GuiMenuItem`s (`0x00610BDC`) — the same primitives as any
stock menu. Populate it with your toggles/actions, each with its own action closure. Labels come from the
localized string table (C22) or, for a mod, a string you supply directly. Persist your options to your own
config file (mirroring `simpsons.ini`, C27.4) so they survive a restart.

## Which approach to choose

- **A "Mods" list of toggles** → Approach A (repurpose). Fastest, robust, recommended for most mods.
- **A distinctly-styled, standalone screen** → Approach B (new subclass + new Scrooby page). More control, more
  work.

The worked example (C38.5) uses Approach A end-to-end.

## Cross-references

- **C21 — Scrooby UI**: adding/using a `FeScreen` layout.
- **C38.1 / C38.2** — the manager, screen stack, and lifecycle.
- **C28.7 — SAHRDiag**: locating live managers and recovering push/lifecycle slots.
