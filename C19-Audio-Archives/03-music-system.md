# C19.3 — The Interactive Music System

**What it is.** The system behind the game's music — not a jukebox playing whole tracks, but an
**interactive composition** engine that stitches streamed segments into seamless, event-reactive music. It's
why the music swells in a chase and settles when you're idle.

**How it works (✅ verified).** From `shar_dumps.csv`:

```
MusicPlayer : EventListener                                 — the game-facing music driver
Sound::MusicSoundPlayer : Sound::daSoundPlayerBase          — plays the music stream
radmusic::composition_data_loader : radLoadDataLoader       — loads a composition
radmusic::radload_radmusic_inventory : radLoadInventory     — the music inventory
radmusic::radmusic_file_loader : radLoadFileLoader          — loads music files (from music0*.rcf)
radmusic::stream_graph_callback : IRadSoundStitchCallback   — stitches stream segments seamlessly
```

The `radmusic::` namespace is a **stream-graph composition** engine. Music is authored as a *graph* of
segments and transitions (a composition); the engine plays a path through the graph, and
`stream_graph_callback` (an `IRadSoundStitchCallback`) **stitches** one streamed segment to the next with no
audible seam. `MusicPlayer`, being an **`EventListener`** (C23.3), reacts to game events — enter a chase,
complete a mission — by choosing a different path through the composition. The actual audio streams from the
four `music0*.rcf` archives (C19.1).

**Why interactive rather than track playback.** A driving-and-action game needs music that *responds*:
tension when cops chase you, calm when you explore, a sting when you finish a mission. Playing fixed tracks
can't do that — you'd get abrupt cuts. A stream-graph composition can: it holds the music in segments with
defined transition points, so it can move from "calm" to "tense" at a musical boundary, seamlessly. This is
a common 2000s-era interactive-music technique, and `radmusic::` is RadCore's implementation of it.

**The stitch callback.** The heart of seamlessness is `stream_graph_callback : IRadSoundStitchCallback`.
"Stitching" means the engine, as one streamed segment nears its end, chooses and queues the next segment so
the audio buffer never runs dry — the join is at a musical boundary and inaudible. This is why the music
never pops or gaps even as it changes with the action: the stitch callback is always preparing the next
segment. It runs on the RadSound streaming path (`IRadSoundBufferedDataSource`, C18.5).

**Why four music archives.** The composition can draw on a lot of material — different moods, areas, and
missions each have music — and streaming it needs it contiguous (C19.1). Four ~225 MB archives hold the
segment library, and the stream-graph engine pulls segments from them as the composition demands. The size
(908 MB) reflects how much *distinct* music a seven-level comedy game carries.

**What happens if you bend it.**

- *Rely on a `radmusic::` class offset* — classes ✅, offsets ⏳. Diff (C4.3).
- *Replace a music segment with one of a different length/format* — the stitch points and streaming assume
  the composition's structure. Match the segment format, or rebuild the composition.
- *Expect fixed-track behaviour* — the music is a graph, not a playlist; it changes with events. Reason about
  it as a composition (C4.4).
