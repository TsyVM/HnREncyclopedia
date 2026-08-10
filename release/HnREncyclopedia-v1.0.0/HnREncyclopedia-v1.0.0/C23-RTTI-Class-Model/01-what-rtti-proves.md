# C23.1 — What RTTI Proves (and What It Doesn't)

**What it is.** The evidence base for the entire runtime half of this book, and the precise line between
what it establishes as fact and what remains open. Getting this line right is what makes the runtime
chapters trustworthy.

**How it works.** MSVC (which built the retail PC `Simpsons.exe`) emits, for every polymorphic class, a
`_RTTITypeDescriptor` (the class's decorated name) and `_RTTIBaseClassDescriptor` records (its base classes
and the byte offset of each base sub-object within the derived class). This metadata is compiled *into the
shipped binary* so `dynamic_cast` and exception handling can work. It is not a leak or a guess — it is the
program's own description of its types, and it can be read straight out of the `.exe`. DonutsSDK's
`data/shar_dumps.csv` is that read: **1,207 classes, 3,924 relations**, every row `CONFIRMED`.

**What it proves (✅).**

- **Class existence and exact names** — `Vehicle`, `sim::SimState`, `CharacterAi::Loco`, `SuperCam`,
  `IEntityDSG`, namespaced exactly as the engine names them.
- **Inheritance** — which classes derive from which, e.g. `Vehicle : DynaPhysDSG, StaticPhysDSG,
  CollisionEntityDSG, IEntityDSG` — and the **byte offset of each base sub-object** within the derived
  class (RTTI records these explicitly). So `sim::SimState`'s `tRefCounted` sub-object at offset 0 is a
  fact, not an inference.

**What it does NOT prove (⏳).**

- **Arbitrary member offsets** — the byte where `Vehicle` stores its top-speed float, or `SuperCam` its
  target. RTTI describes the *type lattice*, not the full layout of non-base data members.
- **Method / function addresses** — where a class's methods or the chunk handlers live in the binary.
- **Singleton / manager pointers** — the address of `VehicleCentral`, `CharacterManager`, etc.

Those are recovered by *other* means — disassembly, and the hex/memory diffing of C4.3.

**Update — member offsets partially recovered (✅ 1,917).** A later pass did this recovery statically:
`DonutsSDK/tools/extract_member_offsets.py` walks every class's vtable (the 965 verified addresses, C23.5)
and disassembles the virtual accessor methods, extracting **1,917 verified member offsets across 694 of the
1,207 classes** (`data/member_offsets.csv`). **333 are named** base-subobject offsets from RTTI (e.g.
`sim::PhysicsProperties::SimUnits @ 0x10`); the other **1,584 are offset-only** — a getter compiled to
`mov eax,[ecx+0x74];ret` proves a member exists *at 0x74* but not its *name* (name it by combining with a
behavioural diff, C4.3). So member offsets are no longer wholly ⏳: a majority of classes now have verified
offsets, names still to be attached. Function addresses and singleton pointers remain ⏳. The rule stands —
never *guess* an offset — but many are now *recovered*, not guessed.

**Why the discipline matters.** A single confidently-wrong offset written as fact would poison every mod
built on it, and the reader would have no way to see it was a guess. So the rule is absolute: **name from
RTTI (✅); offset only from a diff or disassembly you can cite (⏳ until then).** Every runtime chapter that
follows obeys it — you will see many verified class names and inheritance chains, and every specific field
offset marked open.

**What happens if you bend it.**

- *Treat a confirmed class name as license to invent its members* — the class is real, but its offsets are
  not proven. Diff for them (C4.3).
- *Assume a class from the original data set is in your exe* — 36 classes differed between builds (see the
  SDK CHANGELOG); re-verify against your own binary if you depend on one.
- *Confuse a base sub-object offset (proven) with a data-member offset (open)* — RTTI gives the former, not
  the latter. Read the CSV's offset column carefully.
