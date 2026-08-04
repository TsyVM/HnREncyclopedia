# C37.1 — The Options Tree & Screen Classes

> Every settings screen in SHAR is a confirmed `CGuiScreen*` subclass with a known vtable address. This page
> is the map: the menu hierarchy, all 13 settings-screen vtables, and how the front-end and pause menus mirror
> each other.

## The hierarchy

The player opens **Options** from either the main menu or the in-game pause menu. Both lead to the same four
settings areas — the front-end path uses the plain screens, the pause path uses the `Pause*` twins:

```
Main Menu ─► Options (CGuiScreenOptions 0x0060F908)
                ├─ Display      → CGuiScreenDisplay     0x0060FD98
                ├─ Sound        → CGuiScreenSound       0x0060F58C
                ├─ Controller   → CGuiScreenController  0x0060FE38
                └─ Language      → CGuiScreenLanguage    0x0060D500

Pause  ─► Pause Options (CGuiScreenPauseOptions 0x0060E28C)
   └─ Settings hub (CGuiScreenPauseSettings 0x0060E224)
                ├─ Display      → CGuiScreenPauseDisplay    0x0060E334
                ├─ Sound        → CGuiScreenPauseSound      0x0060E200
                └─ Controller   → CGuiScreenPauseController 0x0060E358
```

## All confirmed settings-screen classes (✅ verified)

Every address below is `CONFIRMED` — recovered by the RTTI Complete-Object-Locator walk of retail
`Simpsons.exe` (MD5 `b3a47b881eec97745424b1e2c86cdcaf`) and reproduced by SAHRDiag (C28.7).

| Screen class | vtable VA | Role | Writes |
|---|---|---|---|
| `CGuiScreenOptions` | `0x0060F908` | main Options hub | — |
| `CGuiScreenDisplay` | `0x0060FD98` | video / "graphics" | `#System` |
| `CGuiScreenSound` | `0x0060F58C` | audio volumes | `#Sound` |
| `CGuiScreenController` | `0x0060FE38` | input / button map | `#Controller` |
| `CGuiScreenLanguage` | `0x0060D500` | localisation choice | (locale) |
| `CGuiScreenPauseSettings` | `0x0060E224` | pause settings hub | — |
| `CGuiScreenPauseOptions` | `0x0060E28C` | pause options entry | — |
| `CGuiScreenPauseDisplay` | `0x0060E334` | pause video | `#System` |
| `CGuiScreenPauseSound` | `0x0060E200` | pause audio | `#Sound` |
| `CGuiScreenPauseController` | `0x0060E358` | pause input | `#Controller` |
| `CGuiScreenMiniControllerSelect` | `0x0060D330` | 2-player pad select | — |
| `CGuiScreenMemoryCard` | `0x00610948` | save-device screen | (save) |
| `CGuiScreenAutoLoad` | `0x0060FCE8` | autoload prompt | (save) |

## Why a front-end *and* a pause copy?

SHAR is a console port. On the consoles the front-end and the in-game pause menu are separate UI contexts that
cannot share a live screen instance, so the game ships **two parallel screen classes** for each settings area —
one built under the `FrontEndContext`, one under the `PauseContext` (see the GameFlow contexts in C30). They
present the same controls and write the same `simpsons.ini` keys; only their owning context and layout differ.
On PC this is why changing a setting from the pause menu and from the title screen produces identical `.ini`
edits.

## How a screen becomes an edit

Each `CGuiScreen*` is a Scrooby screen (C21): its layout, text, and sprites come from a `.pag`/Scrooby
resource, and its class supplies the behaviour. The flow for any control is:

```
player moves control ─► screen's handler updates an in-memory settings object
                     ─► on "Apply"/back, the value is applied to the engine
                        (resolution → device reset; volume → RadSound bus; …)
                     ─► and written to simpsons.ini (C27.4) so it persists
```

The specific control→key mappings are the subject of the next three pages: [Display](02-display-video.md),
[Audio](03-audio.md), [Controls](04-controls.md).

## Confirming this yourself

All 13 vtables appear in `DonutsSDK/data/class_vtables.csv`. To see a settings screen live, run SAHRDiag's
dynamic scan (C28.7) with an Options menu open — the screen's instance will appear in
`SAHRDiag_live_objects.csv` identified by one of the vtables above, letting you read its live member bytes.
