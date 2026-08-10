# C48.1 — Bonus Encounters

> Bonus Encounters — grounded in the verified level-init dialogue vocabulary.

AddNPCCharacterBonusMission(npc, type, dialoguePos, id, reward, 'intro', flag, finish) declares a bonus mission or street race against a specific NPC. In level 1: sr1 vs Milhouse, sr2 vs Nelson, sr3 vs another kid — the checkered-flag street races. The args wire the NPC, its dialogue staging id, the mission id, the reward, and intro/finish tags. Why: packaging an optional encounter as one declaration lets designers scatter many bonus races/missions across a level cheaply, each self-contained. Bend it: add your own AddNPCCharacterBonusMission for a new race; change the NPC or reward.

## Cross-references
C16 (missions), C36 (cameras), C42 (gesture animations), C19 (dialogue audio), C22 (localized text), C8 (locators), C44 (level init).
