# C28.2 — Loose Files & Mod Folders

**What it is.** The two lowest, most-used layers: **loose-file shadowing** (the mechanism) and **mod
folders** (the packaging). Together they are how nearly all SHAR content mods work, and they need no tools
beyond a file manager and a text/image editor.

**Loose-file shadowing (✅ verified mechanism).** The VFS (C3.6) resolves an asset path against its mounted
sources, and a loose file can **shadow** a packed one when the loose tree is consulted first. So to replace
any asset, you place a file at the path the game requests: `art\cars\ambul.p3d` loose overrides the packed
one; a loose `.con` overrides the packed handling. This is the base of everything — the packed archives (C3)
never need touching, because a loose file wins. Every disk format in the book (C5–C22) is moddable this way.

**Mod folders (✅ verified structure).** To make loose-file mods *manageable* — shareable, toggleable,
ordered — they're packaged as **mod folders**. Verified from the shipped `mods/99_Mods/`:

```
mods/99_Mods/
  mod.json                     {"name":…, "version":"1.0.0", "author":"You"}
  art/chars/homer_m.p3d        shadowing assets, mirroring the game's paths
  art/chars/homer_a.p3d
  art/chars/homer.cho
```

A mod folder is a **manifest** (`mod.json` — name, version, author) plus the assets it overrides, laid out in
the *same directory structure* as the game (`art/chars/…`). A launcher (C28.3) reads the manifest, and when
the mod is enabled, its files shadow the game's. The `99_` prefix is **load order** — higher numbers apply
later, so `99_` mods win conflicts. This is the Donut Team mod format.

**Why mirror the game's paths.** Laying a mod's files out exactly like the game's means the launcher can
apply them by simple path overlay — mod file at `art/chars/homer_m.p3d` shadows game file at the same path.
No mapping table, no rules: the path *is* the target. This is the same "path is the key" idea as the VFS
(C3.6) and RCF hashing (C3.3), applied to mods. It also makes a mod self-documenting — you can see exactly
what it changes by listing its files.

**What a mod folder can change.** Anything that's an asset: a character's model + `.cho` (C8), a car's model
+ `.con` (C7/C15), a texture (C5), a UI page (C21), a sound (C18), a mission script (C14/C16). The
`99_Mods` example replaces Homer's model and choreography — a character reskin/re-rig. Because it's all
loose-file shadowing underneath, a mod folder is as safe as editing loose files: reversible (disable the
mod), non-destructive (the packed originals are untouched).

**What happens if you bend it.**

- *Mislay a mod file's path* — if it doesn't mirror the game path, it shadows nothing. Match the structure
  exactly.
- *Ignore load order* — two mods changing the same file conflict; the higher-ordered wins. Use the numeric
  prefix deliberately.
- *Shadow a packed file the VFS consults after the archive* — confirm the loose-wins precedence for that
  asset class (C3.6); repack if needed.
