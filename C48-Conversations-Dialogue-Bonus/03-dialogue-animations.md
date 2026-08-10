# C48.3 — Dialogue Animations

> Dialogue Animations — grounded in the verified level-init dialogue vocabulary.

AddAmbientPcAnimation and AddAmbientNpcAnimation queue gesture clips the player and NPC perform while talking: dialogue_open_arm_hand_gesture, dialogue_scratch_head, dialogue_thinking, dialogue_hands_in_air, dialogue_no, and none (idle). ClearAmbientAnimations resets the set for a scene. The clips are ordinary animations played by the animation players (C42.5). Why: gesturing makes a static conversation feel alive and characterful (very Simpsons) at the cost of a few animation clips. Bend it: swap the gesture set per character/scene; add clips (must exist on the rig, C42.7).

## Cross-references
C16 (missions), C36 (cameras), C42 (gesture animations), C19 (dialogue audio), C22 (localized text), C8 (locators), C44 (level init).
