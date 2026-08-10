# C47.5 — Behaviours

> Behaviours — grounded in the verified level-script vocabulary.

AddBehaviour(...) attaches a behaviour to a placed actor, wiring it to the runtime behaviour/AI classes (AttackBehaviour, UFOAttackBehaviour, CharacterAi states, C42/C25). 25 uses in level 1 give actors jobs: patrol, guard, react, attack. A spawn point places the actor; a behaviour tells it what to do. Why: separating placement from behaviour lets the same actor model be a passive bystander or an aggressive guard depending on the attached behaviour. Bend it: attach a different behaviour to change what a spawned actor does; hook the behaviour class (C28.5) for custom logic.

## Cross-references
C8 (locators), C31 (wasps), C42/C25 (behaviours/AI), C45 (peds), C44 (level init), C39.4 (loading), C28 (modding).
