# Chapter 32 — Combat, Health, Collectibles & Inventory

> **Goal of this chapter:** decode the moment-to-moment player systems that aren't driving — the kick/attack
> combat, health and damage, and the collection economy (coins, cards, items) with its inventory. These are
> what you do on foot and what you gather across Springfield.

SHAR is a driving game *and* an on-foot collect-a-thon with light combat. This chapter decodes those systems
from the verified RTTI set (all with confirmed vtable addresses): the kick, the enemies that attack you,
health and damage, and the coins/cards/items you collect into an inventory.

**Key finding (✅ verified):** combat is a **kick** (`KickAction`) against enemies with **`AttackBehaviour`**
(and `UFOAttackBehaviour` — the alien enemies); health is per-object **hit points** (C15) with
**`DamageCondition`**/**`NoDamageBonusObjective`**; and the economy is **coins** (`CoinManager`),
**collector cards** (`CardsDB`/`CardGallery`), **items** (`PickupItemObjective`), and a generic
**`tInventory`**, spent through **`RewardsManager`** (C16.6).

---

## Deep-dive pages

- [C32.1 — Combat: the Kick & Attack Behaviours](01-combat.md): `KickAction`, `AttackBehaviour`, `UFOAttackBehaviour`.
- [C32.2 — Health & Damage](02-health-damage.md): hit points, `DamageCondition`, respawn.
- [C32.3 — Coins & the Economy](03-coins-economy.md): `CoinManager`, spending, `tInventory`.
- [C32.4 — Collectibles & Collector Cards](04-collectibles-cards.md): the card system and the gallery.
- [C32.5 — Rewards & Purchases](05-rewards-purchases.md): `RewardsManager`, buying, unlocks.

---

## 32.1 Combat: the kick & attack behaviours (✅ verified)

On foot, the player's offense is a **kick**, and some enemies attack back:

```
KickAction          (0x0061647C)  — the player's kick attack (the "kickwave" char states, C8)
AttackBehaviour     (0x00615A30)  — an enemy's attack behaviour
UFOAttackBehaviour  (0x006156F0)  — the UFO/alien enemy attack
```

`KickAction` is the player's melee — the kick that smashes objects, gags (C14.4), and enemies. The
verified `*_kickwave` character states (C8, e.g. `homer_kickwave`) are the kick's animation/effect. Enemies
use `AttackBehaviour` (and the alien `UFOAttackBehaviour`) to attack the player. Combat is deliberately
light — this is a comedy game, not a fighter. [C32.1](01-combat.md).

## 32.2 Health & damage (✅ verified)

Health is **hit points** per object (vehicles via `SetHitPoints`, C15.5; characters similarly), tracked
against damage:

```
DamageCondition : MissionCondition   (0x006113CC)  — the "damage" mission condition (C16.4)
NoDamageBonusObjective : BonusObjective (0x0061190C)  — reward for taking no damage
```

The `damage` mission condition (C16.4, 117 uses) fails a stage when the tracked object takes too much damage;
`NoDamageBonusObjective` rewards a flawless run. There's no separate "Health" class — health *is* hit points,
which is why the same `SetHitPoints` (C15) governs both a car's durability and combat. [C32.2](02-health-damage.md).

## 32.3 Coins & the economy (✅ verified)

**Coins** are the currency, managed centrally and held in an inventory:

```
CoinManager   (0x006077E0)  — tracks the player's coins
tInventory    (0x005F874C)  — the generic inventory container
HudCoinCollected (0x0060DC3C)  — the "coin +N" HUD feedback
CoinObjective (0x006117A0)  — a "collect N coins" objective (C16.3)
```

You collect coins from gags (C14.4), smashing objects, and mission rewards; `CoinManager` tallies them; and
you spend them on cars and costumes (`forsale` rewards, C16.6). [C32.3](03-coins-economy.md).

## 32.4 Collectibles & collector cards (✅ verified)

Beyond coins, SHAR is a **collect-a-thon** with a signature **collector card** system:

```
CardsDB (0x00614B98) / CardGallery (0x00614BA8)  — the card database and gallery
CollectorCard (0x00614B8C) / BonusCard (0x00614BE0)  — the cards themselves
CGuiScreenCardGallery / CGuiScreenViewCards  — the UI to view them (C21)
CollectibleObjective / StatePropCollectible / PickupItemObjective  — collect objectives (C16.3)
ActionButton::CollectibleCard / CollectibleFood / RespawnCollectible  — pickup types
```

Each level hides **collector cards**; gathering them fills the `CardsDB`, viewable in the `CardGallery`
(a Simpsons trading-card gag). [C32.4](04-collectibles-cards.md).

## 32.5 Rewards & purchases (✅ verified)

Everything you collect feeds the **reward economy**:

```
RewardsManager (0x006111EC)  — grants/tracks unlocks (C16.6)
ActionButton::PurchaseReward (0x0061760C)  — buying a reward with coins
IGuiScreenRewards / CGuiScreenPurchaseRewards  — the purchase UI (C21)
```

Coins (C32.3) and completed objectives (C16) unlock cars, costumes, and cards through `RewardsManager`,
purchased at shops (`dollar` map icons, C29.3). [C32.5](05-rewards-purchases.md).

---

## Key takeaways

- **Combat** is a **kick** (`KickAction`, the `*_kickwave` states) vs. enemies with `AttackBehaviour` /
  `UFOAttackBehaviour` — deliberately light.
- **Health = hit points** (C15) with `DamageCondition` (C16.4) and a `NoDamageBonusObjective` — no separate
  health class.
- The **economy** is coins (`CoinManager`) held in `tInventory`, plus a **collector-card** system
  (`CardsDB`/`CardGallery`) and **items** (`PickupItemObjective`).
- Everything spends through **`RewardsManager`** (C16.6) — cars, costumes, cards.
- All classes ✅ verified with ✅ vtable addresses; member offsets ⏳.

**Next:** the [Legend](../Legend/README.md) — the exhaustive categorized index of the whole game.
