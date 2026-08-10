# C47.3 — The Wasps / Bee Cameras

> The Wasps / Bee Cameras — grounded in the verified level-script vocabulary.

The w_-prefixed spawn points (w_lemon, w_schoolroof1, w_bonuscar, w_stonetemple, w_trailor1/2, w_cardguard, w_bridge1/2, w_barn) place the flying wasp enemies (the 'bee cameras', internally Shelley/beecamera). They run AttackBehaviour / ActorAnimationWasp (C42) and tie to the wasp/surveillance system (C31). They guard collectibles and story spots (w_cardguard guards a collector card, w_bonuscar a bonus car). Why: dormant proximity-spawned guardians gate rewards and add threat without always simulating. Bend it: move/add wasp spawns by editing the w_ spawn points; retune their range.

## Cross-references
C8 (locators), C31 (wasps), C42/C25 (behaviours/AI), C45 (peds), C44 (level init), C39.4 (loading), C28 (modding).
