# C39.6 — Exceeding Limits Safely

> A method for pushing SHAR's ceilings without the crash-and-guess cycle: measure first, raise the right lever
> for the tier, watch the master ceiling, and test in small steps — with an in-game menu to make it practical.

## The method

```
1. MEASURE   run SAHRDiag (C28.7) → live populations vs caps: how close am I, to which limit?
2. CLASSIFY  which tier is the limit? (C39.1)  script / pool / hard
3. RAISE     use that tier's lever:  edit script (C39.2) | enlarge pool (C39.3) | avoid (hard)
4. BUDGET    watch the static heap (C39.3): every pool byte is spent from one shared reserve
5. FEED      complete the content pipeline (C39.4) so the new headroom is actually filled & drawn
6. TEST      small increments; re-measure; confirm no "full/too many" strings fire
```

The single biggest mistake is skipping step 1 — raising a number blind. SAHRDiag turns "I think I'm near a
limit" into "I have 1000/1000 particles and 336 collision objects," which tells you *exactly* which lever to
pull.

## Match the lever to the tier (don't cross them)

- **Script limit** → edit the script (C39.2). Never patch code for something a number would fix.
- **Pool limit** → enlarge the pool at init (C39.3). Don't try to script past a pool cap — the script check
  isn't the ceiling, the pool is.
- **Hard limit** → respect it. The PC-count and locomotion-animation limits (C39.1) are *"not supported right
  now"* for a reason; exceeding them is deep, risky patching with poor payoff. Design around them instead.

## Watch the master ceiling

Every enlarge spends **static heap** (C39.3). The alarm is explicit — *"Static heap full - requested:%d
available:%d overflow:%d"* — but by then the game is failing. Stay ahead of it: enlarge modestly, re-measure
resident memory, and reclaim heap (drop an unused mode/asset) before adding more. Treat the heap as a fixed
budget you're reallocating, not a wall to lean on.

## What "breaking the game" looks like (and the tier behind it)

| Symptom | Likely cause | Tier |
|---|---|---|
| New spawns silently don't appear | pool full (particles/sounds/model slots) | 2 |
| Hard crash on load with a heap message | static heap exhausted | 3 |
| Instant crash adding a playable character | PC hard limit | 3 |
| Content loads but is invisible | scenegraph/render step missing (C39.4) | — |
| Traffic count won't rise despite `SetMaxTraffic` | pipeline step missing, or pool/path bound | 1→2 |
| Character T-poses / won't move | locomotion animation limit or missing anim | 3 |

Reading the symptom back to a tier is half the debugging.

## A limits/debug menu (ties to C38)

Tuning by edit-and-relaunch is slow. Build a small **debug menu** with the menu-extension techniques (C38):

- live readouts of key pool populations (particles, sounds, collision objects) from the same data SAHRDiag
  reads,
- sliders/toggles for the pool multipliers you hooked (C39.3),
- a "spawn N test objects" action to find the cap interactively.

Now you can walk a level, watch a counter climb toward its cap, and feel exactly where the ceiling is — the
fastest way to tune limits honestly.

## Discipline

- **Measure, don't guess** (SAHRDiag).
- **Right lever for the tier** — never patch what a script sets, never script past a pool.
- **Budget the static heap** — enlarging is zero-sum.
- **Increment and re-test** — small steps, re-measure each time.
- **Respect hard limits** — design around Tier 3, don't brute-force it.
- Single-player, offline, on a copy you own (C28.6).

## Cross-references

- **C28.7 — SAHRDiag**: the measurement tool this method is built on.
- **C39.1–C39.5** — the tiers, levers, pipeline, and specific sound/effect caps.
- **C38** — building the debug/limits menu.
