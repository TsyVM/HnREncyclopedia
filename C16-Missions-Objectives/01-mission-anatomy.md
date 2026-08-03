# C16.1 — Mission File Anatomy & the Roster

**What it is.** How a single mission is split across files, and how the level's roster ties them together.
Every mission is three things — an asset list, a logic script, and (for finales) a showdown — named by a
convention you can read at a glance.

**How it works (✅ verified).** A mission `m{N}` is authored as:

- **`m{N}l.mfk`** — the **load** file: `LoadP3DFile`/`LoadDisposableCar` for every prop, character, and car
  the mission needs (C14.2).
- **`m{N}i.mfk`** — the **instructions** file: `SelectMission("m{N}")`, then the stage/objective logic (C16.2).
- **`m{N}sdi.mfk` / `m{N}sdl.mfk`** — the **showdown** logic/load, for missions with a boss finale (C16.5).

The level's `level.mfk` (C12.4) declares the roster. Verified across levels, the shape is consistent:

```
Level 1: AddMission("m0")…("m7")   + sr1,sr2,sr3,gr1,bm1
Level 2: AddMission("m1")…("m8")   + sr1,sr2,sr3,gr1,bm1
Level 3: AddMission("m1")…("m7")   + sr1,sr2,sr3,gr1,bm1, ismovie
```

So every level runs **7–8 story missions plus 5 bonus missions**, with the occasional level-specific extra
(Level 3's `ismovie`, the Itchy & Scratchy movie). Level 1 uniquely starts at `m0` (a tutorial mission).

**Why split a mission across files.** The load/logic split (C14.1) lets the heavy asset list load in one
phase and the lightweight logic run in another, and lets a designer iterate mission *flow* without touching
its *asset list*. Separating the showdown means a mission's normal run and its boss finale are independent
scripts — the finale can be rebalanced without disturbing the mission that leads to it. The naming
convention (`m` + number + role) means the engine finds each file by pattern, so the level roster is just a
list of mission *names*; the files follow from the name.

**Reading a level's structure.** From `level.mfk`'s `AddMission`/`AddBonusMission` lines alone you have the
whole level plan: which story missions, which races, which bonus. Then each `m{N}i.mfk` gives that mission's
stages. This top-down readability — roster in the level script, detail in the mission scripts — is how you
navigate an unfamiliar level's gameplay without running it.

**What happens if you bend it.**

- *Author a mission file but omit its `AddMission` line* — the mission exists on disk but the level never
  offers it (C12.4). List it in the roster.
- *Break the `m{N}{role}` naming* — the engine can't find the mission's parts by pattern. Keep the
  convention.
- *Put load calls in the `i` file or logic in the `l` file* — it may run, but you break the phase separation
  and make the mission harder to maintain. Keep loads in `…l`, logic in `…i`.
