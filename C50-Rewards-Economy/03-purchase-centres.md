# C50.3 — Purchase Centres

> Where you spend coins: buy new cars (sold by characters like Gil), costumes, and rewards.

## Buying cars (✅ verified)
A purchasable car is declared in the level script with an NPC seller:
```
AddPurchaseCarReward( "gil", "gil", "npd", "gil_loc", 1.3, "gil_car" );
AddPurchaseCarReward( "simpson", "homer", "npd", "homer_loc", 1.3, "homer_car" );
```
Args: reward id, seller NPC model, type (`"npd"`), the seller's locator, a scale, and the car model
to grant. The seller stands at their locator (routed by `AddPurchaseCarNPCWaypoint("gil","gil_walk")`);
walking up triggers `ActionButton::PurchaseCar` (`0x006174EC`) to buy the car for coins. Sellers
include Gil, Otto, Barney, Kearney — very in-character (Gil the hapless salesman selling you cars is
a nice touch).

## Buying costumes & rewards (✅ verified)
- **Skins/costumes:** `ActionButton::PurchaseSkin` (`0x006171BC`) → the outfit is unlocked and
  viewable in `CGuiScreenSkinGallery`.
- **Rewards:** `ActionButton::PurchaseReward` (`0x0061760C`) → `CGuiScreenPurchaseRewards`
  (`0x0060DF2C`) / `IGuiScreenRewards`, backed by `RewardsManager` and the `Reward` objects. The exe
  strings `PurchaseCentre%d_%d`, `PurchaseRewards`, `RewardBG`, `BindReward` confirm the screen flow.

## Why NPC sellers, not a menu
Selling cars through a *character* at a *place* keeps the purchase in the world (you drive to Gil)
rather than a disembodied menu — reinforcing the open-world feel and giving the characters a role.

## Bend it
- Add/change purchasable cars: edit `AddPurchaseCarReward` (seller, price implied by reward data,
  car granted).
- Change what a purchase centre offers via the reward data / `RewardsManager` (C49.5 to hook).

## Cross-references
C24 (the cars you buy), C25/C47 (the seller NPCs + waypoints), C49 (`RewardsManager`), C38 (the
gallery/purchase screens), C14 (the reward scripts).
