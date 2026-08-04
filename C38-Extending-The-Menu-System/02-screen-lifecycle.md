# C38.2 — Screen Lifecycle & Transitions

> To add or hook a menu you intercept a screen's virtual methods. This page describes the lifecycle — how a
> screen is created, shown, updated, and switched — and which methods you target.

## The manager owns a screen stack (✅ verified shape)

`CGuiManager` (`0x00610C48`) keeps a **stack** of `CGuiScreen`s. Opening a menu **pushes** a screen; backing
out **pops** it, revealing the one beneath. Only the top screen (or top few, for overlays) receives input and
updates. Screens never switch themselves directly — they ask the manager to push/pop, which keeps navigation
centralized and reversible.

```
push Options → [ MainMenu, Options ]           (Options now on top)
push Display → [ MainMenu, Options, Display ]   (Display on top)
back         → [ MainMenu, Options ]            (Display popped)
```

## A screen's lifecycle (🟡 reasoned from the class shape)

`CGuiScreen` derives `CGuiEntity` (`0x00610C84`); both are polymorphic with vtables, so the lifecycle is a set
of virtual methods the manager calls. The shape, confirmed by the base classes and standard for this kind of UI
system, is:

| Phase | What happens | What you hook it for |
|---|---|---|
| **construct / init** | screen object created, binds its `FeScreen` layout | add your menu items, load your config |
| **enter / on-show** | screen pushed; runs intro transition, takes focus | start your feature, snapshot state |
| **update(dt)** | per-frame logic while on top of the stack | run your toggles, poll your inputs |
| **handle-input** | button/stick/mouse events routed to the focused menu | catch selection of your item |
| **draw** | the screen renders its `FeScreen` + menu | draw your extra widgets/labels |
| **exit / on-hide** | screen popped; runs outro, releases focus | apply/save your settings, undo hooks |
| **destroy** | screen object torn down | free anything you allocated |

The exact vtable slot indices are build-specific — recover them from the class's vtable with SAHRDiag/DonutsSDK
(C28.7) rather than hard-coding, then hook by slot as the `vanhooks_mod` example does (C28.5).

## Transitions (✅ verified pattern)

A navigation `GuiMenuItem`'s action calls into the manager to push the target screen. That is the seam you use
to open **your** screen: give your item an action that requests a push of your custom `CGuiScreen`
(C38.4), or — for the minimal mod — that simply runs your code and pops back (C38.3).

## Input focus & the menu

Within the focused screen, its `CGuiMenu` (`0x00610C08`) tracks the highlighted `GuiMenuItem` and moves the
selection on up/down, firing the item's action on confirm. When you inject an item (C38.3) you are adding to
this menu's list; when you add a screen you get your own menu with its own focus.

## Why hooking, not patching

Because every lifecycle method is *virtual*, you change behaviour by swapping vtable entries (non-destructive,
reversible — the VanHooks model, C28.5/SAHRDIAG_VTRACE), never by rewriting the screen's bytes. Your detour
runs, then calls the original, so the stock menu keeps working and your addition rides on top.

## Cross-references

- **C28.5 — DonutsSDK native mods** and **SAHRDIAG_VTRACE** — the vtable-hook mechanism.
- **C28.7 — SAHRDiag** — recovering the real vtable slot indices and live screen fields.
- **C38.3 / C38.4** — using these seams to add an item / a screen.
