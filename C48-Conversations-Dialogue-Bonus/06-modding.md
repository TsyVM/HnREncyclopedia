# C48.6 — Modding Conversations

> Modding Conversations — grounded in the verified level-init dialogue vocabulary.

Edit the level init: add an AddNPCCharacterBonusMission for a new encounter; re-stage with SetBonusMissionDialoguePos + SetConversationCam + SetCamBestSide; change the gesture set via AddAmbientPc/NpcAnimation. New participants need loaded character models (C39.4) and their locators in the world art (C8). Voice lines are RSD swaps in dialog.rcf (C19); subtitles via localization (C22). Native: hook the camera/animation classes for custom staging (C28.5). Single-player, reversible (C28.6).

## Cross-references
C16 (missions), C36 (cameras), C42 (gesture animations), C19 (dialogue audio), C22 (localized text), C8 (locators), C44 (level init).
