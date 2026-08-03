# C19.1 — The Seven Archives

**What it is.** The seven RCF files that hold the game's audio, and the logic behind splitting sound across
them. Together they are the single largest category of data in the game.

**How it works (✅ verified sizes).** Measuring the retail tree:

```
music00.rcf  228.5 MB ┐
music01.rcf  225.0 MB │  four streamed music sets (~908 MB)
music02.rcf  228.5 MB │
music03.rcf  226.5 MB ┘
dialog.rcf   173.0 MB    character dialogue
soundfx.rcf  135.3 MB    sound effects
ambience.rcf 102.5 MB    world ambience beds
```

That's **~1.24 GB of the 1.43 GB** of packed data — audio dominates the disc. Each archive is a standard
`RADCORE CEMENT LIBRARY` (C3): a header, a hash-keyed directory, and the member data. Effects, dialogue, and
ambience members are RSD sounds (C18), typically ADPCM-compressed (C18.2); music members are streamed audio.

**Why split by category.** Four reasons, each visible in the split:

1. **Access pattern.** Music is *streamed* — read sequentially in long runs while a track plays — so it wants
   contiguous storage and gets its own archives. Effects/dialogue/ambience are *triggered clips* — random
   access, played on an event — so they're hash-addressed for quick lookup (C3.3).
2. **Residency.** Different categories load and free at different times: ambience changes with the area,
   dialogue with the mission, music with the mood. Separate archives let each be managed independently.
3. **Size budgeting.** Splitting music into *four* archives (rather than one 900 MB file) bounds how much
   music data is touched at once and fits the streaming budget.
4. **Disc layout.** On 2003 optical media, keeping a category contiguous minimises seeks — the music you're
   streaming isn't interleaved with effects you might trigger.

**Why audio is the biggest category.** SHAR is a licensed comedy game: it lives on its **voices** (173 MB of
dialogue — the largest single archive) and its **music** (908 MB across four sets). The world's *look* is
264 MB of loose art (C12); its *sound* is nearly five times that. This ratio is the fingerprint of the genre
— a talkie, music-driven cartoon world spends its disc on being *heard*.

**Reaching the audio.** Each archive is opened and indexed like any RCF (C3.4): read the header and directory
(a few KB), then seek to the one member you want — never load a 228 MB archive whole to pull one sound
(C3.5). Members self-identify by magic (`RSD4`, C18.1) once extracted, even without their hashed names.

**What happens if you bend it.**

- *Load a whole music archive to extract one track* — a quarter-gig for one file. Seek to the directory
  offset (C3.5).
- *Assume all seven use identical layout* — read each archive's own header/directory (C3.1); don't reuse
  constants across files.
- *Repack a giant archive to change one sound* — prefer the loose-shadow route (C3.6) unless you must repack.
