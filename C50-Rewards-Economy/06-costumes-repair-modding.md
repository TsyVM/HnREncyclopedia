# C50.6 — Costumes, Repair & Modding

> The last economy pieces — outfits and car repair — and how to mod the whole loop.

## Costumes / skins (✅ verified)
Costumes are **skins**: bought with `ActionButton::PurchaseSkin` (`0x006171BC`) and browsed in
`CGuiScreenSkinGallery` (`0x0060F5FC`). A skin swaps the character's texture/model variant. They're a
cosmetic reward sink for coins.

## The wrench — car repair (✅ verified)
`ActionButton::WrenchIcon` (`0x00617148`), with the exe string `RepairCostInfo`, is the **car
repair**: at a repair spot you spend coins to fix your damaged vehicle. (This is what the "wrench" is
— vehicle repair, not a weapon.) Damage accrues from the vehicle-physics/destruction system (C35).

## Modding the economy
- **Prices & what's sold:** the reward data + `AddPurchaseCarReward` scripts (C50.3) — change
  sellers, cars, and (via reward data) costs.
- **Coin values:** `GagSetCoins` on gags (C41.4), destructible payouts (C32).
- **Cosmetics:** new skins are texture/model swaps (C5/C7) surfaced through the skin gallery.
- **Deeper changes:** hook `RewardsManager`/`CoinManager` (C49.5) — e.g. free purchases, max coins
  (trainer). Single-player/offline, reversible (C28.6).

## Cautions
- The economy is coupled to the **save** (`CharacterSheetManager`, C27) — bad edits can corrupt
  progress; back up the save.
- Reward/skin ids must match across script, gallery, and save.

## Cross-references
C35 (vehicle damage the wrench repairs), C5/C7 (skin assets), C49 (managers to hook), C27 (save
coupling), C41.4/C32 (coin sources), C28.6 (ethics).
