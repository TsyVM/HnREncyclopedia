# C37.5 — Language, the Pause Mirror & Memory-Card Screens

> The remaining settings screens: `CGuiScreenLanguage` for localisation, the `Pause*` family that mirrors the
> front-end settings in-game, and the console-legacy save-device screens.

## Language (✅ verified)

`CGuiScreenLanguage` (`0x0060D500`) selects the game's localisation. The choice drives which localized string
table and fonts the UI loads (C22 — fonts & localization). Unlike the other settings, the language selection
is not a numeric `#`-section key in `simpsons.ini`; it is applied through the localisation manager and the
selected locale is reflected in which text bible the front-end binds (the `FeTextChildTextBibleString` objects
seen live in the SAHRDiag capture, C28.7). Changing it reloads the front-end's strings.

## The pause-menu mirror (✅ verified)

Because SHAR is a console port with separate front-end and in-game UI contexts (C30), each settings area ships
**twice** — once for the title-screen `FrontEndContext` and once for the in-game `PauseContext`:

| Front-end screen | Pause twin | Area |
|---|---|---|
| `CGuiScreenOptions` `0x0060F908` | `CGuiScreenPauseOptions` `0x0060E28C` | options hub |
| — | `CGuiScreenPauseSettings` `0x0060E224` | pause settings sub-hub |
| `CGuiScreenDisplay` `0x0060FD98` | `CGuiScreenPauseDisplay` `0x0060E334` | video |
| `CGuiScreenSound` `0x0060F58C` | `CGuiScreenPauseSound` `0x0060E200` | audio |
| `CGuiScreenController` `0x0060FE38` | `CGuiScreenPauseController` `0x0060E358` | input |

Both twins present the same controls and write the same `simpsons.ini` keys; only their owning GameFlow context
and screen layout differ. This is worth knowing for menu modding (C38): to change a setting's UI everywhere,
you edit **both** the front-end and the pause screen.

## Memory-card & autoload screens (✅ verified, console legacy)

`CGuiScreenMemoryCard` (`0x00610948`) and `CGuiScreenAutoLoad` (`0x0060FCE8`) are the save-device screens
carried over from the console builds. On PC the "memory card" is the save folder (C27), but the screens remain
in the flow to prompt for save/load and autoload confirmation. `CGuiScreenMiniControllerSelect` (`0x0060D330`)
is the two-player pad-assignment screen used by the multiplayer/bonus modes.

## Why this matters for modders

These screens complete the picture that the menu system is a **fixed roster of confirmed classes**, each tied
to a Scrooby layout (C21) and a `simpsons.ini` key or save action. Nothing here is dynamically generated — which
is exactly why adding a *new* menu means adding a new screen class and wiring it into the flow, the subject of
the next chapter (C38).

## Cross-references

- **C22 — Fonts & Localization**: what `CGuiScreenLanguage` actually switches.
- **C30 — GameFlow**: the `FrontEndContext` vs `PauseContext` split that forces the mirrored screens.
- **C38 — Extending the Menu System**: adding your own screen to this roster.
