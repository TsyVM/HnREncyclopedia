# C27.4 — `simpsons.ini`: Config

**What it is.** The player's settings file — `simpsons.ini`, plain text in the game folder. Every option
they change (resolution, volumes, controls) is written here, and reading it back is how the game restores
their preferences. Unlike the binary save (C27.1), this one is fully human-readable.

**How it works (✅ verified).** The file is INI-style: `#Section` headers and `key=value` lines. The verified
sections:

```
#System
  display=window            resolution=1600x1200      bpp=32          gamma=1.000000
#Sound
  music=0.039501    sfx=0.093001    dialogue=0.012500    car=0.019501    ambience=0.079262
#Controller0 … #Controller3     (one block per controller/player)
  mouselook=no      invertmousex=no   invertmousey=no   useforcefeedback=yes
  disabletutorials=no
  mousesensitivityx=0.350000   mousesensitivityy=0.500000
  wheelsensitivityx=0.500000   wheelsensitivityy=1.000000
  … 143 buttonmap=… lines (the input bindings)
```

Three concerns, three section types:

- **`#System`** — the display: windowed vs. fullscreen (`display`), `resolution` (e.g. 1600×1200), colour
  depth (`bpp`), and `gamma`. These configure the Direct3D 8 device (C33.1).
- **`#Sound`** — five independent **volume channels** (0.0–1.0): `music`, `sfx`, `dialogue`, `car`, and
  `ambience` — exactly the audio categories of the seven archives (C19.1)! The mixer (C19.5) scales each
  category by its channel volume, so a player can turn down music while keeping dialogue up.
- **`#Controller0–3`** — one block per controller (4 supported): mouse look and inversion, force feedback
  (`useforcefeedback` — the rumble of C33.5), tutorial toggle, mouse/wheel sensitivity, and **143 `buttonmap`
  lines** binding physical inputs to game actions (the `Mappable`/controller system, C24.2/C25.3).

**Why text config.** A settings file is edited by the game (when the player changes an option) and, usefully,
by the player directly. Keeping it plain text means the game writes it trivially (no serialization format),
and a player or modder can open it in any editor to tweak settings the menus don't expose (an unusual
resolution, a finer sensitivity). This is the opposite trade from the binary save (C27.1): the save
prioritises fast fixed-layout reads on a memory card, while the config prioritises human-readability and easy
editing. Each format fits its job — the save is machine-oriented state, the config is human-oriented
preferences.

**The sound channels — a direct tie to C19.** The five `#Sound` volumes map one-to-one onto the audio
categories: `music` (the four `music0*.rcf`), `sfx` (`soundfx.rcf`), `dialogue` (`dialog.rcf`), `car`
(`carsound.rcf`), and `ambience` (`ambience.rcf`) — the seven archives of C19.1 grouped into five mixer
channels. So the config exposes the audio system's structure directly: each archive category is a volume
slider, and the mixer (C19.5) applies it. This is why you can independently balance, say, the (loud) music
against the (quieter) dialogue.

**What happens if you bend it.**

- *Set a resolution the display can't do* — the game may fail to create the D3D device or fall back. Use a
  supported mode.
- *Set a volume outside 0.0–1.0* — the mixer may clip or mute. Keep volumes in range.
- *Corrupt a `buttonmap` line* — that binding breaks. Match the binding format (the numeric device/code
  triple) exactly, or rebind through the menu.
