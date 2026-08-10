# C45.06 — Modding the Crowd

> Modding the Crowd — grounded in the verified level-init vocabulary.

Edit `leveli.mfk`: change the models and weights in each `CreatePedGroup…ClosePedGroup` block to re-cast the crowd; add/replace `AddAmbientCharacter` named NPCs; add `AddAmbientNPCWaypoint` paths. Denser crowds need a larger actor pool (`PreallocateActors`, C44.4/C39). Any new ped model must be packaged/loaded (C39.4) or the spawn fails silently. Reversible, single-player (C28.6).

## Cross-references
C44 (level init), C25 (characters/AI), C42 (locomotion/attacks), C41 (interior NPCs), C47 (waypoints/behaviours), C39 (actor limits).
