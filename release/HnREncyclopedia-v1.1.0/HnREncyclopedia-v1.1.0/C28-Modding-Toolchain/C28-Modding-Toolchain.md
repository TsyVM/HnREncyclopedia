# Chapter 28 — The Modding Toolchain

> **Goal of this chapter:** map the practical ecosystem for changing the game — from dropping a loose file to
> writing native C++ — and the discipline that keeps mods safe and honest. This is where every earlier
> chapter's "you can mod this" becomes a concrete workflow.

The whole book has pointed at modding: edit a `.con` (C15), a `.pag` (C21), a texture (C5). This chapter
steps back and shows the **layers** of the SHAR modding toolchain, from the easiest (a loose file) to the
deepest (native code against the RTTI-verified class set), and the verification discipline that runs through
all of them. Everything here is grounded in the actual tooling shipped in the game folder — the `mods/`
structure, the `NoTrafficDiag.asi` plugin, the proxy DLLs, and the DonutsSDK example.

**Key finding (✅ verified):** the toolchain is a **ladder of six layers**, each reaching deeper: (1)
loose-file shadowing (C3.6), (2) mod folders (`mod.json`), (3) Lucas' Mod Launcher + Lua, (4) ASI plugins /
proxy-DLL injection, (5) the DonutsSDK native C++ layer, (6) raw memory work. The shipped `NoTrafficDiag`
mod demonstrates the professional discipline: **read-only, vtable-identified, re-verify-per-build**.

---

## Deep-dive pages

- [C28.1 — The Six Layers](01-the-layers.md): the modding ladder, easiest to deepest.
- [C28.2 — Loose Files & Mod Folders](02-loose-and-folders.md): shadowing (C3.6) and `mod.json`.
- [C28.3 — Lucas' Mod Launcher & Lua](03-mod-launcher.md): the community standard.
- [C28.4 — ASI Plugins & Injection](04-asi-injection.md): `NoTrafficDiag.asi`, proxy DLLs, the vtable watch.
- [C28.5 — DonutsSDK Native Mods](05-donutsdk.md): `#include <donutsdk/mod.hpp>`, the verified class DB.
- [C28.6 — Verification & Ethics](06-verification-ethics.md): re-verify per build, read-only, single-player.
- [C28.7 — SAHRDiag: the diagnostic tool](07-sahrdiag.md): static RTTI walk + live-object scan that verifies and extends this book and the DonutsSDK.

---

## 28.1 The six layers (✅ verified)

The toolchain is a ladder — pick the lowest rung that does the job:

| Layer | Reaches | Skill | Chapter |
|---|---|---|---|
| 1. Loose-file shadow | replace any asset | drop a file | C3.6 |
| 2. Mod folder (`mod.json`) | packaged asset mods | a folder + JSON | C28.2 |
| 3. Mod Launcher + Lua | scripted behaviour, hooks | Lua | C28.3 |
| 4. ASI / proxy DLL | native code injection | C/C++ + a loader | C28.4 |
| 5. DonutsSDK | typed, verified native access | C++20 | C28.5 |
| 6. Raw memory | anything | disassembly | C4.3 |

[C28.1](01-the-layers.md).

## 28.2 Loose files & mod folders (✅ verified)

The base mechanism is **loose-file shadowing** (C3.6): a loose file in the right path wins over a packed one,
so replacing an asset is dropping a file. **Mod folders** package this: verified `mods/99_Mods/` contains a
`mod.json` (`{"name":…, "version":"1.0.0", "author":"You"}`) and shadowing assets mirroring the game paths
(`art/chars/homer_m.p3d`, `homer.cho`). [C28.2](02-loose-and-folders.md).

## 28.3 Lucas' Mod Launcher & Lua (✅ context)

The community standard is **Lucas' Simpsons Hit & Run Mod Launcher** (Donut Team) — it manages mods, applies
loose-file overrides, and adds a **Lua** scripting layer with hooks into the game. Most content mods target
it. [C28.3](03-mod-launcher.md).

## 28.4 ASI plugins & injection (✅ verified)

Native mods load as **ASI plugins** (DLLs an ASI loader injects) or via **proxy DLLs** (a fake `d3d9.dll`/
`winmm.dll` the game loads, which loads your code). The game folder ships exactly this: `NoTrafficDiag.asi`
and `mods/d3d9.dll`. `NoTrafficDiag`'s log shows it identifying live objects by **vtable** (C23.5) —
`TrafficVehicle` @ `0x00607948`, `RoadManager` @ `0x0060B6D0` — **read-only**. [C28.4](04-asi-injection.md).

## 28.5 DonutsSDK native mods (✅ verified)

The **DonutsSDK** is the typed, verified native layer: `#include <donutsdk/mod.hpp>`, a `void` function, the
`DONUTSDK_MOD(fn)` macro. Verified from `examples/hello_mod/hello_mod.cpp` — it queries the RTTI class DB
(`shar::db::find_class("Vehicle")`), rebases to the live process, and is read-only by default. It builds as a
32-bit DLL injected like any ASI. [C28.5](05-donutsdk.md).

## 28.6 Verification & ethics (✅ verified discipline)

The professional discipline, demonstrated by the shipped mods: **re-verify addresses against your own exe**
(the `NoTrafficDiag` log says so explicitly), prefer **read-only** and **reversible** edits, and keep to
**single-player** (no online cheating). [C28.6](06-verification-ethics.md).

---

## Key takeaways

- The toolchain is a **six-layer ladder** — use the lowest rung that works: loose file → mod folder → Lua →
  ASI/proxy DLL → DonutsSDK → raw memory.
- **Loose-file shadowing** (C3.6) is the base; **mod folders** (`mod.json` + mirrored paths) package it —
  both verified in the shipped `mods/`.
- **Lucas' Mod Launcher** (Donut Team) is the community standard, with a **Lua** hook layer.
- Native mods inject as **ASI/proxy DLLs**; the shipped `NoTrafficDiag.asi` shows the model —
  **vtable-identified, read-only** (verified VAs in its log).
- **DonutsSDK** is the typed layer over the **RTTI-verified class DB** (`DONUTSDK_MOD`, `shar::db`).
- The discipline: **re-verify per build, read-only/reversible, single-player**.

**Next:** [Chapter 6 — Shaders & Materials](../C6-Shaders-Materials/C6-Shaders-Materials.md), or the [chapter map](../README.md#chapters).
