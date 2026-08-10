# C16.6 — Rewards & the Runtime Mission System

**What it is.** The payoff side of missions — the reward system that turns completion into unlocked cars —
and the runtime classes the mission scripts drive. This closes the chapter by connecting authored missions
(C16.1–C16.5) to the game's progression and to the engine.

**Rewards (✅ verified).** `BindReward` connects a mission (or race, or purchase) to what it grants. The
documented syntax and real bindings, from `rewards.mfk`:

```
BindReward( <name>, <file>, <reward type>, <quest type>, <level> );
BindReward( <name>, <file>, <reward type>, "forsale", <level>, <coin cost>, <seller> );

BindReward("famil_v","art\cars\famil_v.p3d","car","defaultcar",   1);            // starting car
BindReward("cletu_v","art\cars\cletu_v.p3d","car","bonusmission",1);             // bonus-mission reward
BindReward("elect_v","art\cars\elect_v.p3d","car","streetrace",  1);             // race reward
BindReward("plowk_v","art\cars\plowk_v.p3d","car","forsale", 1, 40, "simpson");  // buy for 40 coins from Simpson
```

The reward **type** is almost always `"car"`; the **quest type** says how it's earned:

- **`defaultcar`** — the level's starting car.
- **`bonusmission`** — completing the bonus mission (C16.5).
- **`streetrace`** — winning a street race (C16.5).
- **`forsale`** — bought for coins from a named seller (`simpson`, `gil`, …).

So the whole car roster is unlocked through play — mission and race completion — or purchase with the coins
collected from gags and objectives (C16.3 `coins`, C14.4). `rewards.mfk` documents each level's set and total
coin cost; `e3rwrds.mfk` is the E3-demo variant. This `BindReward` graph *is* the game's progression economy,
readable in one file.

**The runtime mission system (✅ names / ⏳ offsets).** At load, the mission scripts build the RTTI-verified
`Mission` family (45 classes in the data set): `Mission`, `MissionStage`, `MissionObjective` and its
subclasses (one per objective type, C16.3), plus the condition watchers. The **class names and inheritance
are verified** from `Simpsons.exe`'s RTTI; the **member offsets are ⏳**, recovered by diffing (C4.3). So we
can state that `AddObjective("goto")` constructs a specific `MissionObjective` subclass and how that class
sits in the hierarchy, while marking the exact fields as the open frontier.

**Why the reward graph is centralised.** Keeping every unlock in `rewards.mfk` (rather than scattered through
missions) means the progression can be balanced in one place — the designer sees the whole economy: which
car each mission/race grants, what's for sale and for how much. It also decouples *earning* from *doing*: a
mission's script (C16.2) doesn't need to know what it unlocks; the reward binding connects them by name. This
is the same data/logic separation as the rest of the engine — missions do, rewards grant, and a name links
them.

**The modding consequence.** To change what a mission unlocks, edit its `BindReward` line; to add a
purchasable car, add a `forsale` binding with a cost and seller; to rebalance the economy, edit `rewards.mfk`
in one place. Because rewards are separate data, you can retune progression without touching mission logic —
and because the mission runtime classes are RTTI-verified, a native mod can identify a live mission/objective
by class (offsets ⏳).

**What happens if you bend it.**

- *Bind a reward to a car file that isn't there* — the unlock grants nothing. Ensure the `.p3d` (C7) and its
  `.con` (C15) exist.
- *Set a `forsale` reward without a cost/seller* — it can't be purchased correctly. Provide the extra
  arguments the `forsale` form needs.
- *Rely on a `Mission*` member offset* — it's ⏳; diff for it first (C4.3). Names are safe to use; offsets are
  not until verified.

**Next:** [Chapter 17 — Choreography & Characters](../C17-Choreography-Characters/C17-Choreography-Characters.md).
