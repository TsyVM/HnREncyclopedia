# Chapter 2 — Identifiers & Radical Hashing

> **Goal of this chapter:** understand every place *The Simpsons: Hit & Run* replaces a human name with
> a 32-bit number — chunk type ids, asset names inside Pure3D, and the keys of the RCF archives — and be
> able to go both directions: name → number to *find* a thing, and number → name to *recover* one.

Chapter 1 showed that a `.p3d` file is a tree of chunks, each tagged by a 32-bit `id`. That id is the
first of three numbering schemes the engine uses in place of text:

1. **Chunk type ids** — the `0x00019000`-style codes that say *what kind* of chunk this is.
2. **Asset name hashes** — inside Pure3D, objects reference each other (a shader names its texture, a
   mesh names its shader) by the **Radical hash** of a name string, not by the string.
3. **RCF directory keys** — the ten `RADCORE CEMENT LIBRARY` archives (Chapter 3) locate a file by the
   Radical hash of its path. The retail `scripts.rcf` directory stores **125 entries keyed by hash**,
   with no plaintext filenames at all (✅ verified in Chapter 3).

All three exist for the same reason: comparing and looking up a 32-bit integer is faster and smaller
than comparing strings, and it lets the engine drop the source text from the shipped build entirely.
The cost — the thing this chapter arms you against — is that a shipped asset often no longer contains
the words a human would search for.

---

## Deep-dive pages

- [C2.1 — Names as Numbers: Why & Where](01-names-as-numbers.md): the three numbering schemes and the trade they make.
- [C2.2 — The Radical String Hash](02-the-radical-hash.md): the algorithm `radLoadObject` and the RCF directory use, with a portable implementation.
- [C2.3 — Chunk-ID Families](03-chunk-id-families.md): reading structure out of the id space (`0x0001xxxx`, `0x0012xxxx`, `0x03F0xxxx`).
- [C2.4 — Collisions & Name Recovery](04-collisions-and-recovery.md): dictionaries, brute force, and recovering names from the scripts.
- [C2.5 — Hashing in Practice](05-hashing-in-practice.md): finding a file in an RCF, matching an asset reference, building a name map.
- [C2.6 — The Master Table as a Tool](06-master-table.md): using the generated 179-id table to identify anything.

---

## 2.1 Three numbering schemes, one motive

A chunk `id` (C1) is an opaque type code. An **asset name hash** turns a string like `"homer_body"`
into a `uint32` the moment the asset is built, so runtime cross-references are integer compares. An
**RCF key** is the Radical hash of a path like `"scripts\cars\ambul.con"`. The first is a small fixed
vocabulary (179 values, [master table](../Glossary/chunk-ids.md)); the second and third are open sets —
any name the artists chose.

## 2.2 The Radical hash (🟡 reasoned; keys ✅ verified)

Radical's asset/loader hash is a 32-bit string hash — the function behind `radLoadObject` lookups and
the RCF directory keys. The DonutsSDK `hashing` module reproduces it as `constexpr`, and the RCF
directory keys in `scripts.rcf` are numerically consistent with a per-character multiply-add hash over
the lowercased, backslash-normalised path. The *algorithm* is presented here as 🟡 Reasoned (it matches
the SDK and all observed keys but is not proven byte-for-byte against a shipped name list, because the
shipped directory stores only the hashes). The *fact that RCF keys are hashes* is ✅ Verified — the
directory contains `{hash, offset, size}` triples and no strings ([C3](../C3-RCF-Archives-VFS/C3-RCF-Archives-VFS.md)).
The full algorithm and code are [C2.2](02-the-radical-hash.md).

## 2.3 The id space has structure

Chunk ids are not random. The census groups them into visible families:

- `0x0001xxxx` — **shaders, textures, meshes** (the `0x00010000` shader family, `0x00011000` primitive
  groups, `0x00019000` textures). The most numerous group by far.
- `0x0012xxxx` — **collision** (`0x00121xxx` volumes and vectors; `0x00120xxx` collision data).
- `0x03F0xxxx` — **scene graph** (root, branch, transform, drawable, sort order).
- `0x0300xxxx` — **paths and fences** (navigation and barrier geometry).
- `0x0701xxxx` — **locators/frames**.

Recognising the family from the top half of an id is often enough to know which chapter to open, before
you decode a byte. [C2.3](03-chunk-id-families.md) maps the space.

## 2.4 Recovering names

Because names ship as hashes, reverse lookup is a real task. Three techniques, in order of yield:
mine the **plain-text scripts** (`.mfk`/`.con`/`.cho` are full of real paths and names — Chapters
14–17), build a **dictionary** of those names and hash it forward to match unknown keys, and only then
**brute force** short names. The RCF directory is the ideal proving ground: hash every path you find in
the scripts and see which of the 125 keys light up. [C2.4](04-collisions-and-recovery.md) is the
workflow.

## 2.5 & 2.6 Using it

To find `scripts\cars\ambul.con` inside `scripts.rcf`, you hash the path and binary-search the
directory (C2.5). To identify an unknown chunk, you look its id up in the generated
[master table](../Glossary/chunk-ids.md) (C2.6). Both are small, both are covered in their pages.

---

## Key takeaways

- The engine replaces text with 32-bit numbers in three places: chunk type ids, asset-name references,
  and RCF directory keys.
- Chunk ids are a closed set of **179** values (verified); asset/RCF hashes are an open set produced by
  the Radical string hash.
- RCF directories are **hash-keyed with no stored filenames** (✅) — name recovery is therefore a
  first-class task, and the plain-text scripts are the richest source of real names.
- Read the id families (`0x0001`, `0x0012`, `0x03F0`, `0x0300`, `0x0701`) to jump straight to the right
  chapter.

**Next:** [Chapter 3 — RCF Archives & the Virtual File System](../C3-RCF-Archives-VFS/C3-RCF-Archives-VFS.md).
