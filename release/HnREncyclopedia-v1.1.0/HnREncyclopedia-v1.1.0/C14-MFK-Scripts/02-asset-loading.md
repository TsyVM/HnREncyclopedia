# C14.2 — Asset Loading

**What it is.** The commands that name every file a level or mission needs and pull them into memory.
`LoadP3DFile` is the single most-used command in the entire game — **1,013 calls** (✅ verified) — and the
loading family is how the abstract "level 1" becomes concrete Pure3D assets.

**The core commands.**

- **`LoadP3DFile("path"[, "group"])`** — load a Pure3D file (C1) into the resident set, optionally tagged
  with a memory/streaming group like `"GMA_LEVEL_OTHER"` (verified in `ss.mfk`). This is the workhorse:
  terrain, models, textures, HUD art, mission props — all arrive through it.
- **`LoadDisposableCar("path", "name", "usage")`** — load a vehicle (its `.p3d` model; its handling comes
  from the matching `.con`, C15) as a *disposable* instance, tagged by usage (`"AI"`, etc.). 128 calls.
  "Disposable" means it's expected to be spawned, used, and freed within the mission — traffic and
  mission cars, as opposed to the persistent player car.
- **`SetDynaLoadData(...)`** — declare dynamically-streamed data (154 calls); content loaded on demand as
  the player moves, rather than all at level start. The `frontend/dynaload/` tree (mission icons, etc.) is
  named through this path.

**How it works.** A level's `…l.mfk` and `level.mfk` run their `LoadP3DFile` calls at load time; the VFS
(C3.6) resolves each path — loose file or `.rcf` member — and the Pure3D loader (C1.8) builds the objects.
The resident set is the union of everything loaded and not yet freed. Missions add their own loads on top
of the level's, and disposable cars are spawned from their loaded models as needed.

**Why explicit, total loading.** SHAR does not auto-discover assets; every file is named in a script. That
is more verbose but entirely predictable — the resident set of any level is exactly the list of
`LoadP3DFile` calls that ran, which is why you can read a `…l.mfk` and know precisely what memory a level
uses. It also makes modding tractable: to add an asset you add a load line; to replace one you change a
path or shadow the file (C3.6). Nothing is hidden.

**The name goldmine.** Because every path is a literal string, the load files are the densest source of
real asset names in the game — 1,013 `LoadP3DFile` paths alone. Mining them (C2.4) recovers the human names
that the binary Pure3D references dropped to hashes. Want to know what `art\cars\skinn_v.p3d` is called?
The `LoadDisposableCar` line that loads it tells you: `"skinn_v"`.

**What happens if you bend it.**

- *Reference a path that doesn't exist* — the load fails and the asset is missing in-game (a car that
  won't spawn, a prop that isn't there). Verify the path resolves through the VFS.
- *Forget the memory group on a large asset* — it may load into the wrong budget and crowd out other
  content; copy the group argument the retail files use for similar assets.
- *Load an asset but never free it across missions* — you grow the resident set and risk running out of
  memory on constrained targets. Respect the level's load/unload phases (C14.1).
