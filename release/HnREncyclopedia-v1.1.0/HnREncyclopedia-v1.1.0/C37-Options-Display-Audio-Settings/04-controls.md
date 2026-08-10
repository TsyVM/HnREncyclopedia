# C37.4 — Controls & Input

> `CGuiScreenController` (`0x0060FE38`) configures input for the keyboard/mouse and up to four game pads. This
> page decodes the `#Controller` section: the `buttonmap` grammar, the sensitivity/invert/force-feedback keys,
> and how bindings are stored.

## The `#Controller` section

Each controller profile is stored as its own section — `#Controller`, `#Controller1`, `#Controller2`,
`#Controller3` (one per player slot). A profile holds a **button-map table** followed by the analog/toggle
settings:

```ini
#Controller
buttonmap=0, 0: ( 1 17 0 )     ; keyboard/mouse binding set
buttonmap=0, 1: ( 1 31 0 )
...
buttonmap=1, 0: ( 0 4 0 )      ; gamepad binding set
buttonmap=1, 1: ( 0 4 1 )
...
mouselook=no
invertmousex=no
invertmousey=no
useforcefeedback=yes
disabletutorials=no
mousesensitivityx=0.350000
mousesensitivityy=0.500000
wheelsensitivityx=0.500000
wheelsensitivityy=1.000000
```

## The `buttonmap` grammar (✅ decoded)

```
buttonmap=<set>, <action>: ( <inputType> <code> <flag> )
```

| Field | Meaning |
|---|---|
| `set` | binding set: `0` = keyboard/mouse, `1` = game pad |
| `action` | the in-game action index (0–26) — accelerate, brake, steer, jump, attack, camera, etc. |
| `inputType` | `0` = gamepad button/axis, `1` = keyboard, `2` = mouse |
| `code` | the DirectInput scancode (keyboard) / button index / axis id |
| `flag` | axis direction or modifier (`0`/`1`) — e.g. positive vs negative axis half |

**Worked example — the movement keys resolve to WASD (✅ verified via DirectInput scancodes):**

| Line | Decode |
|---|---|
| `buttonmap=0, 0: ( 1 17 0 )` | set 0 (kbd), action 0, keyboard `DIK_W` (0x11 = 17) → **forward** |
| `buttonmap=0, 1: ( 1 31 0 )` | keyboard `DIK_S` (0x1F = 31) → **back** |
| `buttonmap=0, 2: ( 1 30 0 )` | keyboard `DIK_A` (0x1E = 30) → **left** |
| `buttonmap=0, 3: ( 1 32 0 )` | keyboard `DIK_D` (0x20 = 32) → **right** |
| `buttonmap=1, 0: ( 0 4 0 )` | set 1 (pad), action 0, gamepad axis/button 4 → **forward** |

The `code` values are standard `DIK_*` DirectInput keyboard scancodes, which is how the table can be decoded
without the game running. The exact action-index → gameplay-verb mapping beyond movement is 🟡 reasoned
(indices 4–26 cover jump, attack, camera, handbrake, horn, and menu actions) — the scancodes themselves are
verified.

## The analog & toggle settings (✅ verified)

| Key | Type | Meaning |
|---|---|---|
| `mouselook` | `yes`/`no` | free-look with the mouse (on foot) |
| `invertmousex` / `invertmousey` | `yes`/`no` | invert horizontal / vertical mouse axis |
| `mousesensitivityx` / `mousesensitivityy` | float | on-foot look sensitivity per axis |
| `wheelsensitivityx` / `wheelsensitivityy` | float | in-vehicle steering sensitivity per axis |
| `useforcefeedback` | `yes`/`no` | rumble on force-feedback pads |
| `disabletutorials` | `yes`/`no` | suppress the tutorial pop-ups (also surfaced in Options) |

Note `disabletutorials` lives with the controller settings but is really a gameplay convenience toggle — the
Options UI exposes it alongside input because that is where the console originals put it.

## Storage & application

The Controller screen edits an in-memory input-binding object; on apply it rewrites the whole `#Controller*`
section and re-registers the bindings with the input system. Because bindings are plain text with a decoded
grammar, remaps can be authored directly in the file (see [C37.6](06-modding-settings.md)).

## Cross-references

- **C27.4 — `simpsons.ini`**: the `#Controller` section as a file.
- **C37.1** — the `CGuiScreenController` / `CGuiScreenPauseController` classes.
- **C37.6** — remapping and sensitivity tweaks as a mod.
