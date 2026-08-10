# C16.5 — Showdowns & Bonus Missions

**What it is.** The two kinds of mission beyond the story chain: the **showdown** (each level's boss
finale) and the **bonus** content (street races, gag races, bonus missions). Together they are the game's
climaxes and its optional challenges.

**Showdowns (✅ verified).** A story mission with a boss finale gets a `m{N}sd` pair — `m{N}sdi.mfk`
(showdown logic) and `m{N}sdl.mfk` (showdown load). Verified: `m0sdi.mfk` opens `SelectMission("m0sd")` and
runs stages like `talkto` → `dialogue` leading into the confrontation. The finale itself uses the
**`destroyboss`** objective (C16.3) — used exactly **4 times** across the game, one per level boss. So the
showdowns are where the level's antagonist is defeated, scripted as their own missions so the finale can be
balanced independently of the mission that leads to it.

**Street races (✅ verified).** Every level's roster (C16.1) includes **`sr1`, `sr2`, `sr3`** — three street
races, documented in the level scripts as a **time trial**, a **circuit race**, and a **waypoint race**.
These use the `race` objective (C16.3, 44 uses) and `race` condition (C16.4), route the player over the road
graph and path segments (C13), and reward a car on completion (C16.6).

**Bonus & gag missions (✅ verified).** `gr1` (a gag race) and `bm1` (a bonus mission) round out each level's
five bonus entries, with level-specific extras like Level 3's **`ismovie`** (an Itchy & Scratchy movie
tie-in). Bonus missions are full missions using the same stage/objective/condition machinery (C16.2–C16.4);
they're "bonus" only in that they're optional and off the main story chain.

**Why separate showdowns and bonus from story missions.** Three reasons, all about *independence*. A
showdown is a difficulty spike that wants its own tuning, so it's its own file. Bonus content is optional, so
it's listed separately (`AddBonusMission`, C12.4) and gated differently. And races use a distinct objective/
condition pair (`race`) with their own runner. Keeping these as separate mission entries — rather than
branches inside story missions — means each can be added, removed, or rebalanced without touching the story
chain, and the level roster (C16.1) reads as a clean list of story + bonus.

**The full level challenge set.** Putting C16.1 and this page together: a level offers **7–8 story missions**
(each possibly with a showdown), **3 street races**, a **gag race**, and a **bonus mission** — roughly a
dozen distinct challenges per level, all built from the same 20 objectives and 7 conditions. That reuse is
how a game this large was authored: a small vocabulary, recombined across ~90 missions.

**What happens if you bend it.**

- *Give a boss finale a normal objective instead of `destroyboss`* — the finale won't register as beating the
  boss. Use `destroyboss` for level bosses.
- *List a bonus mission with `AddMission` instead of `AddBonusMission`* — it enters the story chain instead of
  the optional set (C12.4). Use the right roster call.
- *Rebalance a showdown inside the story mission file* — you couple the finale to the run-up. Keep showdowns
  in their `m{N}sd` files.
