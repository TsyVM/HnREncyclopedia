# Chapter 18 — RSD Sound Format

> **Goal of this chapter:** decode the RSD sample container — the format behind every sound effect and UI
> sound — read its header, extract its samples, and understand the PCM and ADPCM codecs the engine plays it
> through.

Sound in *The Simpsons: Hit & Run* starts with the **RSD** sample format: a small, self-describing audio
container that holds one sound. This chapter decodes it from the retail data — both loose `sound/*.rsd`
files parse cleanly, and the runtime classes that consume RSD are read from the verified RTTI set.

**Key finding (✅ verified):** an RSD file is a **`RSD4` magic + 4-char codec tag** (`PCM `) followed by a
tiny header — **channels, bits-per-sample, sample-rate** — then the samples. The loose UI sounds are
`RSD4PCM`, mono, 16-bit, **24,000 Hz**. The runtime confirms a second codec: `IRadSoundAdpcmDecodeStream`
shows the engine also decodes **ADPCM**-compressed RSD.

---

## Deep-dive pages

- [C18.1 — The RSD Header](01-the-rsd-header.md): `RSD4` + codec tag + channels/bits/rate, decoded.
- [C18.2 — Codecs: PCM & ADPCM](02-codecs.md): the two sample encodings the engine plays.
- [C18.3 — Extracting Audio to WAV](03-extracting.md): pulling samples out to a standard file.
- [C18.4 — Loose vs. Packed Sound](04-loose-vs-packed.md): `sound/*.rsd` vs. the audio RCFs (C19).
- [C18.5 — RSD at Runtime: RadSound](05-radsound-runtime.md): `IRadSoundClip` and the HAL.

---

## 18.1 The RSD header (✅ verified)

An RSD file opens with an 8-byte magic that is really **two** tags — the format (`RSD4`) and the codec
(`PCM ` with a trailing space) — then a fixed header. Decoded from `sound/accept.rsd`:

```
52 53 44 34  50 43 4D 20   "RSD4" + "PCM "   (format + codec tag)
01 00 00 00                channels   = 1   (mono)
10 00 00 00                bits        = 16
C0 5D 00 00                sampleRate  = 24000 Hz
2A 2A 2A 2A …              name field, padded with '*' (0x2A)
… PCM samples …
```

Both loose files (`accept.rsd`, `scroll.rsd`) are byte-for-byte this shape: mono, 16-bit, 24 kHz PCM. The
`*`-padded field is the sound's name/label slot. [C18.1](01-the-rsd-header.md).

## 18.2 Codecs: PCM & ADPCM (✅ verified)

The 4-char codec tag selects the sample encoding. The loose sounds are **`PCM `** — uncompressed 16-bit
samples, the simplest case. But the runtime proves a second codec: the RTTI class
`IRadSoundAdpcmDecodeStream` (C18.5) decodes **ADPCM**, the compressed form used for the bulk audio in the
packed archives (C19) where size matters. So RSD is a *container* with at least two codecs — read the tag,
then decode accordingly. [C18.2](02-codecs.md).

## 18.3 Extracting audio (✅ reproducible)

Because the header gives channels, bits, and rate, and PCM samples are raw, extraction to WAV is a header
translation and a copy:

```python
def rsd_to_wav(path, out):
    b = open(path,'rb').read()
    assert b[:4]==b'RSD4'
    codec = b[4:8]                                  # b'PCM '
    ch, bits, rate = struct.unpack_from('<III', b, 8)
    data = b[0x30:]                                 # samples after the header/name field
    # write a standard 44-byte WAV header for ch/bits/rate, then `data`
```

[C18.3](03-extracting.md) gives the full WAV writer and the ADPCM decode path.

## 18.4 Loose vs. packed (✅ verified)

Only **2** RSD files ship loose (`sound/accept.rsd`, `sound/scroll.rsd` — the accept/scroll UI sounds). The
game's thousands of other sounds are packed into the audio RCFs (`soundfx.rcf`, `carsound.rcf`, etc., C19),
where they're addressed by hash (C3) and often ADPCM-compressed. [C18.4](04-loose-vs-packed.md).

## 18.5 RSD at runtime (✅ verified)

An RSD becomes an `IRadSoundClip` played by an `IRadSoundClipPlayer`, decoded (for ADPCM) through
`IRadSoundAdpcmDecodeStream`, and output via the RadSound **HAL** (`IRadSoundHal*` — 43 classes) with
optional EAX reverb (`IRadSoundHalEffectEAX2Reverb`, matching the shipped `eax.dll`). [C18.5](05-radsound-runtime.md).

---

## Key takeaways

- An RSD is **`RSD4` + a 4-char codec tag** (`PCM `) + header (channels, bits, sample-rate) + samples.
  Loose UI sounds are ✅ **mono, 16-bit, 24,000 Hz PCM**.
- The codec tag selects the encoding; the runtime proves **PCM and ADPCM** (`IRadSoundAdpcmDecodeStream`).
- Extraction is a header translation + sample copy (PCM) or an ADPCM decode.
- Only 2 RSD ship loose; the rest are packed in the audio RCFs (C19), hash-addressed and often ADPCM.
- At runtime an RSD is an `IRadSoundClip` on the RadSound HAL, with EAX reverb support.

**Next:** [Chapter 19 — The Audio Archives](../C19-Audio-Archives/C19-Audio-Archives.md).
