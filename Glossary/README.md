# The Glossary

The glossary is the reference desk of this encyclopedia. Four pages:

- **[terminology.md](terminology.md)** — every acronym and concept used in the chapters, defined once.
- **[chunk-ids.md](chunk-ids.md)** — the master table of all 179 Pure3D chunk identifiers observed in
  the retail data set, with role and occurrence count. This is generated directly by the parser, so
  it is exhaustive for the shipped files, not a curated subset.
- **[extensions.md](extensions.md)** — a file-extension → format → chapter map, and a decision tree
  for identifying an unknown file.
- **[file-catalogue.md](file-catalogue.md)** — the whole retail data set, counted and sized.

## The identification workflow

When you meet an unknown file in this game, resolve it in this order — each step is a cheap test on
the first few bytes:

1. **Is it a RadCore archive?** First 22 bytes `RADCORE CEMENT LIBRARY` → an `.rcf` (see C3).
2. **Is it Pure3D?** First 4 bytes `50 33 44 FF` (`"P3D\xff"`) → a chunk tree (see C1).
3. **Is it Bink video?** First 3 bytes `BIK` → an `.rmv` FMV (see C20).
4. **Is it an RSD sound?** First 4 bytes `RSD4` → a sample container (see C18).
5. **Is it text?** Printable ASCII with `//` comments and `Name(args);` calls → a CON/MFK/CHO script
   (see C14–C17). If it starts with `<?xml` it is a Scrooby `.pag` page (see C21).

The portable identifier that implements this decision tree lives in
[extensions.md](extensions.md#a-portable-identifier).
