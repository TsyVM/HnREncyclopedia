# C2.1 — Names as Numbers: Why & Where

**What it is.** The design decision, made once and applied everywhere, to store references as 32-bit
integers rather than strings. It appears in three distinct layers of the game, and telling them apart
is the first step to working with any of them.

**How it works — the three layers.**

- **Chunk type ids** (C1). A chunk's `id` says what *kind* it is. This is a small, closed vocabulary —
  the [master table](../Glossary/chunk-ids.md) lists all 179 that occur in the retail data. You never
  hash to get one; you look it up.
- **Asset-name hashes.** Inside a Pure3D file, one object refers to another by the Radical hash of the
  target's name. A shader chunk names the texture it wants; a mesh names its shader; a locator names the
  thing it is attached to. At build time the artists' string `"tree_bark"` became a `uint32`, and the
  string was (usually) dropped. Resolution at load time is integer-to-object, via a name→object map the
  loader builds as it goes.
- **RCF directory keys.** The archive directory (C3) locates a member file by the Radical hash of its
  path. `scripts.rcf`'s 125 entries are `{hash, offset, size}` — no paths stored.

**Why it's built this way.** Three wins, all mattering on 2003 console hardware:

1. **Speed.** A 32-bit compare is one instruction; a string compare is a loop. Resolving thousands of
   asset references per level load is far cheaper as integer lookups.
2. **Size.** Dropping the source strings shrinks the shipped data — across 264 MB of `art/` and ten
   archives, the saved bytes are real.
3. **Stability.** An integer key is a fixed width and never contains awkward bytes, so directory and
   reference tables are simple fixed-stride arrays you can binary-search.

**Why it costs you.** The same erasure that helps the engine hurts the reverse engineer: a shipped
texture reference is a number, not the word `"tree_bark"`. You cannot grep the art for a name that is no
longer there. This is the central practical fact of the chapter and the reason [C2.4](04-collisions-and-recovery.md)
on name recovery exists.

**Where the names *survive*.** Crucially, the **plain-text scripts keep their strings**. Every
`.mfk` says `LoadP3DFile("art\cars\ambul.p3d")` in full; every `.con` is human-readable; character
`.cho` files name their targets. So the game ships both a hashed world *and*, in the scripts, a large
dictionary of the exact strings that were hashed. That asymmetry — binary references hashed, script
references in the clear — is what makes recovery tractable rather than hopeless.

**What happens if you bend it.** If you author a new asset and reference it by a hash you computed with
the *wrong* algorithm or the wrong string normalisation (case, slashes), the loader's map lookup misses
and the reference resolves to nothing — a missing texture, an unplaced object, a silent failure rather
than a crash. Get the hash exactly right (C2.2) or the reference is dead.
