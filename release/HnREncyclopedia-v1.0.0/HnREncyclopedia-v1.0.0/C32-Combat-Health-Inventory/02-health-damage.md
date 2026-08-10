# C32.2 — Health & Damage

**What it is.** How the game tracks whether the player, their vehicle, and mission objects can take a hit —
and it's simpler than you'd expect: there's no dedicated "Health" class, because health *is* hit points, the
same value the `.con` sets for a car.

**How it works (✅ verified).** Damage is tracked against **hit points** and gates missions through
conditions:

```
DamageCondition : MissionCondition   (0x006113CC)  — the "damage" mission condition (C16.4)
NoDamageBonusObjective : BonusObjective (0x0061190C)  — reward for taking no damage
```

A vehicle's durability is `SetHitPoints` (C15.5) — the same value for the player's car, mission cars, and the
police (C31.2). Characters have their own hit points similarly. The **`damage` mission condition** (C16.4,
the second-most-common condition at 117 uses) watches a tracked object (usually the mission vehicle,
`SetCondTargetVehicle`, C14.3) and **fails the stage** if it's damaged past a threshold (`SetCondMinHealth`,
C14.3). Conversely, **`NoDamageBonusObjective`** rewards completing a mission without taking damage — the
health counterpart to the `NoCopBonusObjective` (C31.4).

**Why no dedicated health class.** Health as "hit points" folded into every object (via `SetHitPoints`, C15)
rather than a separate `Health` component is a simplicity choice: the same value that makes a car destructible
makes a character or a mission object destructible, and the same `DamageCondition` watches any of them. One
concept (hit points), one condition (damage), reused everywhere. This is lighter than a full health/status
system, and it fits the game — you don't have a health bar in the RPG sense; you have objects with hit points
that break, and missions that fail if the wrong thing breaks. It's the same "reuse one mechanism" instinct as
health being hit points, combat being one kick (C32.1), and the police being a car with a chase AI (C31.2).

**The mission tie.** Health matters almost entirely *through missions*: a stage with a `damage` condition is
a stage where you must protect something (your car, an escort). This is why `damage` is such a common
condition (C16.4) — "don't wreck the car" is a core SHAR mission stake, alongside "don't run out of time"
(`timeout`) and "stay in the car" (`outofvehicle`). Health isn't a standalone survival system; it's a mission
*constraint* the designers apply where the scene needs it.

**What happens if you bend it.**

- *Look for a health system beyond hit points* — there isn't one; health is `SetHitPoints` (C15) plus the
  `damage` condition (C16.4). Model it as hit points.
- *Raise a mission car's hit points to trivialise a `damage` condition* — you defeat the mission's stake.
  Tune within the intended challenge.
- *Rely on a `DamageCondition` member offset* — class/vtable ✅, offset ⏳. Diff (C4.3).
