# Chapter 38 — Extending the Menu System: Adding Your Own Screens

> **Goal of this chapter:** show how a modder can add their **own menu** to the game — a new selectable entry
> in the internal menu (main menu or pause) that opens a custom screen of options or actions you invented.
> Where C37 documented the *existing* settings screens, this chapter documents the *machinery* behind all of
> them, so you can build a new one and wire it into the flow.

The menus you see in SHAR are not hard-coded pixels — they are a small, layered **UI object system**, every
layer of which is a confirmed C++ class in `Simpsons.exe`. Once you understand the stack — system → manager →
screen → menu → item — adding your own screen is a matter of (1) building a new screen, (2) giving it a layout,
and (3) registering it and pointing an item at it. This chapter covers both the minimal approach (inject one
item into an existing screen) and the full approach (a whole new screen class).

**Key finding (✅ verified):** the UI is a five-layer stack of confirmed classes — `CGuiSystem` (`0x0061062C`)
owns a per-context `CGuiManager` (`0x00610C48`; e.g. `CGuiManagerFrontEnd`, `CGuiManagerInGame`), which owns
`CGuiScreen`s (`0x00610A74` base), each holding a `CGuiMenu` (`0x00610C08`) of `GuiMenuItem`s (`0x00610BDC`).
Each screen is backed by a **Scrooby** layout via `FeProject` (`0x005F451C`) / `FeScreen` (`0x005F4190`). Every
one of these has a known vtable, so DonutsSDK + VanHooks (C28.5) can hook the exact methods needed to slot in a
new item and a new screen — no engine source required.

---

## Deep-dive pages

- [C38.1 — The Menu Object Stack](01-menu-architecture.md): the five confirmed layers (system → manager → screen → menu → item) and the Scrooby layout behind them.
- [C38.2 — Screen Lifecycle & Transitions](02-screen-lifecycle.md): how a screen is created, shown, updated, and switched — the virtual methods you hook.
- [C38.3 — The Minimal Mod: Add a Menu Item](03-adding-a-menu-item.md): inject one new `GuiMenuItem` into an existing screen and handle its selection.
- [C38.4 — Adding a Whole New Screen](04-adding-a-new-screen.md): a new `CGuiScreen` subclass, its layout, and registering it with the manager.
- [C38.5 — Worked Example: a "Mods" Menu](05-worked-example.md): a DonutsSDK + VanHooks mod that adds a Mods entry opening a custom options screen.
- [C38.6 — Pitfalls & Discipline](06-pitfalls.md): context mirroring, ownership/lifetime, re-verify per build, single-player.

---

## 38.1 The menu object stack (✅ verified)

```
CGuiSystem            0x0061062C   the UI system (one, owns the managers)
  └─ CGuiManager      0x00610C48   per GameFlow context:
        CGuiManagerFrontEnd / CGuiManagerInGame / CGuiManagerBootUp / …
        └─ CGuiScreen 0x00610A74   a full screen (MainMenu, Options, Pause, …)
              └─ CGuiMenu   0x00610C08   a selectable list within the screen
                    └─ GuiMenuItem 0x00610BDC   one row (text/sprite variants)
   backing layout:  FeProject 0x005F451C  →  FeScreen 0x005F4190   (Scrooby, C21)
```

Every screen in C37 and every menu in the game is an instance of this stack. [C38.1](01-menu-architecture.md).

## 38.2 Lifecycle (✅ verified shape)

A `CGuiScreen` is a `CGuiEntity` (`0x00610C84`) with virtual methods for enter/exit/update/draw and input. The
manager keeps a **stack** of screens; opening a menu pushes a screen, backing out pops it. Transitions are
requested through the manager, not by screens poking each other. The specific hookable virtuals are in
[C38.2](02-screen-lifecycle.md).

## 38.3 Minimal mod — add an item (✅ practical)

The smallest useful mod adds a `GuiMenuItem` to an existing screen (e.g. `CGuiScreenMainMenu` `0x0060FAAC` or
`CGuiScreenPauseOptions` `0x0060E28C`) and handles its selection to run your code or open your screen. You hook
the screen's build/populate method to append the item and its input handler to catch the selection.
[C38.3](03-adding-a-menu-item.md).

## 38.4 New screen (✅ practical)

For a real menu of your own, subclass `CGuiScreen`, back it with a Scrooby layout (reuse an existing `FeScreen`
or add a `.pag` page, C21), register the instance with the appropriate `CGuiManager`, and transition to it from
your item. [C38.4](04-adding-a-new-screen.md).

## 38.5 Worked example (✅ end-to-end)

[C38.5](05-worked-example.md) walks a complete DonutsSDK + VanHooks mod: a **"Mods"** entry added to the pause
Options screen that opens a custom screen with your own toggles, reading/writing your own config.

## 38.6 Pitfalls (✅ honest)

Front-end and pause menus are **separate** screen instances (C37.5), so a menu you want in both places must be
added twice. Screens are engine-owned — respect their lifetime, restore anything you hook, and re-verify
addresses per build. [C38.6](06-pitfalls.md).

---

## What this chapter establishes

- The menu system is a **five-layer stack of confirmed classes**, each with a known vtable — fully hookable.
- Adding a menu ranges from **one injected `GuiMenuItem`** (minimal) to a **new `CGuiScreen` subclass** (full).
- The practical path is **DonutsSDK + VanHooks** (C28.5) hooking the screen's build/input methods, plus a
  **Scrooby layout** (C21) for the visuals.
- Context mirroring, ownership, and per-build re-verification are the discipline that keeps it safe (C28.6).

**Cross-references:** C21 (Scrooby UI / `.pag` layouts), C22 (fonts & localized text for your labels), C37
(the existing settings screens you'll sit beside), C28.5/C28.7 (DonutsSDK hooking + SAHRDiag runtime evidence),
C30 (the GameFlow contexts that own the managers).
