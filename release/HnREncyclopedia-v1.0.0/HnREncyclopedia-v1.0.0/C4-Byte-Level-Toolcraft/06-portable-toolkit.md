# C4.6 — A Portable Toolkit You Keep

**What it is.** The assembled workbench: the small set of modules built across C1–C4 that every later
chapter reuses unchanged. The design goal is a **fixed substrate plus growing decoders** — the walker,
reader, writer, dumper, and identifier never change, and each chapter adds exactly one decoder for one
chunk family on top.

**The five fixed pieces.**

1. **The identifier** (Glossary/extensions) — magic → format. The front door; decides which model applies.
2. **The walker** (C1.3) — `walk` / `walk_tree`, the bounded chunk iterator. Correct for all 179 ids.
3. **The bounded reader/writer** (C4.1) — safe field reads; size-honest serialisation.
4. **The tree dumper** (C4.2) — annotated outline; also the census/histogram tool.
5. **The differ** (C4.3) — locate a field by changing one thing.

None of these know anything about textures, meshes, or collision. That is the point: they are the parts
that are *done*, proven against all 1,941 files, and never need revisiting.

**The growing part: one decoder per family.** A decoder is a function that takes a chunk's `(buf, off,
headerSize, chunkSize)` and returns structured fields — the product of the C4.4 workflow for that family.
The architecture is:

```python
DECODERS = {}                                   # chunk id -> function(own_reader) -> dict
def decoder(cid):
    def reg(fn): DECODERS[cid] = fn; return fn
    return reg

@decoder(0x00019000)                            # Texture (Chapter 5)
def dec_texture(r):
    return { 'width': r.u32(), 'height': r.u32(), 'bpp': r.u32(), '...': '⏳' }

def decode_chunk(buf, off, h, d):
    own = Reader(buf, off+12, off+h)            # scoped to the chunk's own data (C4.1)
    fn = DECODERS.get(struct.unpack_from('<I', buf, off)[0])
    return fn(own) if fn else None              # unknown -> None, harmless (C1.8)
```

Every chapter from 5 onward contributes entries to `DECODERS`. The dumper (C4.2) consults it to print
decoded fields inline; unknown ids fall through to `None` exactly as the engine skips unknown chunks
(C1.8). The book and the toolkit grow the same way: the container model is finished; the decoders
accumulate.

**Why this shape.** It mirrors the engine itself — a generic loader plus a registry of per-id handlers
(C1.8) — and it mirrors DonutsSDK's data library, which is precisely a P3D/CON/RSD/RCF walker plus a
growing set of typed readers. Building your tools this way means your code and the engine's stay
structurally parallel, which is what makes a decode you write *testable against the game*: if the engine
loads a file your walker+decoders read cleanly, and rejects one they choke on, your model matches its
model.

**Portability.** Everything here is raw-byte logic — no engine headers, no platform calls, no external
libraries beyond `struct`. It runs anywhere Python (or C) runs, which is why the same code documents the
PC retail data today and could be pointed at another platform build tomorrow by changing only the
endianness in the reader (C1.4) and the platform-specific decoders. The knowledge is in the layouts and
the method, not in any one program — which is the whole reason this book is written format-first.

**What happens if you bend it.** The one anti-pattern to avoid is letting a decoder reach *outside* its
scoped reader — reading a sibling chunk's bytes because "they're right there." A decoder that respects
its `own` bounds (C4.1) composes safely into the dumper and the census; one that reaches across chunk
boundaries breaks the moment the layout shifts. Keep decoders local to their chunk; let the walker handle
structure.

**Next:** Part II — [Chapter 5, Textures & Images](../README.md#chapters) — applies the whole toolkit to
`0x00019000`, the texture family, and the most common chunks in the game.
