# C23.6 — Using the DonutsSDK Class Database

**What it is.** How a mod actually *uses* the verified class set — the `shar::db` module DonutsSDK generates
from `shar_dumps.csv`. This page closes the chapter by turning the data into a tool.

**How it works.** The SDK's `tools/gen_shar_db.py` compiles the CSV into `shar_db.inl` — `constexpr` tables of
`ClassInfo` (name, namespace, vtable address if known, size if known) and `BaseRelation` (child → base),
sorted for binary search. A mod queries them:

```cpp
#include <donutsdk/mod.hpp>
using namespace donutsdk;

void my_mod() {
    // Identify a live object by its vtable (C23.5) against the verified DB:
    if (const shar::db::ClassInfo* cls = shar::identify(some_obj))
        log.print("class: %.*s\n", (int)cls->name.size(), cls->name.data());

    // Ask the verified inheritance graph a question:
    if (shar::db::derives_from(some_obj, "IEntityDSG"))
        // …it's a scene entity (C23.2); safe to treat as one.
}
```

Everything the DB returns is ✅ verified — names and inheritance from RTTI. What it does *not* give you is a
member offset; those you supply yourself from a diff (C4.3), and the SDK takes them as clearly-marked
user-supplied values (`view.at<T>(offset)`), never as DB facts.

**Why generate it from the CSV.** The single-source-of-truth discipline (shared with the chunk registry of
the SDK's `p3d/chunks.hpp`) means the class DB is a *measurement*, not a hand-maintained list: improve the RE
data set (`shar_dumps.csv`), regenerate, and the DB is current. Never hand-edit `shar_db.inl` — regenerate it.
This is why the DB can be trusted as the verified set: it is produced mechanically from the executable's own
RTTI.

**What the DB is good for today.** Three things, all offset-free and therefore solid:

1. **Type identification** — "what is this object?" (C23.5), for filtering and logging.
2. **Inheritance queries** — "is this a `Vehicle`? a scene entity? an `EventListener`?" — for deciding whether
   an operation is safe.
3. **Documentation** — the DB *is* the runtime map; browsing it (or this book's runtime chapters) tells you
   what classes exist and how they relate, which is the starting point for any RE work.

**Where it grows.** As member offsets and vtable addresses are recovered (by diffing and disassembly, C4.3/
C23.5), they flow into the CSV and regenerate into the DB — each one promoting a class from "named and
identifiable" to "named, identifiable, and readable." The DB is the ledger of that progress: what is ✅ today,
and what is still ⏳.

**What happens if you bend it.**

- *Hand-edit `shar_db.inl`* — your edit is lost on regeneration and breaks the source-of-truth guarantee.
  Edit the CSV and regenerate.
- *Treat a DB `object_size`/`vtable_va` of 0 as real* — 0 means "not yet recovered" (⏳), not "zero." Check
  before relying on it.
- *Build offset-dependent logic on DB facts* — the DB gives names and inheritance; offsets are yours to
  supply and verify. Keep the two clearly separated.

**Next:** [Chapter 24 — Vehicles at Runtime](../C24-Vehicles-Runtime/C24-Vehicles-Runtime.md).
