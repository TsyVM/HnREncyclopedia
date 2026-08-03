# Chapter 20 — Bink Video

> **Goal of this chapter:** decode the full-motion-video files — the logos, the intro, and the mission
> cutscenes — read a Bink header, and understand how the game plays and integrates FMV.

The game's cutscenes and logo stings ship as **16 `.rmv` files** (244 MB) in `movies/`. This chapter decodes
them from the retail data: 15 are standard **Bink** video (RAD Game Tools), one is an anomaly, and all play
through the shipped `binkw32.dll`.

**Key finding (✅ verified):** 15 of the 16 `.rmv` files begin with the Bink magic **`BIKi`** and carry a
textbook Bink header — `fmv2.rmv` is **640×480, 1,333 frames, 30 fps**. The 16th, `credits.rmv`, is **not**
Bink: it begins `00 70 00 00` and contains the tag **`xobX`** ("Xbox" byte-reversed) — a non-Bink container,
almost certainly an Xbox-build artefact (⏳).

---

## Deep-dive pages

- [C20.1 — The Bink Container](01-bink-container.md): the `BIKi` header, decoded.
- [C20.2 — The FMV Set](02-fmv-set.md): the 16 movies — logos, intro, cutscenes.
- [C20.3 — The `credits.rmv` Anomaly](03-credits-anomaly.md): the one non-Bink file.
- [C20.4 — `binkw32.dll` & Playback](04-binkw32-playback.md): the decoder the game ships.
- [C20.5 — FMV as a Game State](05-fmv-game-state.md): the `fmv` objective, `NISSoundPlayer`, and the movie player.

---

## 20.1 The Bink container (✅ verified)

A Bink file opens with a compact header. Decoded from `movies/fmv2.rmv`:

```
42 49 4B 69   "BIKi"          magic (Bink, version 'i')
… fileSize  = 17,053,576      (file length − 8)
… numFrames = 1,333
… largestFrame = 107,468      (biggest frame, for buffer sizing)
… width  = 640
… height = 480
… fpsDividend = 30, fpsDivider = 1   → 30 fps
```

Every field is a plain little-endian `uint32`. Bink stores video and audio interleaved by frame, so a player
reads the header, then streams frames, decoding video and audio together. [C20.1](01-bink-container.md).

## 20.2 The FMV set (✅ verified)

The 16 movies split into **logos**, **narrative**, and **cutscenes**:

| Kind | Files |
|---|---|
| Logos / stings | `foxlogo`, `radlogo`, `vuglogo`, `gracie` |
| Narrative | `intro`, `credits` |
| Cutscenes / mission | `fmv1A`, `fmv2`–`fmv8`, `loot`, `tele` |

The logo movies play at boot (Fox, Radical, VU Games, Gracie Films — the licensors and studios); the cutscenes
are the story's animated moments, triggered by the `fmv` mission objective (C16.3, 6 uses). [C20.2](02-fmv-set.md).

## 20.3 The `credits.rmv` anomaly (✅ verified anomaly)

`credits.rmv` is the exception: it does **not** start `BIKi`. Its first bytes are `00 70 00 00` (repeated),
and at offset 12 it contains the ASCII tag **`xobX`** — "Xbox" reversed. It is a **non-Bink container**,
almost certainly a leftover from the **Xbox build** shipped by mistake in the PC data, or a differently
-muxed movie. Its structure is ⏳ (not decoded here). [C20.3](03-credits-anomaly.md).

## 20.4 `binkw32.dll` & playback (✅ verified)

The game ships **`binkw32.dll`** (RAD Game Tools' Bink runtime) in the game directory — the decoder that
plays the 15 Bink `.rmv` files. Bink was *the* middleware FMV codec of the era; shipping its DLL is why the
movies play without the engine implementing a video codec itself. [C20.4](04-binkw32-playback.md).

## 20.5 FMV as a game state (✅ verified)

Playing a movie is a game state: the **`fmv` mission objective** (C16.3) triggers a cutscene, an
**`NISSoundPlayer`** (C19.2 — "Non-Interactive Sequence") handles its audio, and the movie player takes over
the screen until the movie ends or is skipped, then returns control. [C20.5](05-fmv-game-state.md).

---

## Key takeaways

- **16 `.rmv` FMVs** (244 MB); **15 are Bink** (`BIKi`) — `fmv2` is ✅ **640×480, 1,333 frames, 30 fps**.
- The set is **logos** (Fox/Radical/VU/Gracie), **narrative** (intro/credits), and **cutscenes**
  (`fmv1A`–`fmv8`, `loot`, `tele`), triggered by the `fmv` objective (C16.3).
- **`credits.rmv` is a non-Bink anomaly** (`xobX` tag) — likely an Xbox-build artefact (⏳).
- Playback uses the shipped **`binkw32.dll`** (RAD Game Tools).
- An FMV is a **game state**: the `fmv` objective triggers it, `NISSoundPlayer` handles its audio.

**Next:** [Chapter 21 — Scrooby UI](../C21-Scrooby-UI/C21-Scrooby-UI.md).
