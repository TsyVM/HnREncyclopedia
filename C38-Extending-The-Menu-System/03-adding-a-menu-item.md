# C38.3 — The Minimal Mod: Add a Menu Item

> The smallest useful menu mod: insert one new `GuiMenuItem` into an existing screen and handle its selection.
> No new screen, no new layout — a single entry that runs your code (or opens your screen, C38.4).

## The idea

An existing screen (say `CGuiScreenPauseOptions` `0x0060E28C`) builds its `CGuiMenu` of `GuiMenuItem`s when it
initializes. If you **hook the build step** and append your own item, it appears in the list; if you **hook the
selection/input step** and recognize your item, you run your code when it's chosen. Two hooks, done.

## Steps

1. **Pick the host screen.** Where should the entry appear? Main menu (`CGuiScreenMainMenu` `0x0060FAAC`),
   pause options (`CGuiScreenPauseOptions` `0x0060E28C`), or the settings hub (`CGuiScreenPauseSettings`
   `0x0060E224`). Remember the front-end/pause split (C37.5): add to both if you want it in both.

2. **Recover the vtable slots.** Use SAHRDiag/DonutsSDK (C28.7) to find the slot indices for the screen's
   *build/populate* method (where items are added) and its *input/handle-select* method. Do this per build —
   addresses are specific to your exe (C28.6).

3. **Hook the build method.** In your detour, call the original first (so the stock items exist), then create a
   `GuiMenuItemText` with your label (a localized string, C22) and append it to the screen's `CGuiMenu`.

4. **Hook the input/select method.** When the highlighted item is yours, run your action — toggle a feature,
   open your screen (C38.4), or show a prompt — then return handled; otherwise call the original.

5. **Undo on unload.** Remove your hooks and your item when your mod unloads, so the menu returns to stock
   (VanHooks `remove`, C28.5).

## Sketch (DonutsSDK + VanHooks)

```cpp
// Add a "Mods" row to the pause Options screen and act on it.
#include <donutsdk/mod.hpp>
#include <vanhooks/vanhooks.hpp>
using namespace donutsdk;

const shar::db::ClassInfo* kPauseOpts =
    shar::db::find_class("CGuiScreenPauseOptions");     // vtable 0x0060E28C

// slot indices recovered from the vtable via SAHRDiag (build-specific!)
constexpr std::size_t kBuildSlot  = /* screen build/populate */ 0;
constexpr std::size_t kInputSlot  = /* screen handle-input   */ 0;

static BuildFn  orig_build  = nullptr;
static InputFn  orig_input  = nullptr;
static void*    g_myItem    = nullptr;

void __fastcall hk_build(void* self, void*) {
    orig_build(self);                                   // stock items first
    g_myItem = gui::append_text_item(self, "MODS");     // your helper over CGuiMenu/GuiMenuItem
}

int __fastcall hk_input(void* self, void*, int ev) {
    if (gui::selected_item(self) == g_myItem && gui::is_confirm(ev)) {
        mod::open_my_screen();                          // run code or push your screen (C38.4)
        return 1;                                       // handled
    }
    return orig_input(self, ev);
}
```

`gui::append_text_item` / `gui::selected_item` are thin helpers you write over the confirmed `CGuiMenu`
(`0x00610C08`) and `GuiMenuItem` (`0x00610BDC`) layouts — the SDK gives you the classes and the runtime member
offsets (C28.7) to implement them.

## What this gets you

A real, selectable entry in the stock menu that runs your code. For many mods (a cheat toggle, a debug action,
a "reload config" button) this is all you need. For a full sub-menu of your own options, pair it with a new
screen — next page.

## Cross-references

- **C38.2** — the build/input methods you hook.
- **C38.4** — making the item open a whole new screen.
- **C28.5 / C28.7** — the hooking mechanism and recovering slots/offsets.
