# C18.5 — RSD at Runtime: RadSound

**What it is.** What an RSD becomes when it plays — the RadSound engine, RadCore's audio layer, proven by 43
verified `IRadSound*` classes. This is the runtime that turns a sample file into sound coming out of the
speakers.

**How it works (✅ verified).** From `shar_dumps.csv`, the RadSound clip/player/HAL chain:

```
IRadSoundClip : IRefCount                                   — a loaded sound (an RSD's samples)
IRadSoundClipPlayer : IRadSoundPlayer, IRefCount            — plays a clip
IRadSoundAdpcmDecodeStream : IRadSoundHalDataSource         — decodes ADPCM RSD (C18.2) on the fly
IRadSoundBufferedDataSource : IRadSoundHalDataSource        — streams buffered audio
IRadSoundHalBuffer / IRadSoundHalAudioFormat / …            — the Hardware Abstraction Layer
IRadSoundHalEffectEAX2Reverb : IRadSoundHalEffect           — EAX 2 environmental reverb
```

The chain is: an RSD loads into an **`IRadSoundClip`**; an **`IRadSoundClipPlayer`** plays it; if it's ADPCM
(C18.2), an **`IRadSoundAdpcmDecodeStream`** decodes it to PCM en route; the PCM goes to an
**`IRadSoundHalBuffer`** in the **HAL** (Hardware Abstraction Layer), which is what actually talks to the
sound hardware. Optional **EAX 2 reverb** (`IRadSoundHalEffectEAX2Reverb`) adds environmental echo.

**The HAL and portability.** The `IRadSoundHal*` classes (a large chunk of the 43) are a **hardware
abstraction layer** — RadSound's way of running the same audio code on PC (DirectSound/EAX), PS2, GameCube,
and Xbox by implementing the HAL per platform. On PC, the EAX support (`IRadSoundHalEffectEAX2Reverb`) maps
to the shipped **`eax.dll`** in the game directory — a direct, verifiable tie between an RTTI class and a
file on disk. This is why the game folder has `eax.dll`: it's the PC backend for the reverb effect the HAL
exposes.

**Why an abstraction layer.** A cross-platform 2003 engine can't hardcode DirectSound; it needs one audio
API the game code uses and a per-platform implementation underneath. The HAL is that seam — the game plays an
`IRadSoundClip` through the HAL without knowing whether the HAL is DirectSound, the PS2's SPU, or the
GameCube's DSP. For reverse engineering, the HAL is a clean boundary: everything above it (clips, players,
decode streams) is portable game logic; everything below is platform glue.

**The player hierarchy (lead-in to C19).** Above the raw clip players sits the game's *positional* sound —
`VehiclePositionalSoundPlayer`, `TrafficSoundPlayer`, `AvatarSoundPlayer`, `NISSoundPlayer` — which place a
clip in 3-D space and attach it to a moving object (C24.5/C25). Those are the subject of C19; here it's enough
that they all bottom out in the RadSound clip/HAL chain above. An engine sound is a `carsound.rcf` RSD →
`IRadSoundClip` → decoded → positioned by a `VehiclePositionalSoundPlayer` → output through the HAL.

**What happens if you bend it.**

- *Rely on a RadSound class member offset* — the classes are ✅ (43 of them), offsets ⏳. Diff (C4.3).
- *Assume EAX everywhere* — EAX reverb is a PC HAL effect (`eax.dll`); other platforms use their own. It's an
  optional enhancement, not core.
- *Feed the HAL an undecoded ADPCM clip* — it expects PCM at the buffer; the decode stream (C18.2) must run
  first. Respect the decode-then-play order.

**Next:** [Chapter 19 — The Audio Archives](../C19-Audio-Archives/C19-Audio-Archives.md).
