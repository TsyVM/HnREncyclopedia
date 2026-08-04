# Chapter 37 — Options: Display, Audio, Controls & Graphics Settings

> **Goal of this chapter:** map the game's **Options menu system** — every settings screen the player can
> open, what each control changes, and how each choice is written back to `simpsons.ini`. Where Chapter 27
> decoded the *file*, this chapter decodes the *menus that write it*. After this you can find any option's
> screen class, its `.ini` key, and how to mod both.

Every setting the player can change lives behind a **Scrooby UI screen** (C21), and each of those screens is a
confirmed C++ class in `Simpsons.exe`. When the player moves a slider or picks a resolution, the screen writes
the value into `simpsons.ini` (C27.4) and applies it to the engine. This chapter connects the three: **screen
class → on-screen control → `.ini` key**.

**Key finding (✅ verified):** SHAR's PC options are a small, flat set of screens, all confirmed by RTTI with
known vtable addresses — a main **Options** hub (`CGuiScreenOptions` `0x0060F908`) branching to **Display**
(`CGuiScreenDisplay` `0x0060FD98`), **Sound** (`CGuiScreenSound` `0x0060F58C`), **Controller**
(`CGuiScreenController` `0x0060FE38`), and **Language** (`CGuiScreenLanguage` `0x0060D500`), each mirrored by a
pause-menu variant. **There is no separate "graphics quality" menu:** on PC the graphics settings *are* the
Display screen — resolution, colour depth (bpp), gamma, and windowed/fullscreen. No texture-detail, shadow,
draw-distance, or anti-aliasing options exist in the retail build. That is an accurate, sometimes surprising,
finding — SHAR is a faithful console port whose only video knobs are the four the Display screen exposes.

---

## Deep-dive pages

- [C37.1 — The Options Tree & Screen Classes](01-the-options-tree.md): the menu hierarchy, all 13 confirmed settings-screen vtables, and the front-end vs pause mirror.
- [C37.2 — Display & "Graphics" Settings](02-display-video.md): `CGuiScreenDisplay` — resolution, bpp, gamma, windowed/fullscreen, and the `#System` keys. Why there's no quality menu.
- [C37.3 — Audio Settings](03-audio.md): `CGuiScreenSound` — the five volume channels and the `#Sound` keys.
- [C37.4 — Controls & Input](04-controls.md): `CGuiScreenController` — button mapping, mouse/wheel sensitivity, invert, mouselook, force feedback.
- [C37.5 — Language, Pause Mirror & Memory Card](05-language-pause.md): `CGuiScreenLanguage`, the `Pause*` screen family, and the console-legacy save screens.
- [C37.6 — Modding the Settings](06-modding-settings.md): adding resolutions, forcing widescreen, unlocking hidden values, and re-skinning the menus.

---

## 37.1 The options tree (✅ verified)

Every settings screen is a confirmed `CGuiScreen*` subclass. The player reaches them from the main-menu (or
pause-menu) **Options** hub:

```
Options  (CGuiScreenOptions 0x0060F908)
├─ Display     CGuiScreenDisplay     0x0060FD98   → #System   (resolution, bpp, gamma, display)
├─ Sound       CGuiScreenSound       0x0060F58C   → #Sound    (sfx, music, ambience, dialogue, car)
├─ Controller  CGuiScreenController  0x0060FE38   → #Controller (buttonmap, sensitivity, invert, ffb)
└─ Language    CGuiScreenLanguage    0x0060D500   → (localisation selection)
```

Full class list and the pause-menu mirror are in [C37.1](01-the-options-tree.md).

## 37.2 Display & graphics (✅ verified)

`CGuiScreenDisplay` is the *entire* PC video-settings surface. It maps one-to-one to the `#System` section:

```ini
#System
display=window        ; window | fullscreen
resolution=1600x1200  ; "WxH" string
bpp=32                ; colour depth (16 or 32)
gamma=1.000000        ; brightness, float
```

There are **no other graphics options** in retail SHAR PC — see [C37.2](02-display-video.md) for why, and how
mods add widescreen resolutions.

## 37.3 Audio (✅ verified)

`CGuiScreenSound` exposes **five independent volume sliders**, each a `0.0–1.0` float in `#Sound`:

```ini
#Sound
sfx=0.093001        music=0.039501      ambience=0.079262
dialogue=0.012500   car=0.019501
```

Each maps to a RadSound (RSD) bus (C18/C19). [C37.3](03-audio.md).

## 37.4 Controls (✅ verified)

`CGuiScreenController` covers input for up to four devices. The `#Controller` section stores a full
**`buttonmap`** table plus mouse/wheel sensitivity, axis inversion, mouselook, and force feedback:

```ini
mouselook=no           invertmousex=no       invertmousey=no
useforcefeedback=yes   disabletutorials=no
mousesensitivityx=0.350000   mousesensitivityy=0.500000
wheelsensitivityx=0.500000   wheelsensitivityy=1.000000
```

The `buttonmap=<device>, <action>: ( <type> <code> <mod> )` grammar is decoded in [C37.4](04-controls.md).

## 37.5 Language & the pause mirror (✅ verified)

Each front-end settings screen has a **pause-menu twin** so the player can change settings mid-game:
`CGuiScreenPauseOptions` `0x0060E28C`, `CGuiScreenPauseDisplay` `0x0060E334`, `CGuiScreenPauseSound`
`0x0060E200`, `CGuiScreenPauseController` `0x0060E358`, and the `CGuiScreenPauseSettings` `0x0060E224` hub.
Plus the console-legacy `CGuiScreenMemoryCard`/`CGuiScreenAutoLoad` screens. [C37.5](05-language-pause.md).

## 37.6 Modding the settings (✅ practical)

Because every value is plain text in `simpsons.ini` and every screen is a confirmed class, mods can: add
non-listed resolutions (edit `resolution=`), force fullscreen, raise gamma past the slider cap, remap buttons,
or re-skin the menus via their Scrooby pages (C21). [C37.6](06-modding-settings.md).

---

## What this chapter established

- SHAR's PC options are **13 confirmed settings screens**, all RTTI-verified, under one **Options** hub with a
  full **pause-menu mirror**.
- The **Display** screen is the whole graphics surface: **resolution, bpp, gamma, windowed** — and nothing
  more. No quality/shadow/AA menu exists in retail.
- **Audio** is five volume buses; **Controls** is a button-map table plus sensitivity/invert/force-feedback.
- Every control writes a documented `simpsons.ini` key (C27.4), so all of it is moddable as plain text.

**Cross-references:** C21 (Scrooby UI — how these screens are drawn), C22 (fonts/localization — Language),
C27.4 (`simpsons.ini` file format), C18/C19 (RadSound buses behind the volume sliders), C28.7 (SAHRDiag —
how the screen vtables were confirmed).
