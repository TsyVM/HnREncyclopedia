# C28.5 — DonutsSDK Native Mods

**What it is.** The top native layer: **DonutsSDK**, a C++20 SDK that wraps the raw injection of C28.4 in a
*typed, verified* interface to the game's class model. It's this book's companion — the same RTTI-verified
data set (C23) exposed as a modding library, so native mods build on confirmed facts, not guesses.

**How it works (✅ verified from the SDK).** A DonutsSDK mod is one include, one function, one macro. Verified
from `examples/hello_mod/hello_mod.cpp`:

```cpp
#include <donutsdk/mod.hpp>
using namespace donutsdk;

void hello_mod() {
    mod::Log log{"hello_mod.log"};
    const shar::Image& game = shar::process();        // the live shar.exe, rebased
    if (!game.valid()) { log.print("shar.exe not found\n"); return; }
    log.print("base: 0x%08X\n", (unsigned)game.base());

    // Query the RTTI-verified class DB (C23):
    log.print("Class DB: %zu classes, %zu relations.\n",
              shar::db::kClassCount, shar::db::kRelationCount);   // 1,207 / 3,924
    if (auto* v = shar::db::find_class("Vehicle")) log.print("found Vehicle\n");
}
DONUTSDK_MOD(hello_mod)
```

It builds as a **32-bit DLL** (retail `shar.exe` is x86) and is injected like any ASI (C28.4). The SDK gives
you: `shar::process()` (the rebased live image), the `shar::db` **class database** (the verified 1,207
classes, C23.6), vtable **identification** (`shar::identify`, C23.5), typed **views** over objects, and
**reversible byte patches** (RAII — revert on scope exit).

**Why typed and verified.** Raw ASI work (C28.4) means juggling addresses by hand — error-prone and unsafe.
DonutsSDK layers the book's discipline into the API: class *names and inheritance* are ✅ verified (from the
same `shar_dumps.csv` as C23), so `shar::db::find_class("Vehicle")` and `shar::identify(obj)` are backed by
the executable's own RTTI. What the SDK deliberately does **not** hand you is unverified data: member offsets,
function addresses, and singleton pointers are ⏳ (C23.1) — you supply an offset you found yourself
(`view.at<T>(offset)`), clearly marked as user-supplied. The SDK enforces the exact ✅-name/⏳-offset split
the whole book runs on.

**The safety features.** Two matter most. **`shar::identify`** (C23.5) lets a mod act only on objects of a
verified type — "for every live `Vehicle`, do X" — with the type check backed by RTTI, so you never act on
the wrong object. **Reversible patches** (`shar::nop`/`shar::patch`, RAII) save the original bytes and restore
them on scope exit, so an edit is automatically undone — the native equivalent of the reversible loose-file
mod (C28.2). Together they make native modding as safe as native modding gets: verified type checks, and
edits that undo themselves.

**Where it sits.** DonutsSDK is layer 5 (C28.1) — above raw memory (layer 6), below which there's nothing but
disassembly. Use it when you need *native, typed* access to the runtime classes (C23–C26) and Lua (C28.3)
can't reach. It's the bridge between the book's runtime knowledge and working native code: the classes it
exposes are the ones documented in Part VII, and the offsets you feed it are the ones you recover by the
book's diffing method (C4.3).

**What happens if you bend it.**

- *Feed the SDK an offset you didn't verify* — it's user-supplied and unverified; the SDK marks it so, and
  you must re-verify per build (C28.6). Don't treat it as a DB fact.
- *Build 64-bit* — retail `shar.exe` is x86; the mod must be a 32-bit DLL. Match the target.
- *Skip `shar::identify` and act on raw pointers* — you risk acting on the wrong object. Use the verified
  type check.
