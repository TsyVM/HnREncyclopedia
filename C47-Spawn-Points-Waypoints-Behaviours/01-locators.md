# C47.1 — Locators as Anchors

> Locators as Anchors — grounded in the verified level-script vocabulary.

Almost everything placed in SHAR is anchored to a named locator (C8) — a point or group baked into the world by the artists. Scripts name locators (level1_carstart, w_lemon, m0_apu_place) instead of raw coordinates. Why: decoupling placement (art-authored locators) from logic (scripts that reference them) lets designers move a spawn by moving a locator, with no script change, and keeps scripts readable. Bend it: re-point a spawn/route at a different locator name; add locators in the world art (C8) for new spots.

## Cross-references
C8 (locators), C31 (wasps), C42/C25 (behaviours/AI), C45 (peds), C44 (level init), C39.4 (loading), C28 (modding).
