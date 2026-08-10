# C37.3 — Audio Settings

> `CGuiScreenSound` (`0x0060F58C`) exposes five independent volume sliders. This page documents each channel,
> the `#Sound` keys, and the RadSound buses behind them.

## The five volume channels (✅ verified)

The Sound screen maps one-to-one onto the `#Sound` section — five floats, each in the range `0.0` (silent) to
`1.0` (full):

```ini
#Sound
sfx=0.093001        ; sound effects (kicks, pickups, impacts, UI)
music=0.039501      ; the licensed/score music beds
ambience=0.079262   ; environmental / world ambience
dialogue=0.012500   ; character voice-over lines
car=0.019501        ; vehicle engine / tyre / horn audio
```

| Slider | `.ini` key | Bus | Content |
|---|---|---|---|
| SFX | `sfx` | effects bus | kicks, coins, cards, collisions, UI blips |
| Music | `music` | music stream | the soundtrack (RCF music streams — C19) |
| Ambience | `ambience` | ambience bus | town/level environmental loops (`ambience.rcf`) |
| Dialogue | `dialogue` | voice bus | character speech (`dialog.rcf`) |
| Car | `car` | vehicle bus | engine, skid, horn, crash audio (`carsound.rcf`) |

The five keys correspond directly to the five audio archives the game ships (C19): `ambience.rcf`,
`carsound.rcf`, `dialog.rcf`, the `music*.rcf` set, and `soundfx.rcf`. Each slider scales the gain of its bus.

## How a slider becomes gain

The volume value is a linear `0.0–1.0` multiplier applied to its RadSound bus (C18 covers the RSD sample
format; C19 covers the archives). Moving the slider updates the in-memory settings object; on apply, the value
is pushed to the sound system's per-bus gain and written to `simpsons.ini`. Because the buses are independent,
a player can, for example, mute `music` while keeping `dialogue` and `sfx` — each is its own key.

## Note on the sample values

The values shown above are from a real captured `simpsons.ini` and happen to be low (e.g. `music=0.039501`) —
that is simply the state that player left their sliders in, not a default. A fresh install writes higher
defaults; the point for this chapter is the **structure** (five independent `0.0–1.0` channels), which is
fixed.

## Cross-references

- **C18 — RadSound (RSD)**: the mono/16-bit/24000 Hz sample format behind every effect and voice line.
- **C19 — Audio Archives**: the five `.rcf` sound archives these buses draw from.
- **C27.4 — `simpsons.ini`**: the `#Sound` section as a file.
