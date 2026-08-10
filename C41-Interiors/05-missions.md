# C41.5 — Interiors in Missions

> Some story beats happen inside. The mission system has confirmed hooks for interior state.

## The classes (✅ verified)
- **`InteriorObjective`** (`0x006115E8`) — an objective satisfied by the player being inside a
  named interior (e.g. "go into the Kwik-E-Mart").
- **`LeaveInteriorCondition`** (`0x00611348`) — a condition met by leaving the interior (e.g.
  "get out, then…").
- **`GetOutOfCarCondition`** — the related on-foot gate (you must be out of the car), which
  interiors imply since you enter on foot.

## How they compose
Missions are objective/condition graphs (C16). An interior beat is just those nodes: *enter
interior X* (`InteriorObjective`) → do something inside (talk to an NPC, trigger a gag/NIS) →
*leave* (`LeaveInteriorCondition`). The transition fade (C40) and the swap (C41.1) run
automatically at the boundaries.

## Ambient life inside
`AddAmbientCharacter(..., place)` (in `leveli.mfk`) populates interiors with NPCs — Apu in the
Kwik-E-Mart, Lisa in the school — so an interior objective has someone to interact with.

## What happens if you bend it
A custom mission can require entering your own interior or use `LeaveInteriorCondition` as a
beat. Keep objective ids consistent with the interior ids (C41.3).

## Cross-references
C16 (missions & objectives), C41.1/41.2 (the interior system & flow), C25 (ambient characters),
C17 (choreography/NIS beats inside).
