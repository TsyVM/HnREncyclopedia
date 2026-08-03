# C20.1 — The Bink Container

**What it is.** The header and structure of a Bink video file — the format 15 of the game's 16 FMVs use. Bink
(RAD Game Tools) was the dominant game-FMV middleware of the 2000s, and its container is compact and
self-describing.

**How it works (✅ verified).** A Bink file opens with the magic `BIKi` (the last byte is the codec version —
`i` here) followed by little-endian `uint32` fields. Decoded from `movies/fmv2.rmv`:

```
offset 0:  42 49 4B 69   "BIKi"                 magic + version
offset 4:  fileSize     = 17,053,576            total length minus 8
offset 8:  numFrames    = 1,333
offset 12: largestFrame = 107,468               biggest frame in bytes (buffer sizing)
offset 16: (frames again / flags)
offset 20: width  = 640
offset 24: height = 480
offset 28: fpsDividend = 30
offset 32: fpsDivider  = 1                       → 30.000 fps
```

The frame rate is stored as a **fraction** (dividend/divider) so non-integer rates (e.g. 29.97) are exact;
here it's a clean 30 fps. `largestFrame` tells the player how big a decode buffer to allocate — no frame
exceeds it. After the header come per-frame offset tables and then the interleaved frame data.

**How Bink stores a frame.** Bink interleaves **video and audio per frame**: each frame packet contains that
frame's compressed image plus the audio samples for that frame's duration. A player reads a frame packet,
decodes the image (Bink's proprietary DCT-like codec) and the audio (Bink's ADPCM-like audio), displays the
image, and queues the audio — then moves to the next frame. This interleaving is what keeps audio and video
in sync during streaming: they arrive together, frame by frame.

**Why Bink.** Implementing a video codec is hard and patent-encumbered; Bink solved it as middleware that ran
on every platform of the era (PC, PS2, GameCube, Xbox) with a small, licensable runtime. For a studio like
Radical, licensing Bink was far cheaper than writing a codec, and it gave consistent FMV across all four
platforms SHAR shipped on. The `BIKi` magic and this header are the same on every platform — which is why 15
of the PC files are standard Bink (and why the one that *isn't*, C20.3, stands out).

**Reading it in code.**

```python
def bink_header(b):
    assert b[:3] == b'BIK'
    import struct
    fileSize, numFrames, largestFrame = struct.unpack_from('<III', b, 4)
    width, height = struct.unpack_from('<II', b, 20)
    fdiv, fden = struct.unpack_from('<II', b, 28)
    return dict(version=chr(b[3]), frames=numFrames, w=width, h=height, fps=fdiv/fden)
```

**What happens if you bend it.**

- *Assume a fixed frame rate* — it's a fraction; compute `dividend/divider`. Assuming 30 for a 29.97 file
  drifts sync.
- *Ignore `largestFrame`* — it sizes the decode buffer; a player that under-allocates overflows on the
  biggest frame. Honour it.
- *Try to decode Bink by hand* — the codec is proprietary; use the Bink runtime (`binkw32.dll`, C20.4) or a
  tool that licenses it. The header is open; the codec is not.
