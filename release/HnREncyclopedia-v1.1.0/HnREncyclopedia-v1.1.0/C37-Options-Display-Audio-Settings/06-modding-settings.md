# C37.6 — Modding the Settings

> Every setting is plain text in `simpsons.ini` and every screen is a confirmed class, so the *values* are
> trivially moddable and the *screens* are hookable. This page covers value-level mods (file edits) and points
> at C38 for adding whole new menus.

## Value-level mods (edit `simpsons.ini`)

Because the config is text (C27.4), most "settings mods" are just file edits — no code required. Close the game
first (it rewrites the file on exit and would overwrite your changes).

**Widescreen / custom resolution.** `resolution` is a string the menu never validates against its own list:

```ini
#System
display=fullscreen
resolution=1920x1080     ; any WxH the display driver accepts
bpp=32
```

The device will try to create that back-buffer; if the driver supports the mode it works even though the menu
would never have offered it. This is the basis of community widescreen patches (paired with a HUD/FOV fix,
since the HUD and cameras assume 4:3 — C36).

**Brightness past the slider cap.** The Display screen clamps `gamma`; the file does not:

```ini
gamma=1.400000           ; brighter than the in-menu slider allows
```

**Per-bus audio.** Set any channel independently, including hard mute:

```ini
#Sound
music=0.000000           ; mute music, keep everything else
dialogue=1.000000
```

**Remap controls.** Using the decoded `buttonmap` grammar (C37.4), rebind any action to any DirectInput
scancode — e.g. arrow keys for steering:

```ini
buttonmap=0, 0: ( 1 200 0 )   ; DIK_UP    (0xC8 = 200) → forward
buttonmap=0, 1: ( 1 208 0 )   ; DIK_DOWN  (0xD0 = 208) → back
buttonmap=0, 2: ( 1 203 0 )   ; DIK_LEFT  (0xCB = 203) → left
buttonmap=0, 3: ( 1 205 0 )   ; DIK_RIGHT (0xCD = 205) → right
```

**Sensitivity & feel.** Tune `mousesensitivityx/y`, `wheelsensitivityx/y`, `invertmousex/y`, `mouselook`,
`useforcefeedback` directly.

## Screen-level mods (hook the class)

To change *behaviour* — a wider resolution list, an unclamped gamma slider, a new toggle — hook the settings
screen's class. Each `CGuiScreen*` has a confirmed vtable (C37.1), so DonutsSDK + VanHooks can intercept its
methods exactly as the `vanhooks_mod` example does (C28.5):

- Hook `CGuiScreenDisplay`'s "populate resolutions" or "apply" method to inject extra modes.
- Hook `CGuiScreenSound` to add a channel or change a slider's range.
- Read the live screen object's fields using the runtime member-offset evidence from SAHRDiag (C28.7).

## Adding a whole new menu

Editing values and hooking existing screens does **not** cover adding your *own* screen — a new entry the
player can select from the menu to reach options you invented. That is a larger task (a new screen class, a
Scrooby layout, and wiring it into the menu flow) and has its own chapter: **C38 — Extending the Menu System**.

## Safety

- Back up `simpsons.ini` and your `Save1` before editing.
- Edit with the game closed.
- A malformed `resolution`/`bpp` the driver rejects can fail device creation — keep a known-good line to
  restore. All of this is single-player, offline, on a copy you own (C28.6).

## Cross-references

- **C27.4 / C27.5** — the config file and safe editing.
- **C28.5 / C28.7** — DonutsSDK hooking and SAHRDiag runtime evidence.
- **C38** — building a new menu screen.
