# C32.5 — Rewards & Purchases

**What it is.** Where everything you collect and accomplish pays off — the reward system that grants unlocks
and lets you buy cars and costumes with coins. This page closes the chapter by connecting the collection
economy (C32.3–C32.4) to the reward economy (C16.6).

**How it works (✅ verified).**

```
RewardsManager (0x006111EC)  — grants and tracks unlocks
ActionButton::PurchaseReward (0x0061760C)  — buying a reward with coins
IGuiScreenRewards / CGuiScreenPurchaseRewards (C21)  — the purchase/reward UI
```

**`RewardsManager`** is the central owner of unlocks — it knows what you've earned and what's available. Two
paths grant rewards: **completion** (finishing missions, races, bonus missions binds a reward via
`BindReward`, C16.6) and **purchase** (`ActionButton::PurchaseReward` — walking up to a shop and spending
coins, C32.3, on a `forsale` reward, C16.6). The `CGuiScreenPurchaseRewards`/`IGuiScreenRewards` screens (C21)
are the buy UI, reached at the `dollar` map icons (C29.3). Rewards are cars (the vehicle roster, C24), costumes
(the `a_*`/`b_*` skins, C8/Legend), and collector cards (C32.4).

**The full reward graph.** Putting C16.6 and this page together, SHAR's progression is a graph of
earn→unlock edges owned by `RewardsManager`:

- **Story/bonus missions** (C16) → a car (`bonusmission`/`defaultcar`, C16.6).
- **Street races** (C16.5) → a car (`streetrace`).
- **Coins** (C32.3) → buy a car/costume (`forsale`, with a cost and seller).
- **Collector cards** (C32.4) → the gallery completion.

Every unlock in the game flows through this one manager, which is why the whole economy is readable in one
place (`rewards.mfk`, C16.6): the `BindReward` list *is* the reward graph, and `RewardsManager` executes it.

**Why centralise rewards.** The same reason as coins (C32.3) and every other shared resource: one owner
prevents disagreement. `RewardsManager` is the single source of "what have I unlocked," which the galleries
read, the shops check, and the vehicle/costume selectors query. Combined with `CoinManager` (C32.3) it forms
the complete economy: coins in, rewards out, both centrally managed. This is the payoff structure that makes
the collecting (C32.3–C32.4) *matter* — everything you gather converts, through these managers, into new
content to play with.

**The modding view.** The reward economy is data-editable at the script layer (C16.6): edit `rewards.mfk`'s
`BindReward` lines to change what unlocks what, add a `forsale` binding to make something purchasable, or
retune costs. The runtime managers (`RewardsManager`, `CoinManager`) are the native layer — identify them by
their verified vtables (C23.5) to read/adjust live state (offsets ⏳). So changing *what* you unlock is a data
edit; changing *how the economy behaves* live is a native mod (C28).

**What happens if you bend it.**

- *Bind a reward to missing content* — the unlock grants nothing (C16.6). Ensure the car/costume exists
  (Legend).
- *Rely on a `RewardsManager` offset or singleton* — class/vtable ✅, offset/instance ⏳. Diff (C4.3).
- *Unbalance costs vs. coin sources* — you break the economy's pacing (C32.3). Balance earn against spend.

**Next:** the [Legend](../Legend/README.md) — the exhaustive categorized index of the whole game.
