# C20.4 — `binkw32.dll` & Playback

**What it is.** The decoder that actually plays the Bink movies — `binkw32.dll`, RAD Game Tools' Bink runtime,
shipped in the game directory. It's why the game can play video without implementing a codec itself.

**How it works (✅ verified presence).** The retail game folder contains **`binkw32.dll`** — the 32-bit
Windows Bink runtime. When the game plays a movie, it hands the `.rmv` file to this DLL, which opens it (the
`BIKi` header, C20.1), decodes each frame's video and audio, and blits the video to the screen while playing
the audio. The engine's job is just to tell Bink "play this file into this window" and to handle the
game-side wrapping (fade in/out, skip on button press, return to gameplay when done) — the actual video and
audio decoding is entirely inside `binkw32.dll`.

**Why ship a middleware DLL.** Video compression is a specialised, patent-heavy problem, and in 2003 there was
no good open option that ran across all four of SHAR's platforms. Bink was the industry-standard answer: RAD
Game Tools licensed a small runtime that decoded their proprietary format on PC, PS2, GameCube, and Xbox. For
Radical, dropping in `binkw32.dll` (and its console equivalents) was vastly cheaper and more reliable than
writing a cross-platform video codec. This is the same "license the hard part" logic as using Bink's sibling
audio tech and other middleware — the studio focuses on the game, not on reinventing a codec.

**The DLL as a verifiable tie.** `binkw32.dll`'s presence in the game folder is a *direct, on-disk
confirmation* of the FMV format: the movies are Bink because the Bink runtime is shipped to play them. This is
the same kind of file↔format tie as `eax.dll` confirming EAX reverb (C18.5) — the game carries the exact
middleware its data needs, so the middleware DLLs are a manifest of the formats in use. A folder with
`binkw32.dll` and `.rmv` files is unambiguously a Bink-video game.

**Playing the movies today.** Because Bink is well-known middleware, standard tools (RAD's own Bink tools,
and various open players that license or reimplement Bink decoding) open these `.rmv` files directly — no
game needed. To view or convert a cutscene, point a Bink-capable tool at the `.rmv`; the header (C20.1) and
codec are the same as any Bink file of that vintage. (`credits.rmv`, being non-Bink, C20.3, won't open this
way.)

**What happens if you bend it.**

- *Remove `binkw32.dll`* — the game can't play its movies; FMV objectives (C16.3) and the intro/logos fail.
  It's a required runtime.
- *Replace a movie with a non-Bink file* — `binkw32.dll` rejects it. Keep replacements as valid Bink of the
  same version (`BIKi`).
- *Assume you can decode Bink without the runtime* — the codec is proprietary; use the DLL or a
  Bink-licensed tool. Only the header is open.
