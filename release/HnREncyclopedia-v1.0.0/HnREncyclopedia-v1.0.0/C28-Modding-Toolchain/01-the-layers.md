# C28.1 — The Six Layers

**What it is.** The modding toolchain as a ladder: six layers of increasing power and difficulty, from
dropping a file to writing disassembly-guided native code. The skill is picking the *lowest* rung that does
what you need — deeper is more capable but more fragile.

**How it works.** Each layer reaches something the one above can't:

1. **Loose-file shadowing** (C3.6) — replace any *asset*. Drop a file in the loose tree and it wins over the
   packed version. No tools beyond a file manager. Covers: textures (C5), models (C7), sounds (C18), UI
   (C21), scripts (C14/C15). This is 90% of content modding.
2. **Mod folders** (`mod.json`, C28.2) — *package* loose-file mods so a launcher can manage them (enable,
   disable, order, share). A folder with a manifest and mirrored asset paths.
3. **Lucas' Mod Launcher + Lua** (C28.3) — add *scripted behaviour* and hooks the game exposes. Lua, no
   compilation. Covers gameplay tweaks that assets alone can't.
4. **ASI plugins / proxy DLLs** (C28.4) — inject *native code* into the process. C/C++ compiled to a DLL,
   loaded by an ASI loader or a proxy DLL. Covers anything in the running game.
5. **DonutsSDK** (C28.5) — native code with a *typed, verified* interface to the class set. C++20 over the
   RTTI class DB. Safer and clearer than raw ASI.
6. **Raw memory** (C4.3) — disassembly and direct memory edits. Unlimited, but you own every address.

**Why a ladder.** Each layer trades ease for power, and using a layer deeper than needed is a mistake:
raw-memory-poking a texture swap is absurd when a loose file does it; writing an ASI to change handling is
wasteful when a `.con` edit (C15) suffices. The right instinct is *always start at the top* — can a loose
file do it? a mod folder? — and only descend when the layer above genuinely can't reach. Most mods live in
layers 1–3 (assets and Lua); layers 4–6 are for behaviour the data doesn't expose.

**How the layers relate to the book.** Layers 1–2 are the *disk-side* chapters (Parts I–VI): every asset
format you decoded is something a loose file can replace. Layers 4–6 are the *runtime* chapters (Part VII):
reaching into live objects needs the class model (C23) and offset recovery (C4.3). The book's two halves —
formats and runtime — map onto the toolchain's two halves — assets and code. Understanding the formats lets
you mod at layers 1–3; understanding the runtime lets you mod at layers 4–6.

**Choosing a layer, by task.**

- *Change how something looks/sounds* → layer 1 (loose file): texture, model, sound, UI.
- *Change tuned values* → layer 1: `.con` handling (C15), mission scripts (C14/C16), UI XML (C21).
- *Change behaviour the scripts don't expose* → layer 3 (Lua) or 4–5 (native).
- *Read or tweak live game state* → layer 5 (DonutsSDK, typed) or 4/6 (raw).

**What happens if you bend it.**

- *Reach too deep* — you take on fragility (addresses shift per build, C28.6) for no benefit. Start high.
- *Reach too shallow* — some behaviour truly needs code (layers 4–6). Don't force an asset edit to do a
  code job.
- *Mix layers carelessly* — a loose-file mod and a native mod touching the same thing can conflict. Know
  which layer owns each change.
