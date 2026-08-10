# C45.02 — The Crowd Spawn System

> The Crowd Spawn System — grounded in the verified level-init vocabulary.

The engine keeps a budgeted number of peds near the player, spawning from the active ped group ahead of you and despawning those left behind, so density stays roughly constant as you move. The budget is bounded by the preallocated actor pool (C44.4/C39). Why: streaming a moving bubble of crowd is far cheaper than populating the whole city, and keeps the world feeling full wherever you are. Bend it: raise density by enlarging the actor pool + budget (C39); too many and you hit the actor cap.

## Cross-references
C44 (level init), C25 (characters/AI), C42 (locomotion/attacks), C41 (interior NPCs), C47 (waypoints/behaviours), C39 (actor limits).
