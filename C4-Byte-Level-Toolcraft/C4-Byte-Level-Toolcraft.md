# Chapter 4 — Byte-Level Toolcraft

> **Goal of this chapter:** assemble the small, portable toolkit — bounded readers, tree dumpers, hex
> diffs — and the *method* used to produce the rest of this book, so you can decode a chunk nobody has
> documented and know when your decode is right. This is the chapter that makes the others reproducible.

Chapters 1–3 gave you the three container models of the game: the Pure3D chunk tree, the Radical hash,
and the RCF archive. This chapter is the workbench under them. None of the code here is specific to one
asset type; it is the reusable substrate — the same bounded reader parses a mesh header and a collision
volume, the same tree dumper prints a car and a level, the same diff finds the four bytes a tuning
change touched. Everything is toolkit-agnostic (raw bytes, no engine SDK required) so it outlives any one
program, and everything is designed to **fail loudly** rather than silently mis-parse — the single most
important property when you are reverse engineering, because a quiet wrong answer costs far more than a
crash.

The concrete proof that this toolkit is sufficient: the shipped
[`tools/p3d_rcf_scan.py`](../tools/p3d_rcf_scan.py) is built from exactly these pieces, and it parses all
1,941 Pure3D files and the RCF directories with zero failures.

---

## Deep-dive pages

- [C4.1 — Bounded Readers & Writers](01-bounded-readers.md): the reader that cannot run off the end, and the writer that keeps the size tree honest.
- [C4.2 — Tree Dumpers & Annotation](02-tree-dumpers.md): turning a file into a readable outline, annotated from the master table and recovered names.
- [C4.3 — Hex Diffing: Finding What a Change Touched](03-hex-diffing.md): the fastest way to locate a field — change one thing in-game and diff.
- [C4.4 — The Reverse-Engineering Workflow](04-the-re-workflow.md): from an unknown blob to a confident field layout, with confidence discipline.
- [C4.5 — RTTI & the Verified Class Set](05-rtti-and-class-set.md): what the executable's own type data proves, and how this book uses it.
- [C4.6 — A Portable Toolkit You Keep](06-portable-toolkit.md): the modules assembled, and how each later chapter plugs in one decoder.

---

## 4.1 Read defensively

Every parser in this book is built on a reader that **checks before it reads**. The format's own rules
(C1) already tell you a chunk's bounds; the reader enforces them, so a truncated or misaligned file stops
at the first bad byte instead of returning nonsense:

```python
import struct
class Reader:
    def __init__(self, buf, start=0, end=None):
        self.b, self.o, self.end = buf, start, len(buf) if end is None else end
    def need(self, n):
        if self.o + n > self.end: raise EOFError(f"want {n} at {self.o}, end {self.end}")
    def u32(self): self.need(4); v=struct.unpack_from('<I',self.b,self.o)[0]; self.o+=4; return v
    def f32(self): self.need(4); v=struct.unpack_from('<f',self.b,self.o)[0]; self.o+=4; return v
    def bytes(self, n): self.need(n); v=self.b[self.o:self.o+n]; self.o+=n; return v
```

Bounded by construction, little-endian by default (C1.6). [C4.1](01-bounded-readers.md) adds the writer
that recomputes sizes on the way out (C1.5, C3.4).

## 4.2 Dump before you decode

The first thing you do to any file is dump its structure. The tree dumper from
[C1.6](../C1-Pure3D-Container-Model/06-universal-opener.md), fed the
[master chunk table](../Glossary/chunk-ids.md) as names, turns a wall of bytes into an annotated outline
you can *read*. The shape alone usually tells you the asset class (C2.3), and the annotation tells you
which chapter to open. [C4.2](02-tree-dumpers.md) extends it with recovered asset names (C2.5) so
references read as words.

## 4.3 Diff to find a field

The single fastest reverse-engineering technique in this game: change **one** thing and diff the bytes.
Bump a car's `SetTopSpeedKmh` in its `.con` (Chapter 15), or nudge one slider, save, and byte-diff the
before/after. The handful of bytes that changed *are* the field. Because so much of SHAR's tunable data
is in plain-text scripts, this is often trivial; for binary data it is still the surest way to map a value
to an offset. [C4.3](03-hex-diffing.md).

## 4.4 Decode with a confidence ladder

A decode is not "done" when it produces numbers — it is done when the numbers are *proven*. This book's
markers (✅/🟡/⏳) are a discipline: a field is ✅ only when you can reproduce it from bytes or read it from
RTTI; it is 🟡 when the layout fits all evidence but rests on inference; it is ⏳ when you know a chunk
exists but not yet what its bytes mean. [C4.4](04-the-re-workflow.md) turns this into a repeatable
procedure: dump → hypothesise a struct → validate across many files → mark confidence.

## 4.5 The executable proves the class model

On-disk toolcraft explains files; the runtime half of the book rests on a different, equally hard
evidence base — the **RTTI the compiler left in `Simpsons.exe`**. DonutsSDK's `shar_dumps.csv` carries
**1,207 classes and 3,924 base-class relationships** read straight from the executable's
`_RTTIBaseClassDescriptor` records. That is why Part VII can name `Vehicle`, `sim::SimState`,
`CharacterAi` with ✅ confidence while marking their member offsets ⏳. [C4.5](05-rtti-and-class-set.md)
explains what RTTI does and does not prove.

## 4.6 Keep the toolkit

By the end you have five reusable pieces — reader, writer, dumper, differ, and the identifier from the
Glossary — and every later chapter adds exactly one *decoder* on top. That frozen-substrate/growing
-decoders shape is the architecture of both this book and the DonutsSDK data library.
[C4.6](06-portable-toolkit.md).

---

## Key takeaways

- Build on a **bounded reader**: check, then read; fail loudly, never silently mis-parse.
- **Dump before you decode** — structure and (annotated) names tell you the asset class and the chapter.
- **Diff to find a field**: change one value, diff the bytes; SHAR's plain-text scripts make this easy.
- Hold a **confidence ladder**: ✅ reproduced from bytes/RTTI, 🟡 reasoned, ⏳ open — and never promote a
  guess.
- The **executable's RTTI** is the second evidence base; it proves classes and inheritance, not offsets.
- The toolkit is a fixed substrate; each chapter adds one decoder.

**Next:** [Chapter 5 — Textures & Images](../README.md#chapters) opens Part II by applying all of this to
the most common chunks in the game.
