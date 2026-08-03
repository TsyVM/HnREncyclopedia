# Chapter 27 — Save Data & `simpsons.ini`

> **Goal of this chapter:** decode the two files that persist the player's world — the binary **career save**
> (`Save1`) that records progress, and the text **`simpsons.ini`** config that stores their settings. After
> this chapter you can read a save's structure and edit any game option.

Everything the player earns — missions completed, cars unlocked, coins, cards — lives in a **save file**; every
option they set lives in **`simpsons.ini`**. This chapter decodes both from the retail data: the save's
structure is read directly from a real `Save1`, and the config is plain text.

**Key finding (✅ verified):** the save is a **career-state binary** — a header, the player-slot name
(`Player1`), fixed-stride **record arrays** for mission completion (`sr1`/`sr2`/`sr3`/`bm1`/`gr1` at 32-byte
stride) and unlocked cars/rewards (`famil_v` + `n/a` placeholders at 24-byte stride), plus numeric progress.
`simpsons.ini` is text with **`#System`** (display/resolution/gamma), **`#Sound`** (5 volume channels), and
**`#Controller0-3`** (input) sections.

---

## Deep-dive pages

- [C27.1 — The Save Container (`Save1`)](01-save-container.md): the header, player slot, and layout.
- [C27.2 — Career State: Missions, Cars & Coins](02-career-state.md): the record arrays and progress.
- [C27.3 — The Memory-Card System](03-memory-card.md): `MemoryCardManager` and save/load at runtime.
- [C27.4 — `simpsons.ini`: Config](04-simpsons-ini.md): the System/Sound/Controller sections.
- [C27.5 — Editing Config & Saves](05-editing.md): tuning options safely; the risks of save editing.

---

## 27.1 The save container (✅ verified)

`Save1` (7,194 bytes) opens with a header and the **player-slot name**. Verified layout:

```
@0:   ba 07 ea 07  03 04 0c 19 0b 00 01 00 ...   header + timestamp (🟡)
@17:  "Player1"                                  the save-slot / player name
…     numeric progress (coins, position, current mission — C27.2)
@409: mission-completion records (32-byte stride): "sr1","sr2","sr3","bm1","gr1"
@4397: reward/car records (24-byte stride): "famil_v", then "n/a" (unfilled)
```

It's a flat binary of a header plus **fixed-stride record arrays** — the standard console-save layout.
[C27.1](01-save-container.md).

## 27.2 Career state (✅ verified structure)

The save records progress as record arrays:

- **Mission completion** — records at 32-byte stride naming the bonus missions completed (`sr1`–`sr3`,
  `bm1`, `gr1`, C16.5). The story missions' state sits in the numeric region.
- **Unlocked cars/rewards** — records at 24-byte stride: `famil_v` (the family car, the level-1 default,
  C16.6) is present; unfilled slots read `n/a`. This is the reward economy's persistence (C16.6/C32.5).
- **Coins, cards, current level & position** — in the numeric regions (exact fields 🟡).

[C27.2](02-career-state.md).

## 27.3 The memory-card system (✅ verified)

Saving/loading runs through **`MemoryCardManager`** (a verified runtime class, vtable `0x00607514`) — a
legacy of the console origins (SHAR shipped on PS2/GC/Xbox where saves are memory-card files). The UI is the
`CGuiScreenMemoryCard`/`MemCardCheck`/`LoadGame`/`AutoLoad` screens (C21.5). [C27.3](03-memory-card.md).

## 27.4 `simpsons.ini` (✅ verified)

The config is plain text in sections:

```
#System:      display=window  resolution=1600x1200  bpp=32  gamma=1.000000
#Sound:       music, sfx, dialogue, car, ambience   (volumes 0.0–1.0)
#Controller0..3: mouselook, invertmousex/y, useforcefeedback, disabletutorials,
                 mouse/wheel sensitivity, + 143 buttonmap input bindings
```

Every option the player sets is here, readable and editable. [C27.4](04-simpsons-ini.md).

## 27.5 Editing config & saves (✅ path)

`simpsons.ini` is safe to edit (text — change resolution, volumes, sensitivity). The binary save is riskier:
its record structure is clear, but numeric fields and any checksum are 🟡, so save editing needs care.
[C27.5](05-editing.md).

---

## Key takeaways

- The **save** (`Save1`) is a **career-state binary**: header + player-slot name + fixed-stride **record
  arrays** for mission completion (32-byte) and unlocked cars/rewards (24-byte, `famil_v`+`n/a`), plus numeric
  progress.
- Saving runs through **`MemoryCardManager`** (verified class) — a console-origin legacy — with the
  `CGuiScreenMemoryCard*` UI (C21.5).
- **`simpsons.ini`** is text config: `#System` (display/resolution/gamma), `#Sound` (5 volume channels),
  `#Controller0–3` (input + 143 bindings).
- Config is safe to edit; the save's record layout is ✅ but its exact numeric fields are 🟡 (edit with care).

**Next:** [Chapter 28 — The Modding Toolchain](../C28-Modding-Toolchain/C28-Modding-Toolchain.md).
