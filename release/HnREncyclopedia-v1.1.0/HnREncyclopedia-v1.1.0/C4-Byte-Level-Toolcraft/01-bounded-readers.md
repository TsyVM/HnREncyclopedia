# C4.1 — Bounded Readers & Writers

**What it is.** The two primitives every tool in this book stands on: a **reader** that physically cannot
run past the end of the region it was given, and a **writer** that recomputes container sizes so the
output always balances (C1.5, C3.4). Get these two right and every parser above them inherits their
safety.

**How the reader works.** The reader carries a current offset and a hard `end`, and *every* accessor
calls `need(n)` first. A read that would cross `end` raises immediately, at the exact offset, instead of
returning a garbage value that propagates.

```python
import struct
class Reader:
    def __init__(self, buf, start=0, end=None):
        self.b, self.o = buf, start
        self.end = len(buf) if end is None else end
    def need(self, n):
        if self.o + n > self.end:
            raise EOFError(f"want {n} bytes at {self.o}, region ends {self.end}")
    def u8(self):  self.need(1); v=self.b[self.o];               self.o+=1; return v
    def u16(self): self.need(2); v=struct.unpack_from('<H',self.b,self.o)[0]; self.o+=2; return v
    def u32(self): self.need(4); v=struct.unpack_from('<I',self.b,self.o)[0]; self.o+=4; return v
    def i32(self): self.need(4); v=struct.unpack_from('<i',self.b,self.o)[0]; self.o+=4; return v
    def f32(self): self.need(4); v=struct.unpack_from('<f',self.b,self.o)[0]; self.o+=4; return v
    def bytes(self, n): self.need(n); v=self.b[self.o:self.o+n]; self.o+=n; return v
    def pstr(self):                      # Pure3D length-prefixed string: u8 len + chars
        n = self.u8(); return self.bytes(n).decode('latin-1')
```

Two details that matter in this game: default **little-endian** (C1.6), and a `pstr` helper because
Pure3D stores names as a **one-byte length followed by the characters** (🟡 — the common Pure3D string
form; confirm per chunk when a name field is in play).

**Why bound every read.** Reverse engineering means pointing a parser at bytes whose layout you are still
guessing. An unbounded reader rewards a wrong guess with a plausible-looking wrong number; a bounded one
turns the same wrong guess into an exception at a known offset — which is *information* (your struct is
too long, or you started at the wrong place). The reader that fails loudly is the one that teaches you.

**How the writer works.** The mirror of the reader: build a chunk tree as nested objects, then serialise
**bottom-up**, measuring children before writing the parent's `chunkSize` (the `rebuild()` from
[C1.5](../C1-Pure3D-Container-Model/05-editing-and-repacking.md)). The writer never lets you hand-set a
size — it computes every `headerSize`/`chunkSize` from the actual bytes, so the size tree cannot go stale.
The same principle rebuilds an RCF directory (C3.4): compute offsets and sizes from the real layout, sort,
write.

**Scoping a reader to a chunk.** The pattern you use constantly: given a chunk at `(off, headerSize,
chunkSize)`, make a reader bounded to its **own data** and another to its **children**:

```python
own      = Reader(buf, off+12,        off+headerSize)   # this chunk's fields
children = Reader(buf, off+headerSize, off+chunkSize)   # its child chunks
```

Now a decoder for that chunk can read its fields from `own` and know it will raise the instant it tries to
read past its own data into a child — a built-in check that your field list is the right length.

**What happens if you bend it.**

- *Use an unbounded `struct.unpack_from` directly* and a wrong offset reads neighbouring data as your
  field — the silent-wrong-answer failure this whole chapter exists to prevent. Read through the bounded
  reader.
- *Set a `chunkSize` by hand in the writer* and you reintroduce exactly the stale-ancestor bug of C1.5.
  Let the writer compute it.
- *Reuse one reader across a chunk boundary* instead of scoping to `own`/`children` and you lose the
  free length check; scope readers to the region you mean to read.
