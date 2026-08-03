# C18.1 — The RSD Header

**What it is.** The small, fixed header that opens every RSD sound and makes it self-describing: two
identifying tags and three numbers that tell you exactly how to play the samples that follow.

**How it works (✅ verified).** Decoded from `sound/accept.rsd` (identical in `scroll.rsd`):

```
offset 0:  52 53 44 34   "RSD4"        format magic
offset 4:  50 43 4D 20   "PCM "        codec tag (4 chars, space-padded)
offset 8:  01 00 00 00   channels = 1  (mono)
offset 12: 10 00 00 00   bits     = 16 (bits per sample)
offset 16: C0 5D 00 00   rate     = 24000 (Hz)
offset 20: 2A 2A 2A …    name/label field, padded with '*' (0x2A)
…          PCM samples
```

The magic is split deliberately into **format** (`RSD4` — "Radical Sound Data v4") and **codec** (`PCM ` —
the sample encoding). The three header numbers are everything a player needs: how many channels, how many
bits per sample, and the sample rate. After the header comes a name/label field padded with the `*`
character, then the raw samples. Both loose files are mono, 16-bit, 24 kHz — a modest rate that fits UI
blips and, across thousands of packed sounds (C19), keeps the audio budget down.

**Why a split magic.** Separating format from codec in the first 8 bytes lets one loader recognise "this is
RSD" (`RSD4`) and then branch on the codec tag (`PCM `, or an ADPCM tag, C18.2) without a version table. It's
the same self-describing instinct as the Pure3D container (C1) and the FourCC parameters of shaders and
collision (C6/C11): put the type in the first bytes, branch on it, and the format stays extensible — add a
codec tag and old readers can still identify the file even if they can't decode it.

**Why 24 kHz mono.** 24,000 Hz is half of CD's 48 kHz and below the 44.1 kHz music standard — deliberately
economical. For sound effects and voice (not music), 24 kHz is plenty, and mono halves the data again.
Multiply by thousands of sounds (dialogue alone is 173 MB, C19) and the savings are the difference between
fitting on the disc and not. Music, which needs fidelity, is handled separately (the `music0*.rcf` streams,
C19) — the RSD path is for effects and voice.

**Reading it in code.**

```python
def rsd_header(b):
    assert b[:4]==b'RSD4'
    return {'codec': b[4:8].decode().rstrip(),
            'channels': int.from_bytes(b[8:12],'little'),
            'bits':     int.from_bytes(b[12:16],'little'),
            'rate':     int.from_bytes(b[16:20],'little')}
```

**What happens if you bend it.**

- *Ignore the codec tag and assume PCM* — an ADPCM RSD (C18.2) decoded as PCM is noise. Read the tag and
  branch.
- *Assume a fixed sample-data offset* — the name/label field length can vary; find where the `*` padding
  ends (or use the known header size) before reading samples.
- *Play at the wrong rate* — using 44100 for a 24000 Hz clip pitches it up and speeds it. Honour the header's
  rate.
