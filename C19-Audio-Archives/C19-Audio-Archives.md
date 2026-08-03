# Chapter 19 — The Audio Archives

> **Goal of this chapter:** map the seven audio RCF archives that hold ~1.24 GB of the game's sound, and
> decode the runtime systems that play them — positional sound, the interactive music system, and the
> dialogue coordinator.

Audio is the largest thing in the game by disc space: **seven RCF archives** (C3) totalling ~1.24 GB of the
1.43 GB of packed data — four music sets, dialogue, effects, and ambience. This chapter reads that split and
the verified runtime classes that turn packed RSD (C18) into the living soundscape of Springfield.

**Key finding (✅ verified):** the audio runtime is three coordinated systems on the RadSound HAL (C18.5): a
**positional sound** player hierarchy (`VehiclePositionalSoundPlayer`, `TrafficSoundPlayer`,
`AvatarSoundPlayer`, …), an **interactive music** system (`MusicPlayer` + the `radmusic::` composition
engine), and a **dialogue** system with a priority queue (`DialogCoordinator`, `DialogPriorityQueue`).

---

## Deep-dive pages

- [C19.1 — The Seven Archives](01-seven-archives.md): what each RCF holds and why the split.
- [C19.2 — Positional Sound Players](02-positional-players.md): 3-D sound attached to moving objects.
- [C19.3 — The Interactive Music System](03-music-system.md): `MusicPlayer`, `radmusic::`, streamed sets.
- [C19.4 — The Dialogue System](04-dialogue-system.md): the coordinator and the priority queue.
- [C19.5 — The Audio Frame & the HAL](05-audio-frame.md): how it all mixes each frame.

---

## 19.1 The seven archives (✅ verified sizes)

| Archive | Size | Holds | Codec (typical) |
|---|--:|---|---|
| `music00.rcf` | 228.5 MB | streamed music set 0 | streamed |
| `music01.rcf` | 225.0 MB | streamed music set 1 | streamed |
| `music02.rcf` | 228.5 MB | streamed music set 2 | streamed |
| `music03.rcf` | 226.5 MB | streamed music set 3 | streamed |
| `dialog.rcf` | 173.0 MB | character dialogue | ADPCM RSD (C18.2) |
| `soundfx.rcf` | 135.3 MB | sound effects | ADPCM RSD |
| `ambience.rcf` | 102.5 MB | world ambience beds | ADPCM RSD |

The split is by **role and access pattern**: music is streamed (read sequentially in long runs), so it gets
its own four large archives; dialogue, effects, and ambience are triggered clips (random access), packed as
hash-addressed RSD (C3/C18). [C19.1](01-seven-archives.md).

## 19.2 Positional sound players (✅ verified)

Most game sounds are **positional** — placed in 3-D and attached to a moving source. The verified hierarchy:

```
PositionalSoundPlayer : SimpsonsSoundPlayer
VehiclePositionalSoundPlayer : PositionCarrier
  ├ AIVehicleSoundPlayer         — AI/traffic car engines
  └ TrafficSoundPlayer           — ambient traffic
AvatarSoundPlayer                — the player character
AnimObjSoundPlayer               — animated objects / gags (C14.4)
PlatformSoundPlayer, NISSoundPlayer (cutscenes, C20)
```

`PositionCarrier` ties a sound to a world position; each player type attaches to its kind of source (car,
character, gag). [C19.2](02-positional-players.md).

## 19.3 The interactive music system (✅ verified)

Music is not just streamed files — it's an **interactive composition** system:

```
MusicPlayer : EventListener                         — drives music, reacts to game events
Sound::MusicSoundPlayer : Sound::daSoundPlayerBase  — the music player
radmusic::composition_data_loader                   — loads compositions
radmusic::stream_graph_callback : IRadSoundStitchCallback  — stitches streams seamlessly
```

`radmusic::` is a **composition/stream-graph** engine — it stitches streamed segments (from `music0*.rcf`)
into seamless, event-reactive music (`MusicPlayer` being an `EventListener`). [C19.3](03-music-system.md).

## 19.4 The dialogue system (✅ verified)

Dialogue — the game's largest single archive (173 MB) — has its own coordination layer:

```
DialogCoordinator : EventListener
DialogPriorityQueue : DialogLineCompleteCallback, DialogCompleteCallback
DialogLine : PlayableDialog, SelectableDialog
DialogList, DialogSelectionGroup, DialogQueueElement
DialogueObjective : MissionObjective (the "dialogue" objective, C16.3)
```

A **priority queue** decides which line plays when multiple want to (mission line vs. ambient bark); the
coordinator manages it. [C19.4](04-dialogue-system.md).

## 19.5 The audio frame (✅ verified)

Each frame the players update their positions, the music stitches its next segment, the dialogue queue picks
the highest-priority line, and everything mixes through the RadSound **HAL** (C18.5) with EAX reverb.
[C19.5](05-audio-frame.md).

---

## Key takeaways

- **Seven audio RCFs** hold ~1.24 GB: four **streamed music** sets, plus **dialogue** (173 MB), **effects**
  (135 MB), and **ambience** (102 MB) as hash-addressed ADPCM RSD (C18).
- Sound is **positional**: a verified player hierarchy attaches 3-D sound to cars, traffic, the player, and
  gags (`VehiclePositionalSoundPlayer`, `TrafficSoundPlayer`, …).
- Music is an **interactive composition** system (`MusicPlayer` + `radmusic::`) that stitches streamed
  segments and reacts to game events.
- Dialogue has a **priority queue** (`DialogCoordinator`/`DialogPriorityQueue`) choosing which line plays.
- Everything mixes through the RadSound HAL (C18.5); classes ✅, offsets ⏳.

**Next:** [Chapter 20 — Bink Video](../C20-Bink-Video/C20-Bink-Video.md).
