# C4.5 — RTTI & the Verified Class Set

**What it is.** The second evidence base of this book. On-disk toolcraft (C4.1–C4.4) explains *files*;
the running-game half of the book — Part VII, and every "the loader builds a `Vehicle`" aside — rests on
the **Run-Time Type Information the compiler left in `Simpsons.exe`**. This page explains what that data
is, what it proves, and what it does not.

**What RTTI is.** When a C++ program uses polymorphism (virtual functions, `dynamic_cast`), the compiler
emits metadata describing each class: a type descriptor with the class's **name**, and — for MSVC, which
built the retail PC executable — `_RTTIBaseClassDescriptor` records describing its **base classes** and
how their sub-objects are laid out within the derived class. This metadata is compiled *into the shipped
binary*. It is not a guess, a leak, or an external claim; it is the program describing its own types to
itself, and it can be read straight out of the `.exe`.

**What has been extracted (✅ verified).** DonutsSDK's `data/shar_dumps.csv` is that extraction:
**1,207 RTTI-confirmed classes** and **3,924 base-class relationships**, each row tagged `CONFIRMED`
because it comes directly from a `_RTTIBaseClassDescriptor` in `Simpsons.exe`. From it you get, with
certainty:

- **Class existence and exact names** — `Vehicle`, `VehicleCentral`, `Character`, `CharacterAi`,
  `sim::SimState`, `sim::SimulatedObject`, `SuperCam`, `tDrawable`, `IEntityDSG`, `CollisionEntityDSG`,
  namespaced exactly as the engine names them.
- **Inheritance** — that `sim::SimulatedObject` derives from `tEntity`, that `sim::SimState` carries
  `tRefCounted`/`radLoadObject`/`IRefCount` sub-objects at offset 0, and so on — including the byte
  offset of each base sub-object within the derived class, which RTTI records explicitly.

**What RTTI does *not* prove (⏳ Open).** RTTI describes the *type lattice*, not the full memory layout of
non-base members. It does **not** give you: the offset of an arbitrary data member like a vehicle's
top-speed float; the address of a method or the loader for a chunk; the address of a singleton or manager.
Those are recovered by *other* means — disassembly, the hex/memory diffing of C4.3 — and until they are,
this book marks them ⏳ and the SDK leaves them as explicit `TODO`s rather than inventing them. This is
the same honesty the SDK's own documentation insists on: class existence and inheritance are CONFIRMED;
member offsets, function addresses, and singleton pointers are not yet tabulated and must never be
guessed.

**How this book uses it.** The split is clean and it is why Part VII reads the way it does:

- Naming a class, its namespace, and its ancestry → **✅**, cite the RTTI set.
- Saying a chunk id constructs an instance of such a class → **🟡** (the correspondence is reasoned from
  the class's role and the chunk's contents) unless a decode nails it.
- Stating the byte offset of a specific member, or the address of a handler → **⏳** until diffing or
  disassembly promotes it, with the source of that promotion stated.

**Why two evidence bases, kept separate.** Files and the executable are independent sources, and keeping
their claims distinct is what lets a reader trust each. A file claim is reproducible with the parser on
their own copy of the data; a class claim is reproducible by reading the RTTI of their own copy of the
`.exe`. Neither borrows the other's authority. When a chapter connects the two — "the `SetTopSpeedKmh`
value from the `.con` ends up in *this* member of the live `Vehicle`" — that bridge is exactly where a ⏳
sits until both ends are pinned.

**What happens if you bend it.** Treating an RTTI-confirmed class name as license to invent its members'
offsets is the tempting error — the class is real, so surely the offsets are "probably" thus. They are
not proven, and a wrong offset written as fact is the worst kind of error because the reader has no way to
see it is a guess. Name from RTTI; offset only from a diff or a disassembly you can cite.
