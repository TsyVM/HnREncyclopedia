# C14.3 — Missions: Stages, Objectives & Conditions

**What it is.** The heart of the game's scripting: how a mission is expressed as a sequence of **stages**,
each with an **objective** to accomplish and **conditions** that pass or fail it. This structure is read
directly from shipped mission logic (`bm1i.mfk`, ✅ verified).

**The structure.** A mission logic file opens by selecting the mission, then lists stage blocks:

```c
SelectMission("bm1");            // name this mission (154 CloseMission pair it)

AddStage(0);                      // begin a stage; the int is a stage-type/flags value
  SetStageMessageIndex(12);       // localized instruction text id (C22)
  AddObjective("getin");          // the goal: get in the car
CloseStage();

AddStage(16);
  SetStageMessageIndex(145);
  AddObjective("delivery");        // deliver something
  AddCondition("timeout");         // fail if time runs out
CloseStage();
```

**The verbs, with verified counts.**

- **`SelectMission("name")` / `CloseMission()`** (154 each) — bracket the whole mission.
- **`AddStage(flags)` / `CloseStage()`** (670 each — perfectly balanced) — bracket one stage. The integer
  is a stage type/flags value (`0`, `16`, … observed).
- **`AddObjective("type")`** (671) — the stage's goal. Verified types include `getin`, `delivery`, `goto`
  — a small vocabulary of objective kinds the engine knows how to run.
- **`AddCondition("type")` / `CloseCondition()`** (435 each) — pass/fail conditions; `timeout` is the most
  common. Conditions can carry parameters via `SetCond…` setters (`SetCondTime` 100, `SetCondMinHealth`
  113, `SetCondTargetVehicle` 136).
- **`SetStageMessageIndex(n)`** (495) — the localized text shown for the stage (resolved via the string
  tables, C22).
- **`AddStageTime(s)`** (74), **`AddStageWaypoint`** (442), **`AddStageVehicle`** (177) — per-stage timers,
  route points, and vehicles.

**Why it's built this way.** A mission-as-stage-list is a tiny state machine: the engine runs the current
stage until its objective is met or a condition fails, then advances. Expressing that as balanced
`AddStage…CloseStage` blocks gives designers a readable, linear script with no explicit state-machine
wiring — the *order* of the blocks is the flow. The separate condition system means "how you fail" is
decoupled from "what you do," so the same objective (`delivery`) can have a timeout in one stage and not in
another. This is the classic data-driven mission design that lets non-programmers author gameplay.

**Mapping to runtime (✅ names / ⏳ offsets).** These verbs build the RTTI-confirmed `Mission`,
`MissionStage`, and `MissionObjective` class family (45 classes, C26). The class names and the
objective/condition *types* are verified; the exact per-object memory layout is ⏳ and recovered
separately.

**What happens if you bend it.**

- *Add an objective type the engine doesn't know* — an unrecognised `AddObjective("…")` string has no
  runner and the stage can't complete. Use the verified objective vocabulary.
- *Leave a stage without a completion path* — no reachable objective/condition and the mission hangs on
  that stage. Every stage needs a way forward.
- *Unbalance `AddStage`/`CloseStage`* — folds stages together or desyncs the parse (C14.1). Keep them
  matched; the 670/670 count is the invariant.
