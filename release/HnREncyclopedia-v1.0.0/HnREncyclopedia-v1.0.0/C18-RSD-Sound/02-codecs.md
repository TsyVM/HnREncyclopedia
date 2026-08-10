# C18.2 — Codecs: PCM & ADPCM

**What it is.** The two sample encodings RSD carries. The codec tag in the header (C18.1) selects one, and
they trade size against simplicity: **PCM** is raw and large, **ADPCM** is compressed and needs decoding.

**PCM (✅ verified).** The loose sounds are `PCM ` — linear 16-bit samples, one after another, no
compression. To play them you just feed them to the audio hardware at the header's rate. This is the
simplest possible encoding: the bytes *are* the waveform. It's used where the sound is small and decode cost
should be zero — the UI accept/scroll blips (C18.1). Size for a 24 kHz mono 16-bit sound is
`24000 × 2 = 48,000` bytes per second, which is why PCM is reserved for short sounds.

**ADPCM (✅ verified via runtime).** The bulk of the game's audio — thousands of effects and voice lines in
the packed archives (C19) — is **ADPCM** (Adaptive Differential PCM). The RTTI proves it directly:
`IRadSoundAdpcmDecodeStream : IRadSoundHalDataSource` is a decode stream the engine runs to turn compressed
ADPCM into playable PCM on the fly. ADPCM stores the *difference* between successive samples with an adaptive
step size, typically at ~4 bits per sample — roughly a 4:1 compression over 16-bit PCM. For 173 MB of
dialogue (C19), that compression is what makes the voice fit.

**Why two codecs.** It's the classic size/CPU trade, and SHAR picks per use:

- **PCM** — zero decode cost, large. Used for tiny, frequently-triggered UI sounds where you want them to
  fire instantly with no decode.
- **ADPCM** — cheap decode, ~4× smaller. Used for the huge library of effects and voice where total size
  dominates and a little decode per sound is fine.

Having both in one container (`RSD4` + codec tag) means the audio pipeline is uniform — everything is an RSD
— while each sound picks the encoding that suits it. This is why the codec tag exists: it lets one format
serve both the instant UI blip and the compressed voice line.

**Decoding ADPCM.** ADPCM decode is a small state machine: for each 4-bit code, look up a step from an
adaptive table, add/subtract it from the running sample, and clamp. The exact table and nibble order are the
RSD/Radical ADPCM variant (🟡 — the *presence* of ADPCM is ✅ from `IRadSoundAdpcmDecodeStream`; the exact
byte layout of an ADPCM RSD is recovered by decoding a packed sound and checking it against the engine's
output, the C4.4 workflow). Once decoded, an ADPCM RSD is played identically to a PCM one.

**What happens if you bend it.**

- *Decode ADPCM as PCM* (or vice versa) — noise or silence. The codec tag is authoritative; branch on it.
- *Assume ADPCM's 4:1 ratio is exact* — it depends on the variant and block layout. Measure against real
  decoded output.
- *Re-encode PCM→ADPCM without matching the engine's variant* — the engine's decoder expects its exact ADPCM
  layout. Match it, or keep replacements PCM where size allows.
