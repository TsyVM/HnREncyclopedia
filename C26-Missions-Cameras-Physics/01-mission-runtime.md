# C26.1 — The `Mission` Runtime Family

**What it is.** The runtime of everything Chapter 16 decoded from scripts — the `Mission` object that runs a
mission, and the objective/condition objects that make up its stages. This is where the mission *data*
becomes a live, ticking state machine.

**How it works (✅ verified).** From `shar_dumps.csv`:

```
Mission : EventListener
MissionObjective : EventListener            (21 subclasses)
MissionCondition                            (13 subclasses)
BonusMissionInfo : HasPresentationInfo, EventListener
HudMissionObjective : HudEventHandler       — the on-screen objective (SetHUDIcon, C14.6)
HudMissionProgress  : HudEventHandler       — the progress display
```

A `Mission` is an **`EventListener`** (C23.3) — the key to how the mission state machine (C16.2) runs. Rather
than polling, the mission *listens* for the game events that satisfy or fail its current stage: "player
reached location," "vehicle destroyed," "timer expired." When an event matching the active objective arrives,
the stage advances; when one matching a condition arrives, the stage fails. So the balanced `AddStage…
CloseStage` script (C16.2) builds a chain of event-listening objects, and the game's event stream drives them.

**Why event-driven.** A mission could be written as a per-frame poll ("is the player at the target yet?"),
but that's wasteful and tangled. Making missions `EventListener`s means each objective registers interest in
exactly the events it cares about and sleeps otherwise — efficient, and cleanly decoupled from the systems
that emit the events (the vehicle emits "destroyed," the mission listens). This is why 117 classes derive from
`EventListener` (C23.3): the whole runtime communicates by events, and missions are prime consumers. It's also
why the mission *scripts* can be pure data (C16) — the script declares which objectives/conditions to create,
and the event system wires them to the game automatically.

**The HUD tie.** `HudMissionObjective` and `HudMissionProgress` are `HudEventHandler`s — they listen for the
same mission events and update the on-screen objective text and progress. So `SetHUDIcon`/
`SetStageMessageIndex` (C14.6/C16.2) feed these HUD listeners, and the player sees the mission state change
because the HUD objects react to the same events the mission does. Mission logic and mission display are two
sets of listeners on one event stream.

**What happens if you bend it.**

- *Expect a mission to poll* — it's event-driven; if an objective never gets its event, the stage hangs
  (C16.2). Ensure the events an objective needs are actually emitted.
- *Rely on a `Mission` member offset* — the classes are ✅, offsets ⏳. Diff (C4.3).
- *Edit HUD display expecting mission logic to change* — the HUD listeners and the mission listeners are
  separate; changing one doesn't change the other.
