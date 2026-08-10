# C47.2 — Spawn Points by Locator Script

> Spawn Points by Locator Script — grounded in the verified level-script vocabulary.

AddSpawnPointByLocatorScript(locator, script, actor, locator2, range, param) spawns an actor at a locator when the player comes within range. In level 1 it places the wasp beecamera Shelley at w_* locators with ranges like 15.0-60.0. It is the general proximity-spawn primitive: spawn X near locator Y within radius R. Why: proximity spawning keeps enemies/actors dormant until you approach, saving simulation and making encounters feel placed. Bend it: change the actor, locator, or range to move/retune an encounter.

## Cross-references
C8 (locators), C31 (wasps), C42/C25 (behaviours/AI), C45 (peds), C44 (level init), C39.4 (loading), C28 (modding).
