# C2.5 — Hashing in Practice

**What it is.** The two everyday operations the hash enables: **find a file in an RCF by its path**, and
**match a Pure3D asset reference to the object it names**. Both are short; both appear constantly in the
later chapters.

**Finding a file in an RCF.** The archive directory (C3) is a sorted array of `{hash, offset, size}`.
To pull `scripts\cars\ambul.con` out of `scripts.rcf`:

```python
key = radical_hash('scripts\\cars\\ambul.con')   # normalise + hash (C2.2)
entry = directory.get(key)                        # dict or binary search of the sorted array
if entry:
    data = archive[entry.offset : entry.offset + entry.size]
```

Because the directory is keyed by hash, you *must* reproduce the engine's normalisation exactly (lower
case, backslashes). When a lookup misses, suspect the string form before the algorithm — round-trip a
name you know works to prove your hasher, then fix the path form.

**Matching a Pure3D reference.** As the loader walks a `.p3d` (C1.8) it builds a map from each named
object's hash to the live object. A shader chunk that references texture `0x1A2B3C4D` is resolved by
looking that key up in the map. Offline, you reproduce this by:

1. First pass — walk the tree, and for every chunk that carries a **name** in its own data, record
   `hash(name) → chunk`. (Which chunks carry names, and where, is per-family — Chapters 5–8.)
2. Second pass — for every chunk that carries a **reference** `uint32`, resolve it against the map from
   pass one.

Two passes because a reference can point forward to an object defined later in the file; build the whole
name map first, then resolve.

**Building a project-wide name map.** Combine C2.4's script-mined dictionary with the per-file name maps
and you get a single table that resolves most hashes across the whole game to readable names. Persist it
as a simple `hash,name` CSV and every tool you write can annotate its output:

```python
names = load_csv('names.csv')                     # hash -> name, from scripts + recovery
def label(h): return names.get(h, f'0x{h:08X}')
```

This is precisely how the [master chunk table](../Glossary/chunk-ids.md) annotates chunk *type* ids, and
how a good dumper annotates asset *reference* ids — the difference is only which table you look in (the
closed 179-id type table vs. the open recovered-name table).

**Why do it once, centrally.** Asset references cross files — a mission `.p3d` references a car texture
defined elsewhere. A per-file map resolves only local names; a project-wide map resolves the
cross-references that make the asset graph navigable. Build it once, reuse it everywhere.

**What happens if you bend it.** Resolving references against a *partial* name map silently leaves real
references as hex and can hide that an asset is missing entirely. Always report the unresolved count:
a dump that says "312 references, 40 unresolved" is honest; one that silently prints hex for the 40 hides
a gap in your dictionary.
