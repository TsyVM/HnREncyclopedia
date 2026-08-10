# C50.4 — The Phone Booth

> How you start story missions: answer the phone.

## What it is (✅ verified)
`CGuiScreenPhoneBooth` (`0x0060E020`) is the **story-mission select** screen. Phone booths are placed
around each level at `PhoneBooth%d_%d` locators (exe strings `PhoneBooth`, `PhoneBooths`); walking to
a ringing booth and answering opens this screen to start (or replay) the level's story missions.

## Why a phone booth
It's the game's diegetic mission-giver: instead of an abstract menu, the story reaches you by phone
(very sitcom). Placing booths around the level also spaces the missions geographically and gives you
a reason to drive to a spot.

## The flow
```
drive to a ringing PhoneBooth locator ─► answer ─► CGuiScreenPhoneBooth ─► pick a mission
   ─► MissionManager loads the mission (C16) ─► (conversation intro, C48) ─► play
```
This complements the **bonus** encounters (street races) which are started in the world by driving
up to an NPC (C48) rather than at a booth.

## Bend it
- The booth is a `CGuiScreen` (C38) — hookable to change the mission list or add entries (C38.3).
- Booth *placement* is locators in the level (C8/C47).

## Cross-references
C16 (missions the booth starts), C48 (mission intro conversations), C38 (the screen system), C8/C47
(booth locators), C50.1 (its place in the loop).
