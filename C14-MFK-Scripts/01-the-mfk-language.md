# C14.1 — The MFK Language & File Roles

**What it is.** The grammar of `.mfk` and the naming convention that tells you what each file does before
you open it. MFK is the same surface language as `.con` (Chapter 15) — `Name(args);` statements and `//`
comments — scaled up to 172 commands and organised into files by role.

**How the language works.** Statements execute top to bottom. Arguments are strings (asset paths, object
and mission names), integers (indices, flags), and floats (positions, times). There is no user-defined
control flow, but there *is* structure by convention: many commands come in **open/close pairs** that
bracket a block — `AddStage`/`CloseStage`, `AddObjective`/`CloseObjective`, `AddCondition`/`CloseCondition`,
`CreatePedGroup`/`ClosePedGroup`, `GagBegin`/`GagEnd`. The engine maintains an implicit "current" context
(the stage you're building, the gag you're defining) and the setters in between apply to it. That the
open and close counts match *exactly* across the whole tree (670/670, 671/671-class, 419/419 — ✅ verified)
is proof the blocks are always balanced, and a validity check for any file you edit.

**The file-role convention.** The `scripts/` tree encodes each file's job in its name:

- **`ss.mfk` / `ssi.mfk`** — the top-level session setup (loads global assets, wires the front-end).
- **`level.mfk` / `leveli.mfk`** (per level dir) — level setup: the world, ambient population, traffic
  budget.
- **`m{N}l.mfk`** — mission N **load** file: the asset manifest (`LoadP3DFile`/`LoadDisposableCar`).
- **`m{N}i.mfk`** — mission N **instructions**: `SelectMission` then the stage/objective logic.
- **`m{N}sd{i,l}.mfk`** — the mission's **showdown** (finale) load/logic.
- **`bm…`, `gr…`, `sr…`, `d…`** — bonus, street-race, sub-race, and other mission-type prefixes
  (verified filenames in `scripts/missions/level01`).

**Why it's built this way.** Separating *loading* from *logic* (the `l`/`i` split) lets the engine load a
mission's heavy assets in one phase and run its lightweight script logic in another, and lets designers
iterate on mission flow without touching the asset list. Encoding the role in the filename means the level
loader can find the right file by pattern (`m` + index + role) rather than a manifest — the naming *is* the
index. This is the same "convention over configuration" instinct that makes the whole scripts tree
navigable without a table of contents.

**Reading a tree at a glance.** `scripts/missions/level01/` holds `m0…`–`m7…` (the seven story missions
plus a tutorial `m0`), `bm1` (a bonus mission), `gr1` (a street race), `sr…` (sub-races), and `d1` — each
in `i` and `l` variants, some with `sd`. From filenames alone you can reconstruct the level's mission
roster before reading a line of script.

**What happens if you bend it.**

- *Unbalance an open/close pair* — leave out a `CloseStage()` and every following stage folds into the
  current one, or the parser desyncs. The balanced-count invariant is real; keep pairs matched.
- *Misname a mission file* — the loader finds files by their role pattern, so a renamed `m3i.mfk` may
  simply not be found and the mission won't run. Keep the `m{N}{role}` convention.
- *Put logic in an `l` file or loads in an `i` file* — it may work, but you break the phase separation the
  engine expects and make the mission harder to maintain. Keep loads in `…l`, logic in `…i`.
