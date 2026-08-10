# C50.1 — The Economy Loop

> The whole progression in one sentence: **earn coins, spend them on cars/costumes/repairs, collect
> hidden cards, and your progress is saved** — all coordinated by `RewardsManager`.

## The loop (✅ verified)
```
EARN     smash gags/props/traffic (C32/C41) ─► coins ─► CoinManager (0x006077E0)
SPEND    Purchase Centre ─► PurchaseCar / PurchaseSkin / PurchaseReward ; WrenchIcon ─► repair
COLLECT  find CollectorCards (CardsDB 0x00614B98) ─► CardGallery / ScrapBook
PROGRESS RewardsManager (0x006111EC) ─► CharacterSheetManager (0x0061116C) ─► save (C27)
SELECT   PhoneBooth (CGuiScreenPhoneBooth) ─► start the next story mission
```

## Who owns what (✅ verified managers, C49)
- **`CoinManager`** — the coin balance and coin pickups.
- **`RewardsManager`** — the catalogue of rewards and what's unlocked.
- **`CharacterSheetManager`** — the persistent record (cards found, cars owned, missions done) that
  goes to the save file (C27).

## Why a loop, not just missions
The economy gives the open world *purpose between missions*: every smashed object and hidden card
feeds a reward you can see and buy. It's the carrot that turns free-roam into progression, and it's
why coins/cards are scattered everywhere.

## Bend it
Most economy tuning is data: coin values on gags (C41.4), reward prices, what an NPC sells
(C50.3). The managers can be hooked (C49.5) for deeper changes (e.g. infinite coins — a classic
trainer, single-player only, C28.6).

## Cross-references
C50.2–50.6 (each stage), C49 (the managers), C27 (the save), C32 (where coins come from).
