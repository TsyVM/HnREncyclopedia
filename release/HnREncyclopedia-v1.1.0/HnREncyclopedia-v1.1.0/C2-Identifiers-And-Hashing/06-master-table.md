# C2.6 — The Master Table as a Tool

**What it is.** The [`Glossary/chunk-ids.md`](../Glossary/chunk-ids.md) table is not decoration — it is a
working tool, generated directly by the parser from the shipped files, and it is the fastest way to
identify any chunk you meet. This page is how to *use* it.

**How it was made (✅ verified, reproducible).** `tools/p3d_rcf_scan.py` walks all 1,941 `.p3d` files,
counts every chunk id, and records whether each ever appears as a container. The table is its output:
179 rows, each an id, its role, and its exact occurrence count. Re-run the scanner on your own copy and
you get the same 179 rows — the table is a *measurement*, not a hand-curated list, which is why it can be
trusted as the closed set of ids that exist in the retail data.

**Using it to identify a chunk.** When the dumper prints `0x00121110 [L] ...`, look it up: it is the
collision "vector list" leaf, the second-most-common chunk in the game, documented in Chapter 11. Three
columns answer three questions:

- **Role** tells you whether to expect children (and cross-checks your walk — if the table says a given
  id is only ever a leaf but your walk found children, suspect a desync, C1.7).
- **Occurrence count** tells you whether a chunk is core (hundreds of thousands) or rare (a handful) —
  rare ids are where undiscovered structure and edge cases hide.
- **Name** (🟡/⏳) points you at the chapter, or flags the id as still-Open.

**Using it as a validator.** The table is the closed vocabulary of the retail data, so it doubles as a
sanity check: any id your walk produces that is *not* in the table is a red flag — either a desync
(you're reading data as a header) or a file that isn't retail (a mod, a different platform build). The
forensic walker in [C1.7](../C1-Pure3D-Container-Model/07-failure-modes.md) uses exactly this test.

**Using it to prioritise reverse engineering.** Sort by occurrence and you get the game's own priority
list: decode `0x00011003`, `0x00121110`, `0x00011005`, `0x00121100`, `0x00011004` first and you have
explained the overwhelming majority of all chunk *instances* in the game — the **shader parameters**
(`0x0001**1**xxx`) and **collision** (`0x0012**1**xxx`) that dominate by raw count. The long tail of
rare ids can wait. This priority is exactly why Part II opens on textures, shaders, and meshes: those
families, by count, are most of the game — and decoding them (C5–C7) is what promoted their names in
this table from 🟡 to ✅.

**Keeping it current.** If you extend the game (a mod adds a chunk id) or study another platform build,
regenerate the table from *that* data set rather than editing this one by hand. The table is only
trustworthy because it is generated; a hand-edited table is a claim, not a measurement.

**What happens if you bend it.** Treating the name column as verified fact is the one misuse to avoid —
names are 🟡 reasoned, from public Pure3D convention, not byte-proven in this data set. The id, role, and
count are solid; the name is a signpost. When a name matters to correctness, confirm it by decoding the
chunk in its chapter.

**Next:** [Chapter 3 — RCF Archives & the Virtual File System](../C3-RCF-Archives-VFS/C3-RCF-Archives-VFS.md).
