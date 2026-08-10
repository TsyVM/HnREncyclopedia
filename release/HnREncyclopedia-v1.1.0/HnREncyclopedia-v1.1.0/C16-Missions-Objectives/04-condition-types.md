# C16.4 — The 7 Condition Types

**What it is.** The closed vocabulary of how a stage can *fail* (or, sometimes, additionally succeed).
Where objectives (C16.3) define what to *do*, conditions define what must stay true — or must not happen —
while you do it. Every `AddCondition("type")` in the game uses one of **7** types.

**The full set (✅ verified counts).**

| Condition | Uses | Fails the stage when… |
|---|--:|---|
| `timeout` | 169 | the stage timer runs out |
| `damage` | 117 | the mission vehicle takes too much damage |
| `outofvehicle` | 100 | the player leaves the required vehicle |
| `position` | 17 | the player/target leaves a required area |
| `followdistance` | 12 | a followed target gets too far away |
| `race` | 10 | race-specific failure (last place, etc.) |
| `keepbarrel` | 10 | a carried "barrel"/cargo is lost |

**How it works.** A condition is a *watcher* the engine runs alongside the objective. `AddCondition("type")`
opens it and `CloseCondition()` closes it (balanced 435/435, C14.3); the `SetCond…` setters parameterise it:
`SetCondTime(n)` for `timeout`, `SetCondMinHealth(n)` for `damage`, `SetCondTargetVehicle(…)` to say which
vehicle's damage or occupancy matters. So `AddCondition("timeout")` + `SetCondTime(60)` is "fail if 60
seconds pass"; `AddCondition("damage")` + `SetCondMinHealth` + `SetCondTargetVehicle` is "fail if this car is
wrecked."

**Why conditions are separate from objectives.** Decoupling "what you do" from "how you can fail" is what
lets the same objective carry different stakes in different stages. A `delivery` objective (C16.3) might have
a `timeout` in a time-pressure stage and no timeout in a relaxed one; a `goto` might add a `damage` condition
when you're escorting a fragile car. One objective vocabulary × seven condition types composes into the
game's whole difficulty design without new code. It also makes failure *readable*: a mission's conditions
tell you exactly how it can go wrong, which is the other half of understanding it.

**The distribution as design.** `timeout`, `damage`, and `outofvehicle` are 90% of all conditions — SHAR's
tension comes from **time pressure**, **protecting your vehicle**, and **staying in the car**. That
`outofvehicle` is so common reflects the game's identity: it wants you *driving*, and leaving the car mid
-mission usually fails you. `keepbarrel` and `followdistance` are the specialised ones, for the carry-cargo
and tailing missions.

**Reading a mission's stakes.** A stage's conditions are its risk profile. `timeout` + `damage` on a
delivery stage says "get there fast without wrecking the car." Pairing the objective (what) with the
conditions (how you fail) gives the complete stage in two lines — which is why documenting both vocabularies
together (C16.3 + here) is what makes missions fully legible.

**What happens if you bend it.**

- *Invent a condition type* — no watcher exists for it, so it never fires (the stage can't fail that way).
  Use one of the 7.
- *Add a condition without its `SetCond…` parameters* — an unparameterised `timeout` has no time,
  `damage` no threshold. Provide the setters the condition needs (C14.3).
- *Unbalance `AddCondition`/`CloseCondition`* — the parse desyncs (C14.1). Keep them matched (435/435).
