# C28.3 — Lucas' Mod Launcher & Lua

**What it is.** The community-standard tool for SHAR modding — **Lucas' Simpsons Hit & Run Mod Launcher**, by
Donut Team — which manages mod folders (C28.2), applies overrides, and adds a **Lua** scripting layer with
hooks into the game. Most published SHAR mods target it.

**How it works (🟡 — community tool, not shipped in this data set).** The Mod Launcher sits between the mods
and the game: it reads mod folders (their `mod.json` manifests, C28.2), lets the user enable/disable and
order them, and at launch applies their loose-file overrides (C28.2/C3.6) — often via a virtual overlay so
the game's real files are never modified. On top of asset overriding, it exposes a **Lua** API: a mod can
ship Lua scripts that run in the game and call into launcher-provided hooks — changing gameplay values,
reacting to events, adding logic that assets alone can't express.

**Why Lua.** Lua is the standard game-scripting language — small, embeddable, easy to author — and it lets
modders add *behaviour* without a C++ toolchain or injection (C28.4). A Lua mod can do things a data mod
can't: change a value conditionally, respond to a game event, script a new interaction. It's the middle
ground of the ladder (layer 3, C28.1) — more than assets, less than native code — and it's where most
*behavioural* (as opposed to *cosmetic*) SHAR mods live.

**The relationship to this book.** The Mod Launcher is the *delivery vehicle* for the disk-side modding the
book documents: you decode a format (C5–C22), make your change, package it as a mod folder (C28.2), and the
launcher applies it. The book explains *what* the files are and *how* to change them safely; the launcher is
*how you ship and load* those changes. For the Lua layer, the book's runtime chapters (C23–C26) explain the
systems the Lua hooks touch — a Lua mod that changes handling is reaching the same `Vehicle` (C24) a
DonutsSDK mod would, through the launcher's hooks instead of native code.

**Where DonutsSDK fits alongside it.** The Mod Launcher (Lua) and DonutsSDK (C++, C28.5) are complementary,
not competing: Lua is for scripted content and gameplay logic through the launcher's hooks; DonutsSDK is for
native code that reaches directly into the RTTI-verified class model (C23) when Lua's hooks don't go deep
enough. A modder uses the launcher for content and Lua, and drops to DonutsSDK for native work — the SDK's
own docs frame it this way (it "fills the gap" the launcher's Lua doesn't cover).

**What happens if you bend it.**

- *Assume launcher internals from this book* — the launcher is a community tool not shipped in this data set;
  its exact Lua API is its own documentation (🟡). The book covers the *game* it mods, not the launcher's
  internals.
- *Ship a data mod as raw loose files instead of a mod folder* — it works (C3.6) but isn't manageable. Package
  it (C28.2) so the launcher can handle it.
- *Reach for native code when Lua suffices* — many behavioural mods are fine in Lua (layer 3). Descend to
  native (C28.4/C28.5) only when needed.
