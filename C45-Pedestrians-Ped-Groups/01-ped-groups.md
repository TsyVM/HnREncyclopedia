# C45.01 — What a Ped Group Is

> What a Ped Group Is — grounded in the verified level-init vocabulary.

A ped group is a numbered, weighted pool of pedestrian models. `CreatePedGroup(N)` opens it, `AddPed("model", weight)` adds a model with a relative spawn weight, `ClosePedGroup()` finalizes it. Multiple groups let different areas draw different crowds. The weight (2nd arg) biases how often a model appears. Why: a weighted pool gives a varied, controllable crowd from a handful of models without hand-placing anyone. Bend it: change models/weights to re-cast the crowd; add models (must be loaded, C44.2).

## Cross-references
C44 (level init), C25 (characters/AI), C42 (locomotion/attacks), C41 (interior NPCs), C47 (waypoints/behaviours), C39 (actor limits).
