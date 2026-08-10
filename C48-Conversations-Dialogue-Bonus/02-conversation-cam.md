# C48.2 — The Conversation Camera

> The Conversation Camera — grounded in the verified level-init dialogue vocabulary.

SetConversationCam(shot, framing, id) sets up a two-shot: shot 0 uses a player framing (pc_far/pc_near), shot 1 an NPC framing (npc_far/npc_near); the game cuts between them as each speaks. SetCamBestSide(bestside, id) picks the flattering side to shoot from. It is a scripted use of the camera system (C36) for staged dialogue. Why: a shot/reverse-shot is the film-grammar way to shoot a two-person conversation, and doing it with named framings lets designers stage each chat without new camera code. Bend it: change framings (near/far), the best side, or add shots for a different feel.

## Cross-references
C16 (missions), C36 (cameras), C42 (gesture animations), C19 (dialogue audio), C22 (localized text), C8 (locators), C44 (level init).
