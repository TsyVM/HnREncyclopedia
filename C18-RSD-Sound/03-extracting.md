# C18.3 — Extracting Audio to WAV

**What it is.** Turning an RSD into a file you can play — a WAV — which for PCM is a header swap and for
ADPCM is a decode-then-write. This is the practical payoff of the header decode (C18.1).

**Extracting PCM (✅ reproducible).** A PCM RSD's samples are already linear 16-bit; wrapping them in a
44-byte WAV header is all it takes:

```python
import struct
def rsd_pcm_to_wav(rsd_path, wav_path):
    b = open(rsd_path,'rb').read()
    assert b[:8] == b'RSD4PCM '
    ch, bits, rate = struct.unpack_from('<III', b, 8)
    # samples begin after the header + name field; locate end of '*' padding:
    off = 20
    while off < len(b) and b[off] == 0x2A: off += 1
    data = b[off:]
    byte_rate = rate * ch * bits//8
    hdr = (b'RIFF' + struct.pack('<I', 36+len(data)) + b'WAVEfmt ' +
           struct.pack('<IHHIIHH', 16, 1, ch, rate, byte_rate, ch*bits//8, bits) +
           b'data' + struct.pack('<I', len(data)))
    open(wav_path,'wb').write(hdr + data)
```

The WAV `fmt` fields come straight from the RSD header — channels, rate, bits — because both formats
describe linear PCM the same way. This is why PCM extraction is trivial: the two containers wrap the *same*
samples.

**Extracting ADPCM.** For an ADPCM RSD (C18.2), insert a decode step before writing: run the samples through
the ADPCM state machine to produce 16-bit PCM, then write that as WAV. The decoder is small (a nibble loop
with an adaptive step table); the exact table/layout is the RSD ADPCM variant (🟡, C18.2), confirmed by
checking your decoded output against a sound you can hear in-game.

**Batch extraction from archives.** The interesting audio is packed (C19). Combine the RCF extractor (C3.4)
with this: pull each member out of `soundfx.rcf`/`carsound.rcf` by hash, recognise the `RSD4` magic, and run
it through this converter. Because RCF members keep their own magic (C3.3), an extracted sound self-identifies
as RSD even without its name. A whole sound bank falls out as WAVs in one pass.

**Why WAV.** WAV is the lowest-common-denominator audio container — every tool opens it, and its PCM form is
byte-compatible with RSD's PCM samples. Converting to WAV (rather than a compressed format) keeps the
extraction lossless and the pipeline simple: RSD-PCM → WAV-PCM is a header change, no re-encoding, no quality
loss. Re-encode to MP3/OGG later if you want; extract to WAV first.

**What happens if you bend it.**

- *Hardcode the sample offset at 0x20* — the `*` name field length can vary; scan past the padding (as
  above) or use the known header size. A wrong offset prepends garbage or clips the start.
- *Write the wrong WAV `fmt` fields* — mismatched channels/rate/bits play the sound wrong. Copy them from the
  RSD header exactly.
- *Forget to decode ADPCM* — you'll write compressed bytes into a PCM WAV and hear noise. Check the codec tag
  first (C18.1).
