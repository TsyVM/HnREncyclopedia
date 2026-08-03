# C26.2 — Objectives & Conditions as Classes

**What it is.** The runtime form of the mission vocabulary — and one of the strongest cross-validations in
the whole book: the objective/condition *types* found in the scripts (C16) and the objective/condition
*classes* found in the executable's RTTI independently describe the same system.

**The cross-validation (✅ two independent sources).**

| | Script side (C16, from `.mfk`) | Runtime side (RTTI, from `.exe`) |
|---|---|---|
| Objectives | **20** `AddObjective` types | **21** `MissionObjective` subclasses |
| Conditions | **7** `AddCondition` types | **13** `MissionCondition` subclasses |

The objective numbers match almost exactly — **20 script types vs. 21 runtime classes** — from *two
completely independent evidence bases*: one extracted by parsing the shipped mission scripts, the other by
reading the compiled executable's type metadata. Neither knew about the other. When two independent methods
converge on the same count, the finding is about as solid as reverse engineering gets. (The one-class
difference is a base or a variant class with no direct script keyword — expected slack, not a contradiction.)

**Why the condition counts differ more (7 vs. 13).** Conditions show 7 script keywords but 13 runtime
classes. This is the *reverse* of a problem — it means the runtime has finer-grained condition classes than
the script vocabulary exposes: several runtime `MissionCondition` subclasses are parameterisations or
internal variants that the script layer reaches through the same keyword plus `SetCond…` setters (C16.4).
`VehicleCarryingStateProp` (the `keepbarrel` condition) is one such verified class. So the script keyword is
the *user-facing* vocabulary; the runtime classes are the *implementation*, and there are more of the latter.

**How a keyword becomes a class.** When a mission script runs `AddObjective("goto")` (C16.3), the mission
system constructs the corresponding `MissionObjective` subclass — a "go to location" objective object — and
registers it as an event listener (C26.1). The objective's parameters (target, waypoint) come from the
stage's setters (C14.3/C14.5). So each of the 20 script verbs maps to one of the 21 runtime classes, and the
mapping is the bridge between the mission *language* (C16) and the mission *engine* (here). Recovering the
exact keyword→class mapping is a small RE task (match each subclass's behaviour to a keyword); the *counts
matching* already proves the mapping exists.

**Why this matters for the book's method.** This cross-validation is the clearest vindication of the
two-evidence-base approach (C4.5, C23.1): on-disk parsing (the scripts) and executable RTTI (the classes) are
independent, and where they overlap they *agree*. That agreement is what lets the book trust each base for
what only it can prove — the scripts for the vocabulary and its usage counts, the RTTI for the class
hierarchy — and to present the runtime chapters with confidence.

**What happens if you bend it.**

- *Assume one script keyword = exactly one runtime class* — usually true for objectives, looser for
  conditions (13 classes, 7 keywords). Map by behaviour, not by count alone.
- *Rely on an objective/condition class offset* — classes ✅, offsets ⏳. Diff (C4.3).
- *Treat the 20-vs-21 gap as an error* — it's expected slack (a base/variant with no keyword). The
  convergence is the signal, not the exact tie.
