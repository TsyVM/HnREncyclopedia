# C50.2 — Coins

> The currency: where coins come from, who counts them, and what they look like.

## The source (✅ verified)
Coins drop when you **smash things** — gags (a gag can carry a coin reward via `GagSetCoins`, C41.4),
destructible props and crates (C32), and traffic/objects during mayhem. They also come from mission
rewards. The player drives/walks over them to collect.

## The counter (✅ verified)
`CoinManager` (`0x006077E0`) is the manager (C49) that tracks the coin balance and manages the coin
pickups in the world. Spending (at purchase centres, C50.3; repair, C50.6) deducts from it; the
balance persists via the character sheet (C27).

## The model (✅ verified)
The coin pickup's 3D model is set once per level in init: `SetCoinDrawable("coinShape_000")`
(C44.3). That's why coins look consistent across a level and can be reskinned by changing that
drawable.

## Why coins as the single currency
One universal currency (coins) keeps the economy simple and legible: everything you smash pays into
the same pot, and everything you buy draws from it. No exchange rates, no multiple currencies — very
appropriate for the game's audience.

## Bend it
- Change coin values on gags (`GagSetCoins`, C41.4).
- Reskin the coin (`SetCoinDrawable`, C44).
- Hook `CoinManager` (C49.5) to alter the balance (trainer; single-player only).

## Cross-references
C32 (destructibles that drop coins), C41.4 (`GagSetCoins`), C44 (coin model in init), C49
(`CoinManager`), C27 (persisting the balance).
