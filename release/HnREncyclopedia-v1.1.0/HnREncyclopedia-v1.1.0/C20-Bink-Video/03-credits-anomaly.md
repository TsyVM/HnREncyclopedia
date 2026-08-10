# C20.3 — The `credits.rmv` Anomaly

**What it is.** The one movie file that breaks the pattern. Fifteen of the sixteen `.rmv` files are standard
Bink (C20.1); `credits.rmv` is not — and identifying *how* it differs is a small, instructive piece of
reverse-engineering forensics.

**How it works (✅ verified anomaly).** `credits.rmv`'s first 32 bytes:

```
00 70 00 00  00 70 00 00  00 70 00 00  78 6F 62 58   .p...p...p..xobX
03 00 00 00  80 02 00 00  E0 01 00 00  A7 14 00 00
```

Two things stand out. First, the magic is **not** `BIKi` — it's `00 70 00 00` (repeated), so a Bink player
would reject it. Second, at offset 12 sits the ASCII tag **`xobX`** — which is **"Xbox" byte-reversed**
(`X`,`b`,`o`,`x` stored little-endian as a 4-byte word reads `xobX`). Further in, the values `0x280 = 640`
and `0x1E0 = 480` appear — the familiar 640×480 dimensions — so it *is* a 640×480 movie, just in a different
container.

**What it most likely is (🟡 reasoned).** The `xobX`/"Xbox" tag strongly suggests `credits.rmv` is an
**Xbox-build artefact**: a movie packaged in the Xbox version's container format that was included in the PC
release by mistake, or a differently-muxed file the PC build handles specially. SHAR shipped on PC, PS2,
GameCube, and Xbox from one asset pipeline (C20.1); a cross-platform build occasionally leaves a
platform-specific file in the wrong release. The presence of `xobX` and non-Bink magic in an otherwise
all-Bink folder is the fingerprint of exactly that.

**Why document an anomaly at all.** Because a good reverse-engineering reference states the *boundary* of
what's known (the ⏳ marker) rather than hiding the messy file. "15 of 16 are Bink; the 16th is a non-Bink
`xobX` container, structure not yet decoded" is honest and useful: it tells a tool author to magic-check
every file (not assume Bink), and it flags `credits.rmv` as the one that needs special handling. Pretending
the folder is uniformly Bink would break any tool that hit `credits.rmv`.

**The lesson for tooling.** This is why the universal identifier (C4.6, Glossary) magic-checks every file
rather than trusting extensions: `credits.rmv` has the `.rmv` extension of a movie but not the Bink magic of
its siblings. A tool that keys off the extension mis-handles it; a tool that keys off the magic correctly
routes 15 files to the Bink path and flags the 16th as unknown. Content, not extension, is the truth (C3.3,
C18.4).

**Status.** `credits.rmv` container: ⏳ **Open** — identified as non-Bink and `xobX`-tagged, structure not
decoded. The other 15 movies: ✅ Bink.

**What happens if you bend it.**

- *Feed `credits.rmv` to a Bink player* — it rejects the file (wrong magic). Detect and route it separately.
- *Assume the `.rmv` extension means Bink* — 1 of 16 isn't. Magic-check.
- *Delete it as "corrupt"* — it's not corrupt, it's a different container. Leave it or investigate it, don't
  discard it.
