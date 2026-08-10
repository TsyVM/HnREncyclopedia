# C16.2 — Stages: the Mission State Machine

**What it is.** The engine that runs a mission: a linear sequence of **stages**, each an objective to meet
under some conditions, advanced one at a time until the mission is won or failed. It is a small,
data-defined state machine.

**How it works (✅ verified).** A stage is a balanced `AddStage…CloseStage` block. Verified from a real
mission (`bm1i.mfk`, C14.3), with the full setter set:

```
AddStage(flags);                     // flags: stage type (0, 1, 16, … observed)
  SetStageMessageIndex(145);         // localized instruction text (C22)
  AddObjective("delivery");          // the goal (C16.3)
  AddStageVehicle(…);                // a vehicle this stage needs
  AddStageWaypoint(…);               // route points (on paths/road graph, C13)
  AddStageTime(0);                   // a timer for the stage
  AddCondition("timeout");           // a failure condition (C16.4)
CloseStage();
```

The engine runs the current stage: it shows the message, activates the objective, and watches the
conditions. When the objective is met it advances to the next stage; if a condition fails, the mission
fails. The stages run **in file order** — there is no branching in the common case, so the *sequence of
blocks is the mission's flow*. The perfectly balanced `AddStage`/`CloseStage` counts across the game
(670/670, C14.3) confirm every stage is well-formed.

**The `AddStage` flags.** The integer argument is a stage type/flags value (`0`, `1`, `16` observed). It
governs stage behaviour — whether the player must be in a car, whether it's a cutscene stage, and so on
(🟡 — the exact bit meanings are partially decoded; the values are verified). A designer picks the flag that
matches the stage's kind.

**Why a linear state machine.** Most SHAR missions are a *sequence*: go here, talk to them, drive there,
deliver this. A linear stage list expresses that directly — no explicit state wiring, just an ordered list
of "do this, then this." It keeps missions readable (you can follow one top to bottom) and authorable by
designers rather than programmers. Branching, where needed, is handled by conditions (C16.4) that fail a
stage, and by separate showdown files (C16.5), rather than by control flow in the script.

**Stage support commands.** Around the objective and conditions, a stage pulls in what it needs:
`AddStageVehicle` spawns a mission car (from a `LoadDisposableCar`, C14.2, tuned by a `.con`, C15);
`AddStageWaypoint` places route points on the path/road data (C13); `SetStageMessageIndex` binds the HUD
instruction (C22). A stage is thus the meeting point of objectives, world data, and presentation.

**What happens if you bend it.**

- *Leave a stage with no reachable objective/condition* — the mission hangs there forever. Every stage needs
  a way to advance or fail.
- *Unbalance `AddStage`/`CloseStage`* — stages fold together or the parse desyncs (C14.1). Keep them matched.
- *Use the wrong `AddStage` flag* — the stage may demand the player be in/out of a car unexpectedly. Match
  the flag to the stage's kind.
