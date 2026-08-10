# C16.3 — The 20 Objective Types

**What it is.** The complete, closed vocabulary of what a mission stage can ask the player to *do*. Every
`AddObjective("type")` in the game uses one of **20** types — verified by extracting and counting all
`AddObjective` calls across `scripts/missions/`.

**The full set (✅ verified counts).**

| Type | Uses | What the player must do |
|---|--:|---|
| `goto` | 191 | drive/walk to a location |
| `dialogue` | 139 | play through a conversation |
| `talkto` | 99 | approach and talk to a character |
| `getin` | 48 | get into a specified vehicle |
| `race` | 44 | win a race |
| `timer` | 27 | do something before time runs out |
| `interior` | 19 | enter an interior |
| `losetail` | 17 | lose a pursuer |
| `destroy` | 15 | destroy a target object/vehicle |
| `delivery` | 15 | deliver something/someone |
| `dump` | 13 | drop off cargo/an item |
| `follow` | 7 | follow a target at distance |
| `coins` | 7 | collect a number of coins |
| `fmv` | 6 | trigger a full-motion cutscene (C20) |
| `buycar` | 6 | purchase a vehicle |
| `pickupitem` | 4 | pick up an item |
| `gooutside` | 4 | leave an interior |
| `destroyboss` | 4 | defeat the level boss (C16.5) |
| `buyskin` | 4 | purchase a costume |
| `dummy` | 2 | a placeholder/no-op stage |

**How it works.** Each type names a *runner* the engine implements — code that knows how to watch for "the
player reached the location" (`goto`) or "the target is destroyed" (`destroy`). The objective's parameters
come from the stage's setters (target vehicle via `SetObjTargetVehicle`, C14.3; waypoints via
`AddObjectiveNPCWaypoint`, C14.5; talk target via `SetTalkToTarget`). So `AddObjective("goto")` plus a
waypoint is "go *there*"; `AddObjective("talkto")` plus a target is "talk to *them*."

**Why a closed vocabulary.** A fixed set of objective types is what makes missions *data*, not code. The
engine implements each runner once; designers compose missions by choosing types and parameters. Twenty
types cover the whole game — which tells you SHAR's mission design is deliberately built from a small
palette of reusable verbs, recombined across ~90 missions. The distribution is the game's DNA: `goto` +
`dialogue` + `talkto` are 60% of all objectives, so SHAR is fundamentally *drive somewhere and have a
conversation*, with racing, destroying, and delivering as the action spice.

**Reading a mission's shape from its objectives.** Dump a mission's `AddObjective` lines and you have its
skeleton: a chain of `goto`/`talkto`/`dialogue` is a story mission; a `race` is a race; a `destroyboss` marks
a finale. You can classify any mission by its objective sequence before reading a single parameter.

**What happens if you bend it.**

- *Invent an objective type* — there's no runner for it, so the stage can never complete (C14.3). Use one of
  the 20.
- *Use an objective without its required parameters* — a `talkto` with no target, a `goto` with no waypoint,
  has nothing to check. Provide the setters the type needs.
- *Misuse `dummy`* for real gameplay — it's a placeholder that completes trivially. Use it only as a spacer.
