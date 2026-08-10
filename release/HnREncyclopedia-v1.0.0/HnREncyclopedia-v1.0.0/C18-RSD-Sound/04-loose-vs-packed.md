# C18.4 — Loose vs. Packed Sound

**What it is.** The two places RSD sounds live: a tiny handful loose in `sound/`, and the overwhelming
majority packed into the audio RCF archives (C19). Knowing which is which tells you how to reach a given
sound.

**How it works (✅ verified).** Only **2** RSD files ship loose: `sound/accept.rsd` and `sound/scroll.rsd` —
the menu **accept** and **scroll** sounds. Everything else — every effect, every voice line, every engine
sound — is inside the seven audio RCFs:

```
soundfx.rcf   135 MB   sound effects
carsound.rcf   21 MB   vehicle/engine audio
ambience.rcf  102 MB   world ambience
dialog.rcf    173 MB   character dialogue
music00-03.rcf ~908 MB streamed music
```

Packed sounds are addressed by the **Radical hash of their path** (C3.3), stored as `{hash, offset, size}`
in the archive directory, and are commonly **ADPCM**-compressed (C18.2) to fit. A packed RSD still begins
`RSD4` (C3.3), so once extracted it self-identifies and decodes exactly like a loose one.

**Why only two loose.** The accept/scroll sounds are needed **before** the archives are mounted — they're
the front-end's most basic feedback, playing as the game boots and the menus first appear. Keeping them
loose (and PCM, for zero-decode instant playback, C18.2) means the UI can beep before the audio system has
loaded any archive. Everything else can wait for its archive to mount, so it's packed. This is the same
"bootstrap essentials loose, bulk content packed" logic as the rest of the VFS (C3.6) — the two loose sounds
are the audio equivalent of the always-resident terrain (C12.1).

**Reaching a packed sound.** To get a specific sound out of an archive you need its path (to hash) or you
extract everything and identify by content:

- *By name*: hash the sound's path (C2.2) and look it up in the archive directory (C3.4). Requires knowing
  or recovering the path (C2.4).
- *By content*: extract every member (C3.4), keep the ones starting `RSD4`, and convert (C18.3). Names are
  lost but the audio is recovered — useful for a full rip.

**The modding consequence.** To replace the accept/scroll sounds, edit the loose files directly (or shadow
them, C3.6) — the easy case. To replace a packed sound, either rebuild the archive (C3.4 — heavy) or drop a
loose file the VFS consults first (C3.6 — light), the same two routes as any packed asset. Because the loose
tree shadows the archives, even packed audio can often be overridden without repacking.

**What happens if you bend it.**

- *Look for a sound loose that's actually packed* — 2 of thousands are loose. Check the archives (C19) for
  the rest.
- *Replace a packed ADPCM sound with a PCM file of a different length* — you change the member size and must
  repack correctly (C3.4), or shadow it loose. Match the format the engine expects.
- *Assume packed sounds have readable names* — the directory is hash-keyed (C3.3). Recover the path or
  identify by content.
