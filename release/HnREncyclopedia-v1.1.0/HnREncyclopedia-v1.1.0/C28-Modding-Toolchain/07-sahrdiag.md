# C28.7 — SAHRDiag: the diagnostic tool

> **Where this book comes from.** Almost every "✅ verified" in these chapters
> traces back to two evidence bases: parsed asset files, and a walk of the retail
> `Simpsons.exe`. **SAHRDiag** is the tool that performs the second walk — and,
> crucially, it re-performs it on demand so the book and the DonutsSDK can be
> *proven*, not merely trusted.

SAHRDiag lives at the top level of the project (`SAHRDiag/`). It is the SHAR
analogue of the analysis tool used for other Radical/Pure3D-era reversing work:
a **static + dynamic** inspector for `Simpsons.exe` that needs no IDA, x64dbg, or
Ghidra. It is strictly **read-only** — it observes the game, never edits it.

## Two modes

**Static** (no game running). The host rebuilds `Simpsons.exe`'s section-mapped
image and walks MSVC RTTI: every polymorphic class carries a *TypeDescriptor* and
a *Complete Object Locator* (COL), and the COL chain resolves **class name →
vtable → virtual methods**. Because SHAR ships full RTTI, this recovers the entire
object model deterministically. This is the exact walk behind Chapter 23's class
model and the DonutsSDK's verified vtable set.

**Dynamic** (game running). `SAHRDiag.dll` is injected, waits for the world to
load, then runs the **live-object scan**: it reads committed heap memory, matches
each object's first dword against the confirmed `{class → vtable}` catalogue, and
dumps the object's leading bytes. A live C++ object's first dword *is* its vtable
pointer, so a match positively identifies the object's class — and its bytes are
the raw evidence for confirming **member offsets** at runtime. This generalizes
the shipped `NoTrafficDiag` plugin (C28.4), which proved the technique on traffic
vehicles (`TrafficVehicle` @ vtable `0x00607948`, spotted by its first dword
`48 79 60 00`), to **all** catalogued classes.

## What it did for this book and the SDK (✅ verified)

Run against retail `Simpsons.exe` (MD5 `b3a47b881eec97745424b1e2c86cdcaf`):

| Result | Value |
|---|---|
| TypeDescriptors recovered | 1,327 |
| Complete Object Locators | 2,116 |
| Linked vtables | 1,228 |
| DonutsSDK's 965 confirmed vtables reproduced | **965 / 965 (100%), 0 conflicts** |
| Clean new classes surfaced (not previously catalogued) | **166** |

The 100% reproduction is the point: the central claim these chapters rest on —
that the class/vtable data is real and recoverable — is now *self-checking*. And
the 166 new classes (`EngineState`, `EventListener`, `ForceEffect`, `GuiMenuItem`,
`HudMapCam`, `ICameraShaker`, `ICarSoundParameters`, `ILaneControl`,
`BonusObjective`, `Card`, `CGuiEntity`…) were promoted into the SDK catalogue,
taking it from 965 to **1,131** confirmed vtables.

## How a modder uses it

1. **Verify a build.** Point the Python path at your own copy —
   `python3 SAHRDiag/static/sahrdiag.py "<game>" "<DonutsSDK>"` — and it re-derives
   the vtable catalogue and reports any drift from your exe. Addresses are
   build-specific; this is how you re-verify them (C28.6).
2. **Find an object's real layout.** Run the live-object scan while the thing you
   care about is on screen (a specific vehicle, a HUD element), then read the byte
   dump against `member_offsets.csv` to locate the field you want.
3. **Graduate to interception.** The optional **VTRACE** overlay
   (`SAHRDIAG_VTRACE.md`) turns the static vtable list into a live
   trigger→method→effect trace using the same VanHooks mechanism the DonutsSDK's
   `vanhooks_mod` example uses — the bridge from *observing* to *hooking*.

## What a live run proved (✅ verified)

A real dynamic capture — `SAHRDiag.dll` injected into a running `Simpsons.exe`,
dumping **20,000 live objects** across **1,228 vtables** — turned theory into
measured fact:

- **The method is sound.** Every one of the 20,000 objects (100%) began with the
  exact vtable pointer it was matched on. That is independent runtime proof of the
  identification technique *and* the vtable catalogue Chapter 23 rests on.
- **Object sizes fell out for free.** Pool-allocated classes sit contiguously, so
  the stride at which a vtable repeats is the object's size: `tTexture` = 0x20,
  `daSoundResourceData` = 0x14, `Blinker` = 0x18, `radObjectListNode` = 0x18,
  `CollectorCard` = 0x30, and 11 more.
- **Composition became visible.** A different class's vtable at a stable offset is
  a member subobject there — several at 100% support: `tSkeleton +0x10` holds its
  joint array, `tBillboardQuadGroup +0x18` its quad array, `tCompositeDrawable
  +0x34` its element array, and `tTexture ↔ tShader` cross-link at +0x20.

These promoted straight into the DonutsSDK (`data/runtime_object_sizes.csv`,
`data/runtime_composition.csv`); the full write-up is `SAHRDiag/reports/RUNTIME_FINDINGS.md`.

## Discipline

SAHRDiag embodies the same ethics as the rest of this chapter: **read-only,
vtable-identified, re-verify per build, single-player**. It never writes game
memory; it is an inspection and documentation tool for a game you own. It is the
reason this encyclopedia can end most claims with a checkmark instead of a shrug.
