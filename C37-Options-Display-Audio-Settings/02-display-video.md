# C37.2 — Display & "Graphics" Settings

> `CGuiScreenDisplay` (`0x0060FD98`) is the whole of SHAR's PC video configuration. This page documents its
> four controls, the `#System` keys they write, how they apply to the engine, and — importantly — why there is
> **no** separate graphics-quality menu.

## The four (and only) video settings (✅ verified)

The Display screen maps one-to-one onto the `#System` section of `simpsons.ini`:

```ini
#System
display=window        ; window | fullscreen
resolution=1600x1200  ; "WIDTHxHEIGHT" as a string
bpp=32                ; back-buffer colour depth: 16 or 32
gamma=1.000000        ; brightness multiplier, float (slider-clamped)
```

| Control | `.ini` key | Values | Applies to |
|---|---|---|---|
| Windowed / Fullscreen | `display` | `window`, `fullscreen` | D3D device present mode |
| Resolution | `resolution` | `"WxH"` string, e.g. `800x600`, `1600x1200` | D3D back-buffer size (device reset) |
| Colour depth | `bpp` | `16`, `32` | back-buffer pixel format |
| Gamma / Brightness | `gamma` | float ~`0.5`–`2.0` | gamma-ramp on the device |

Changing resolution or colour depth triggers a **Direct3D device reset** — the same Invalidate/Restore cycle
the renderer uses on any device-lost event (C33). Gamma is applied by setting the device's gamma ramp; it does
not require a reset.

## Why there is no "graphics quality" menu (✅ verified)

Players coming from later PC games expect texture-detail, shadow, draw-distance, or anti-aliasing toggles.
**SHAR has none of these.** The retail PC build is a faithful port of the console versions, and its only video
knobs are the four above. The evidence is threefold:

1. **No such screens exist.** The settings-screen roster (C37.1) contains a `Display` screen and nothing else
   video-related — no `CGuiScreenGraphics`, `CGuiScreenQuality`, or equivalent in the RTTI class set.
2. **No such keys exist.** `simpsons.ini`'s `#System` section holds exactly `display`, `resolution`, `bpp`,
   `gamma` — there is nowhere to persist a quality setting.
3. **The engine is fixed-function-era.** SHAR renders through Pure3D on Direct3D 8 with a fixed shading model
   (C33). Texture and geometry LOD are authored into the assets (the `.p3d` mesh/texture chunks), not chosen
   at runtime, so there is no quality dial to expose.

This is an honest and useful conclusion: on PC, **"graphics settings" and "display settings" are the same
screen**, and improving visuals is a *modding* task (higher-res textures, widescreen patches), not an in-game
option.

## Resolution handling

`resolution` is stored as a **string**, parsed into width/height at load. The menu offers a fixed list of
standard modes the device reports as supported (e.g. `640x480`, `800x600`, `1024x768`, `1280x1024`,
`1600x1200`). Because the value is just text, the file accepts any `WxH` the driver will accept even if the
menu never lists it — the basis for the widescreen mods in [C37.6](06-modding-settings.md).

## Gamma

`gamma=1.000000` is neutral. The Display screen's brightness slider maps to this multiplier and clamps it to a
safe range so the player cannot black out or blow out the image. Editing the file directly bypasses the clamp
(again, see C37.6).

## Cross-references

- **C33 — Rendering**: the Pure3D/Direct3D 8 pipeline these settings drive, and the device-reset cycle.
- **C27.4 — `simpsons.ini`**: the `#System` section as a file.
- **C5 / C7 — Textures / Meshes**: where visual quality is actually authored (assets, not options).
