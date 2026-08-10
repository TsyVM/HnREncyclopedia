# C50.5 — Collector Cards & the Scrapbook

> The hidden-collectible layer: find cards around the world, view them in galleries, track them in
> the scrapbook.

## Collector cards (✅ verified)
`CardsDB` (`0x00614B98`) is the card database; `Card` (`0x00614BD4`) and `CollectorCard`
(`0x00614B8C`) are the card objects. Cards are **hidden collectibles** scattered through each level
(some guarded by wasps — recall `w_cardguard`, C47.3) that you pick up. There are seven per level
(one per level = a themed set), a classic completionist hunt.

## Viewing & tracking (✅ verified screens, C38)
- `CGuiScreenCardGallery` (`0x0061009C`) / `CGuiScreenViewCards` (`0x0060DCC4`) — browse the cards
  you've found.
- `CGuiScreenScrapBook` (`0x0060F888`) + `ScrapBookContents` + `ScrapBookStats` — the scrapbook that
  records collectibles and completion stats.
- Found-status persists on the character sheet (`CharacterSheetManager`, C27).

## Why collector cards
They're the exploration reward — a reason to leave the mission path and comb the level, with a
tangible collection to show for it. Guarding some behind wasps (C47) adds a light challenge.

## Bend it
- Card *placement* is world/spawn data (C47). The gallery/scrapbook are `CGuiScreen`s (C38).
- Completion state lives on the character sheet / save (C27).

## Cross-references
C47.3 (wasp-guarded cards), C38 (gallery/scrapbook screens), C27 (found-state in the save), C32
(collectibles), C50.1 (the loop).
