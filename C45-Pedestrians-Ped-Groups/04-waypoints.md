# C45.04 — Wander Waypoints

> Wander Waypoints — grounded in the verified level-init vocabulary.

`AddAmbientNPCWaypoint("eddie","eddie_walk1")` (×55 in level 1) links an NPC to path nodes it walks between, giving purposeful movement. The waypoints are locators (C8) in the world. Why: scripted wander paths make NPCs look like they have somewhere to be, far better than random drift, at trivial cost. Bend it: add waypoints to route an NPC along a custom path; ties to the broader waypoint/behaviour system (C47).

## Cross-references
C44 (level init), C25 (characters/AI), C42 (locomotion/attacks), C41 (interior NPCs), C47 (waypoints/behaviours), C39 (actor limits).
