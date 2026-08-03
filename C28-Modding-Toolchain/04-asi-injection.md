# C28.4 — ASI Plugins & Injection

**What it is.** The layer where mods become *native code running inside the game process* — loaded as ASI
plugins or through proxy DLLs. This is how a mod reaches the live objects the runtime chapters (C23–C26)
describe. The game folder ships real examples.

**How it works (✅ verified tooling).** Two injection mechanisms, both present in the game directory:

- **ASI plugins.** An `.asi` file is just a DLL with a different extension, loaded by an **ASI loader** (a
  small runtime that scans for `.asi` files at startup and `LoadLibrary`s them). Verified:
  **`NoTrafficDiag.asi`** ships in the game folder (with its `.log` and `.started` files). Once loaded, the
  plugin's code runs in the game's address space and can read/patch memory.
- **Proxy DLLs.** The game loads certain system DLLs by name (`d3d9.dll`, `winmm.dll`); replacing one with a
  **proxy** — a DLL that forwards the real functions *and* runs your code — injects without a separate loader.
  Verified: **`mods/d3d9.dll`** is exactly this (a D3D9 proxy; note the game itself renders on D3D8 via
  `pddidx8r.dll`, so a `d3d9.dll` here is a modding hook, not the renderer).

**A verified example — the `NoTrafficDiag` vtable watch.** `NoTrafficDiag.asi`'s log is a masterclass in
careful native modding, and it demonstrates the runtime chapters in action:

```
[NoTrafficDiag] shar.exe base: 0x00400000
  - PathManager      preferred=0x006072A8  live=0x006072A8
  - TrafficVehicle   preferred=0x00607948  live=0x00607948
  - RoadManager      preferred=0x0060B6D0  live=0x0060B6D0
[NoTrafficDiag] Read-only vtable watch. This build never writes to game memory…
[NEW]  RoadManager      @ 0x004BCB44   bytes: D0 B6 60 00 …   (vtable ptr 0x0060B6D0)
[NEW]  TrafficVehicle   @ 0x004FF7A8
```

It works by **vtable identification** (C23.5): it knows the vtable addresses of `TrafficVehicle`,
`RoadManager`, `PathManager`, and scans memory for objects whose first pointer matches — each match is a live
instance of that class. Note the first bytes of a found `RoadManager` are `D0 B6 60 00` = `0x0060B6D0`, its
vtable — exactly the identification mechanism (C23.5). This is the ⏳→✅ offset/address recovery the book
describes, done for real.

**Why this is the model to follow.** `NoTrafficDiag` is **read-only** — it *watches* traffic objects to
diagnose them, never writing to game memory or calling game code. That's the safest possible native mod: it
can't crash or corrupt the game because it only reads. And its log explicitly warns *"Re-verify these VAs
against your own exe"* — the exact per-build discipline (C28.6). It's a native mod done right: identify by
vtable (verified mechanism), read before you write, and never trust an address across builds.

**The tie to the runtime chapters.** Everything `NoTrafficDiag` does rests on the class model: `TrafficVehicle`
(C24.3), `RoadManager`/`PathManager` (the road network runtime, C13.5) are RTTI-verified classes (✅ names);
their vtable addresses are the ⏳ part it recovered by disassembly. A native mod is applied C23 (identify by
vtable) + C4.3 (recover offsets) — this page is where those techniques become a working plugin.

**What happens if you bend it.**

- *Write to memory before reading/verifying* — a wrong address corrupts the game. Follow `NoTrafficDiag`:
  read-only first, verify, then (if ever) write.
- *Hardcode vtable/member addresses across builds* — they shift. Re-verify per exe (C28.6).
- *Use a proxy DLL that doesn't forward the real functions* — you break the system the game needed. A proxy
  must forward *and* add.
