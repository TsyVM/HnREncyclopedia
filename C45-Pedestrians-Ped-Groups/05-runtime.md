# C45.05 — Peds at Runtime

> Peds at Runtime — grounded in the verified level-init vocabulary.

Live pedestrians are `Character`/`NPCharacter`/`Pedestrian` objects (C25) under a `CharacterManager`. They move on locomotion sets (C42.4), follow waypoints (C45.4), and react to the player — fleeing an oncoming car, getting kicked (C42.2), being run down (ties to Hit & Run, C31). Why: reusing the character/AI stack for the crowd means peds get the same movement/animation/reaction machinery as story NPCs for free. Bend it: hook `CharacterManager`/`Character` to alter crowd behaviour (C28.5).

## Cross-references
C44 (level init), C25 (characters/AI), C42 (locomotion/attacks), C41 (interior NPCs), C47 (waypoints/behaviours), C39 (actor limits).
