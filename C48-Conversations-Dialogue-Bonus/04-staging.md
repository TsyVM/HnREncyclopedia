# C48.4 — Staging the Scene

> Staging the Scene — grounded in the verified level-init dialogue vocabulary.

SetBonusMissionDialoguePos(id, playerPos, npcPos, carStart) places the player and NPC at named locators (C8) and sets the car start for after the chat; AddBonusMissionNPCWaypoint(npc, wp) routes the NPC into and out of the scene. Together they block the little scene: where each stands, where they enter/leave, where you resume driving. Why: locator-based staging lets the same conversation system be reused anywhere by just naming different spots. Bend it: move the participants by re-pointing the positions; re-route the NPC with waypoints.

## Cross-references
C16 (missions), C36 (cameras), C42 (gesture animations), C19 (dialogue audio), C22 (localized text), C8 (locators), C44 (level init).
