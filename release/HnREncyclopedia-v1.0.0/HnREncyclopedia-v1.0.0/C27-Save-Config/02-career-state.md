# C27.2 — Career State: Missions, Cars & Coins

**What it is.** What the save actually *records* — the player's progress: which missions they've completed,
which cars they've unlocked, how many coins and cards they have, and where they are in the world. These are
the record arrays and numeric fields inside `Save1` (C27.1).

**How it works (✅ verified structure).** The save persists the reward economy (C16.6/C32) as records:

- **Mission completion** (32-byte-stride array @409) — records naming completed missions. Verified content:
  the bonus missions `sr1`, `sr2`, `sr3` (street races), `bm1` (bonus mission), `gr1` (gag race) — the level's
  bonus roster (C16.5). Each record marks a mission done. The story missions' completion (m0–m8, C16) is
  tracked in the numeric progress region (a bitfield/counter per level).
- **Unlocked cars & rewards** (24-byte-stride array @4397) — records naming unlocked content. Verified:
  `famil_v` (the family car — the level-1 default reward, C16.6) is present; every other slot reads `n/a`
  (not yet unlocked). This array *is* the persistent form of the reward graph (C16.6): as you earn cars and
  costumes via `RewardsManager` (C32.5), their names fill these slots.
- **Coins** (numeric region) — the `CoinManager` (C32.3) total, persisted so your money survives a reload.
- **Collector cards** (numeric region) — which of the `CardsDB` (C32.4) cards you've found.
- **Current level & position** (numeric region) — where you are, so a load drops you back in place.

The exact byte layout of the numeric fields is 🟡 (readable as numbers, but each field's meaning needs a
save-diff to pin — change one thing in-game, re-save, diff, C4.3); the **record arrays are ✅** (their
strides and string contents are verified).

**Why persist the reward economy this way.** The save's job is to make the reward economy (C16.6, C32)
*durable* — everything you earn must survive turning the game off. Mirroring the economy's structure (missions
→ rewards → cars/cards/coins) as save records means the save *is* the economy's memory: the mission records
say what you've done, the reward records say what you've unlocked, the numeric fields say what you hold. On
load, the game reads these back and reconstructs your state — `RewardsManager` (C32.5) knows what's unlocked
because the save told it, `CoinManager` (C32.3) knows your coins, the mission system (C16) knows your
progress. The save is the bridge between sessions.

**Reading a player's progress.** From `Save1` you can reconstruct the whole career: the mission array shows
which bonus content is beaten, the reward array shows the garage (which cars unlocked), and the numeric fields
show coins and story progress. A fresh save (like this one — only `famil_v` unlocked, missions mostly empty)
reads as "early game"; a complete save would have full mission and reward arrays. This makes the save a
readable snapshot of exactly how far a player has gotten.

**What happens if you bend it.**

- *Add a reward name to a slot without the right record format* — the game may not recognise the unlock. Match
  the 24-byte record layout (C27.1).
- *Edit coins in the numeric region without confirming the field* — it's 🟡; verify by save-diffing (C4.3)
  before trusting an offset.
- *Mark a mission complete out of sequence* — you can desync story progress. The mission records and the
  numeric story-progress must agree.
