# C31.4 — Scripting Pursuit

**What it is.** How missions control the police pursuit — the `SetHitNRun` script command that tunes the
meter per mission, and the `NoCopBonusObjective` that rewards avoiding the cops. This is where the enforcement
systems (C31.1–C31.2) meet the mission scripting (C14/C16).

**How it works (✅ verified).** Two hooks:

- **`SetHitNRun(...)`** — a mission-script command used **78 times** across the game (verified in the MFK
  vocabulary, C14). It tunes the Hit & Run system for a mission: whether the meter is active, how sensitive it
  is, and how the chase behaves. Some missions want the pressure of a possible chase (a getaway); others — a
  peaceful escort or delivery — **suppress** the meter so the police don't interfere. So the pursuit isn't a
  fixed global; each mission dials it via `SetHitNRun`.
- **`NoCopBonusObjective : BonusObjective`** (0x00611958) — a bonus objective (C16) that rewards completing a
  mission **without triggering the cops**. It watches the Hit & Run state (C31.1) and grants a bonus if you
  stayed clean. This turns "avoid the police" into an optional challenge with a payoff.

Together they make the police a *designed* element of each mission, not just an ambient nuisance: the
designer decides, per mission, whether the cops are in play (`SetHitNRun`) and whether avoiding them is
rewarded (`NoCopBonusObjective`).

**Why script-controlled pursuit.** A global, always-on pursuit would fight the mission design — you can't
script a careful escort if the police might randomly appear. Making the meter *mission-configurable* lets each
scene use exactly the tension it wants: a chase mission cranks it up, a delivery suppresses it, a "get away
clean" mission adds the `NoCopBonusObjective` to reward stealth. This is the same *data-driven, per-mission*
philosophy as the rest of the mission system (C16): the engine provides the pursuit *mechanism*, and the
scripts decide *when and how* it applies. It's why the same open world can host both frantic police chases
and calm story missions.

**The reward tie.** `NoCopBonusObjective` being a `BonusObjective` (C16) means it plugs into the reward
economy (C16.6): staying clean can unlock content, the same way completing bonus missions and races does.
This makes police avoidance a *first-class* objective with a `BindReward` (C16.6) payoff, not just a
soft preference. The player who evades the cops gets something concrete for it.

**What happens if you bend it.**

- *Add mayhem-heavy content to a mission that suppressed the meter* — you may re-enable heat the designer
  turned off. Check the mission's `SetHitNRun` (C14).
- *Rely on the objective/manager offsets* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Remove `SetHitNRun` from a mission* — it reverts to default pursuit behaviour, which may not suit the
  scene. Set it deliberately per mission.
