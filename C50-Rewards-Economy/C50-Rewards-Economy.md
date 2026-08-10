# Chapter 50 — Rewards & the Economy Loop

> **Goal of this chapter:** decode the game's economy — how you **earn** coins, where you **spend**
> them (buy cars, costumes, rewards; repair your car), how you **collect** cards and track them in
> the scrapbook, and how you **start** story missions at the phone booth. This is the whole
> reward/progression loop we referenced but never assembled.

Hit & Run isn't only driving and missions — there's a full progression economy underneath:
smash things for coins, spend them at purchase centres on new cars (from characters like Gil) and
outfits, hunt hidden collector cards, and pick your next story mission at a phone booth. Every
piece is a confirmed class or script command.

**Key finding (✅ verified):** the loop is **earn → spend → collect → progress**, each with real
backing. **Earn:** the `CoinManager` (`0x006077E0`) tracks coins dropped by smashing gags/props/
traffic (C32/C41). **Spend at Purchase Centres:** `ActionButton::PurchaseCar` (`0x006174EC`),
`PurchaseSkin` (`0x006171BC`), and `PurchaseReward` (`0x0061760C`) buy vehicles, costumes, and
rewards; cars are sold by NPCs set up with `AddPurchaseCarReward("gil","gil","npd","gil_loc",1.3,
"gil_car")`. The `WrenchIcon` action (`0x00617148`) + `RepairCostInfo` string is the **car repair**.
**Select missions:** the **phone booth** (`CGuiScreenPhoneBooth` `0x0060E020`, `PhoneBooth%d_%d`
locators) is where story missions are chosen. **Collect:** `CardsDB`/`Card`/`CollectorCard` are the
hidden collector cards, viewed in `CGuiScreenCardGallery`/`ViewCards` and the `CGuiScreenScrapBook`.
**Costumes:** skins via `PurchaseSkin` + `CGuiScreenSkinGallery`. All of it is owned by
`RewardsManager` (`0x006111EC`) and recorded in `CharacterSheetManager` (`0x0061116C`, the save,
C27).

---

## Deep-dive pages

- [C50.1 — The Economy Loop](01-the-loop.md): earn → spend → collect → progress, and who owns it.
- [C50.2 — Coins](02-coins.md): `CoinManager`, where coins come from, the coin model.
- [C50.3 — Purchase Centres](03-purchase-centres.md): buying cars (Gil et al.), skins, and rewards.
- [C50.4 — The Phone Booth](04-phone-booth.md): `CGuiScreenPhoneBooth` — selecting story missions.
- [C50.5 — Collector Cards & the Scrapbook](05-cards-scrapbook.md): `CardsDB`, galleries, the scrapbook.
- [C50.6 — Costumes, Repair & Modding](06-costumes-repair-modding.md): skins, the wrench/repair, and editing the economy.

---

## 50.1 The loop (✅ verified)

Earn coins (`CoinManager`) → spend at purchase centres (`PurchaseCar`/`Skin`/`Reward`) and repair
(`WrenchIcon`) → collect cards (`CardsDB`) → progress recorded on the character sheet
(`CharacterSheetManager`, C27), all under `RewardsManager`. [C50.1](01-the-loop.md).

## 50.2 Coins (✅ verified)

`CoinManager` (`0x006077E0`) tracks the coin balance; coins drop from smashed gags/props/traffic
(C32/C41); the coin pickup model is set in level init (`SetCoinDrawable`, C44). [C50.2](02-coins.md).

## 50.3 Purchase centres (✅ verified)

At a **Purchase Centre** (`PurchaseCentre%d_%d`) you buy: **cars** — sold by NPCs declared with
`AddPurchaseCarReward(id, npcModel, "npd", locator, scale, carModel)` (Gil, Otto, Barney, Kearney…)
— **skins/costumes** (`PurchaseSkin`), and **rewards** (`PurchaseReward` → `CGuiScreenPurchaseRewards`).
[C50.3](03-purchase-centres.md).

## 50.4 The phone booth (✅ verified)

`CGuiScreenPhoneBooth` (`0x0060E020`) at `PhoneBooth%d_%d` locators is the **story-mission select** —
you answer the phone to pick/start the next mission. [C50.4](04-phone-booth.md).

## 50.5 Collector cards & scrapbook (✅ verified)

Hidden **collector cards** (`CardsDB` `0x00614B98`, `Card`, `CollectorCard`) are found around each
level (some guarded by wasps, C47); viewed in `CGuiScreenCardGallery`/`ViewCards` and tracked in the
`CGuiScreenScrapBook`(+`Contents`/`Stats`). [C50.5](05-cards-scrapbook.md).

## 50.6 Costumes, repair & modding (✅ verified)

Costumes are **skins** (`CGuiScreenSkinGallery`); the **wrench** (`WrenchIcon` + `RepairCostInfo`)
repairs your car for coins. Editing the economy is mostly script + reward data. [C50.6](06-costumes-repair-modding.md).

---

## What this chapter established

- The economy is a full **earn → spend → collect → progress** loop, owned by `RewardsManager` and
  saved via `CharacterSheetManager` (C27).
- **Purchase Centres** sell cars (from NPCs like Gil), costumes (skins), and rewards; the **wrench**
  repairs; the **phone booth** selects story missions.
- **Collector cards** (`CardsDB`) are the hidden-collectible layer, shown in galleries/scrapbook.

**Cross-references:** C32 (coins/collectibles/inventory), C27 (the save/character sheet), C44 (coin
model in init), C47 (card-guarding wasps), C24 (the cars you buy), C38 (the gallery/booth screens),
C49 (`CoinManager`/`RewardsManager` in the manager layer), C14 (the reward scripts).
