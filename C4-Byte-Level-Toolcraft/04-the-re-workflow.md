# C4.4 — The Reverse-Engineering Workflow

**What it is.** The repeatable procedure that produced this book, from an unknown blob to a field layout
you can trust — and the confidence discipline that decides when you are allowed to write "✅". It ties
the previous three pages into a loop.

**The loop.**

1. **Identify.** Magic test (Glossary identifier). Is it Pure3D, RCF, Bink, RSD, a script? This decides
   which container model (C1–C3) applies.
2. **Dump.** Tree-dump it (C4.2). Read the structure: which id families (C2.3), which chunk is the one
   you care about, where its own data begins (`off+12`) and ends (`off+headerSize`).
3. **Hypothesise a struct.** Scope a bounded reader to the chunk's own data (C4.1) and propose a field
   list — "u32 count, then `count` × (f32 x, f32 y, f32 z)". The header sizes constrain you: your struct
   must consume exactly `headerSize − 12` bytes, no more, no less.
4. **Validate across many files.** Run the hypothesis over *every* file that contains the chunk (the
   census tells you there are, say, 67,434 of them). A struct that reads cleanly and produces sane values
   across thousands of instances is strong; one that works on one file and raises on the next is wrong.
   The bounded reader makes this automatic — a bad struct raises at a known offset.
5. **Cross-check the value.** Where possible, tie the number to something observable: a bounding box
   should enclose the mesh's vertices; a sample rate should be a real audio rate (the RSD `0x5DC0` reads
   as 24,000 Hz — a plausible rate, which corroborates the field); a top-speed float should match the
   `.con` value that produced it. Corroboration promotes a guess.
6. **Mark confidence and move on.** Assign ✅/🟡/⏳ honestly (below), record the layout, add a decoder
   (C4.6), and return to step 2 for the next chunk.

**The confidence ladder — the rule for each marker.**

- **✅ Verified.** You can *reproduce* it. On-disk: a parser reads it from the shipped bytes and the same
  read works across the population (the census, the RCF directory, the header layouts in C1/C3). Runtime:
  it is in the executable's RTTI (C4.5). The test is reproducibility on the reader's own copy.
- **🟡 Reasoned.** The layout or name fits *all* evidence and contradicts none, but rests on inference —
  a name from public Pure3D convention, a field role deduced from behaviour rather than proven from bytes.
  Most decoded semantics start here and get promoted to ✅ when a cross-check nails them.
- **⏳ Open.** You know the chunk exists (it's in the census) but not yet what its bytes mean, or you know
  a runtime class exists (RTTI) but not its member offsets. State the boundary; do not fill it with a
  guess dressed as fact.

**Why the discipline matters more than the result.** A reverse-engineering document is only as useful as
it is trustworthy. A single confidently-wrong "✅" poisons everything a reader builds on it. It is far
better to ship a ⏳ that says "this 24-byte chunk is not yet decoded" than a ✅ that says "these are XYZ
positions" when you validated it on one file. The markers are a promise about *how you know*, and keeping
that promise is what makes the book safe to build on — which is exactly why the on-disk claims here are
tied to a re-runnable parser and the runtime claims to the executable's own RTTI.

**What happens if you bend it.**

- *Promote to ✅ on one file* — the population is the proof. Validate across the census before you claim
  verified.
- *Let a struct "mostly work" with a fudge* (skip a few bytes to make it fit) — the skipped bytes are a
  field you haven't understood. An honest ⏳ on those bytes beats a ✅ on a struct with a hole in it.
- *Decode without cross-checking values* — a layout that parses is not a layout that is *right*. Tie at
  least one field to something observable before you trust the rest.
