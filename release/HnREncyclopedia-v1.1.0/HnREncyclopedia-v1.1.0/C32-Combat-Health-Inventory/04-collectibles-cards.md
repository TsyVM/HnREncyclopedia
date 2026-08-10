# C32.4 — Collectibles & Collector Cards

**What it is.** SHAR's collect-a-thon layer beyond coins — the scattered collectibles and, most
distinctively, the **collector cards**: a set of Simpsons trading cards hidden across the levels, gathered
into a gallery. Collecting is a core SHAR activity, and the cards are its signature.

**How it works (✅ verified).**

```
CardsDB      (0x00614B98)  — the database of all cards and which you've found
CardGallery  (0x00614BA8)  — the gallery view of collected cards
CollectorCard(0x00614B8C) / BonusCard (0x00614BE0)  — the card objects
CGuiScreenCardGallery / CGuiScreenViewCards  — the UI screens (C21)
CollectibleObjective / StatePropCollectible / PickupItemObjective  — collect objectives (C16.3)
ActionButton::Collectible / CollectibleCard / CollectibleFood / RespawnCollectible  — pickup action types
```

Each level hides **collector cards** (`CollectorCard`) — pick one up and it's added to the **`CardsDB`**,
viewable in the **`CardGallery`** (the `CGuiScreenCardGallery`/`ViewCards` UI, C21). This is a Simpsons
trading-card gag turned into a collection meta-game spanning the whole world. Other collectibles feed
mission objectives: **`CollectibleObjective`**/**`CoinObjective`** (C16.3) for "collect N of these," and the
**`ActionButton::Collectible*`** family for the different pickup types — cards, food, respawning
collectibles — triggered by walking into them (an `ActionButton`, the context-action system).

**Why a card collection.** Collect-a-thons of the era (SHAR is contemporary with the 3-D platformer collectathon
boom) reward *exploration* with *completion sets*, and a trading-card gallery is the perfect fit for a licensed
comedy world: each card is a joke/reference, and finding them all is a completionist goal orthogonal to the
missions. Making it a **database + gallery** (`CardsDB`/`CardGallery`) means the game tracks your set across
levels and lets you admire it — the payoff is the gallery. This is content the world is *littered* with (the
`collect` map icon, C29.3, marks them), giving a reason to drive and walk every corner of Springfield beyond
the missions.

**Collectibles as objects and objectives.** A collectible is both a *world object* (an `ActionButton::Collectible`
you touch) and, when a mission needs it, an *objective* (`CollectibleObjective`, C16.3). The
`RespawnCollectible` variant re-appears after being taken (for repeatable pickups like health/coins);
`StatePropCollectible` ties a collectible to a mission's state. This dual nature — object in the world,
objective in a mission — is the same pattern as vehicles (C24.5) and characters (C25.5): a thing exists in the
world and can *also* be referenced by a mission. The collection systems and the mission systems meet at the
collectible.

**What happens if you bend it.**

- *Rely on a `CardsDB`/collectible member offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Add a collectible without placing it (a locator, C8.4)* — it has nowhere to appear. Place it in the world.
- *Confuse a repeatable pickup with a one-time card* — `RespawnCollectible` re-appears; a `CollectorCard` is
  once. Use the right type.
