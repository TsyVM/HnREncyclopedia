# C38.5 — Worked Example: a "Mods" Menu

> End-to-end: a DonutsSDK + VanHooks mod that adds a **"Mods"** entry to the pause Options screen, which opens a
> custom screen with your own toggles, backed by your own config. Uses Approach A (repurpose a stock screen) so
> the example stays focused on the wiring, not on re-implementing a screen.

## What we're building

```
Pause ▸ Options ▸ [ Display  Sound  Controller  Language  MODS ]   ← we add "MODS"
                                                        │ select
                                                        ▼
                     ┌ MODS ─────────────────────────────┐
                     │  Unlimited Sprint     : ON         │   ← our toggles
                     │  Free Camera          : OFF        │
                     │  Reload Config                     │
                     │  Back                              │
                     └────────────────────────────────────┘
```

## Pieces

1. A hook on `CGuiScreenPauseOptions` (`0x0060E28C`) build → append a **MODS** `GuiMenuItemText`.
2. A hook on its input → on MODS selected, push our screen.
3. Our screen = a repurposed `CGuiScreenMessage`/settings screen whose items are our toggles.
4. A tiny config file (`mods.ini`) so toggles persist (mirrors `simpsons.ini`, C27.4).

## Code (illustrative)

```cpp
#include <donutsdk/mod.hpp>
#include <donutsdk/game/shar/member_offsets.hpp>
#include <vanhooks/vanhooks.hpp>
using namespace donutsdk;

// ---- config ---------------------------------------------------------------
struct ModConfig { bool unlimitedSprint=false, freeCam=false; };
static ModConfig g_cfg;

// ---- our screen (Approach A: repurpose) -----------------------------------
static void* build_mods_screen() {
    void* scr = gui::clone_screen("CGuiScreenPauseSettings");   // reuse a list screen
    gui::set_title(scr, "MODS");
    gui::clear_items(scr);
    gui::add_toggle(scr, "Unlimited Sprint", &g_cfg.unlimitedSprint);
    gui::add_toggle(scr, "Free Camera",      &g_cfg.freeCam);
    gui::add_action(scr, "Reload Config",    []{ cfg_load(&g_cfg, "mods.ini"); });
    gui::add_action(scr, "Back",             []{ gui::pop_screen(gui::current_manager()); });
    return scr;
}

// ---- host-screen hooks (C38.3) --------------------------------------------
static gui::BuildFn orig_build; static gui::InputFn orig_input; static void* g_item;

void __fastcall hk_build(void* self, void*) {
    orig_build(self);
    g_item = gui::append_text_item(self, "MODS");
}
int __fastcall hk_input(void* self, void*, int ev) {
    if (gui::selected_item(self) == g_item && gui::is_confirm(ev)) {
        gui::push_screen(gui::current_manager(), build_mods_screen());
        return 1;
    }
    return orig_input(self, ev);
}

// ---- install --------------------------------------------------------------
void mods_menu() {
    mod::Log log{"mods_menu.log"};
    cfg_load(&g_cfg, "mods.ini");

    const shar::Image& game = shar::process();
    const auto* host = shar::db::find_class("CGuiScreenPauseOptions");   // 0x0060E28C
    void** vt = reinterpret_cast<void**>(game.rebase(host->vtable_va));

    auto& eng = vanhooks::global_engine();
    eng.hook_vtable({ .vtable=vt, .slot_index=kBuildSlot, .tag="PauseOptions::build" },
                    &hk_build, reinterpret_cast<void**>(&orig_build));
    eng.hook_vtable({ .vtable=vt, .slot_index=kInputSlot, .tag="PauseOptions::input" },
                    &hk_input, reinterpret_cast<void**>(&orig_input));
    log.print("mods menu installed\n");
}
DONUTSDK_MOD(mods_menu)
```

The `gui::*` helpers are the only thing you implement yourself; each is a few lines over the confirmed
`CGuiManager` / `CGuiScreen` / `CGuiMenu` / `GuiMenuItem` layouts, using the runtime member offsets SAHRDiag
recovered (C28.7). `kBuildSlot` / `kInputSlot` come from reading the host screen's vtable on **your** build.

## Applying the toggles

The toggles just set booleans; a separate part of your mod reads them each frame (e.g. a hook on the player or
camera update, C35/C36) and acts — that logic is independent of the menu and out of scope here. The menu's job,
which this example completes, is to let the player **see and change** your options from inside the game's own UI.

## Result

A stock-looking **MODS** entry sits with Display/Sound/Controller/Language; selecting it opens a page of your
toggles that persists to `mods.ini`. To also expose it on the title screen, repeat the two hooks on
`CGuiScreenOptions` (`0x0060F908`) under `CGuiManagerFrontEnd` (C37.5 / C38.6).

## Cross-references

- **C38.3 / C38.4** — the item-injection and screen-open mechanics this assembles.
- **C28.5 / C28.7** — DonutsSDK + VanHooks and the runtime offsets behind the `gui::*` helpers.
- **C27.4** — the `simpsons.ini`-style config the toggles persist to.
