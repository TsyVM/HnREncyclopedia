# C32.3 — Coins & the Economy

**What it is.** The game's currency system — **coins** — and the inventory that holds them. Coins are what
you collect everywhere and spend on cars and costumes; they're the connective tissue of SHAR's
collect-and-unlock loop.

**How it works (✅ verified).**

```
CoinManager      (0x006077E0)  — the singleton that tracks the player's coins
tInventory       (0x005F874C)  — the generic inventory container
HudCoinCollected (0x0060DC3C)  — the "+N coins" HUD feedback
CoinObjective    (0x006117A0)  — a "collect N coins" mission objective (C16.3, the `coins` type)
```

You earn coins from **gags** (`GagSetCoins`, C14.4), smashing objects and property, mission rewards, and
races. **`CoinManager`** is the central tally — a singleton (like `VehicleCentral`, C24.3) that owns your
coin count. When you pick coins up, **`HudCoinCollected`** shows the gain. The `coins` objective (C16.3,
`CoinObjective`) is a mission goal to collect a number of them. And **`tInventory`** is the generic inventory
container that holds what you carry — coins and any mission items (C32.4).

**Why a central coin manager.** Coins are earned and spent all over the game — every gag, every shop, every
reward references them — so a single `CoinManager` owning the count is the clean design: one source of truth
for "how many coins do I have," which the HUD reads, the shops check, and missions query. Scattering the coin
count would risk it disagreeing with itself. This is the same manager-singleton pattern as vehicles
(`VehicleCentral`, C24.3), characters (`CharacterManager`, C25.3), and cameras (`SuperCamCentral`, C26.4) —
SHAR centralises every shared resource in one manager. The coin count is a shared resource; `CoinManager`
owns it.

**`tInventory` — the generic container.** `tInventory` is a reusable inventory data structure (the `t` prefix
marks it as a low-level tool/template class, like `tDrawable`, `tEntity`). It holds a set of items — coins,
and the pickup items missions use (C32.4/C16.3 `pickupitem`). Being generic means the same container serves
any "things the player is carrying" need, rather than a bespoke structure per item type. When a mission has
you carry a "barrel" (the `keepbarrel` condition, C16.4) or an item (`pickupitem`), that's tracked through the
inventory/carry system.

**The economy loop.** Coins tie the whole game together: collect them (gags, smashing, missions) → they
accumulate in `CoinManager` → spend them on cars and costumes via `RewardsManager`/`PurchaseReward` (C32.5,
C16.6) at shops (`dollar` icons, C29.3). This collect-and-spend loop, alongside the mission progression
(C16), is SHAR's core reward structure. It's why coins appear in so many systems — they're the currency that
connects collecting to unlocking.

**What happens if you bend it.**

- *Rely on the `CoinManager` singleton address or a member offset* — class/vtable ✅, offset and instance
  pointer ⏳. Diff (C4.3).
- *Add coin sources without balancing shops* — you inflate the economy (C16.6). Balance earn against spend.
- *Assume a separate money type* — it's coins, one currency, one `CoinManager`. Model it as such.
