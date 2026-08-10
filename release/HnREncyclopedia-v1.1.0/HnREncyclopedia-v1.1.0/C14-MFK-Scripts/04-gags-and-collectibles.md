# C14.4 — Gags & Collectibles

**What it is.** The scripting subsystem behind SHAR's interactive comedy — the "gags" scattered through
each level (the exploding stuff, the animated set-pieces) — and the collectibles the player picks up. It is
a complete verb family with its own open/close discipline, verified across the mission tree.

**The gag verbs (✅ verified counts).** A gag is defined by a balanced block and a set of setters:

```c
GagBegin("name");                 // 419 calls
  GagSetPosition(...);            // 418 — where it is
  GagSetTrigger(...);             // 414 — what sets it off
  GagSetSound(...);               // 406 — the sound to play (C19)
  GagSetCycle(...);               // 419 — its animation cycle/timing
  GagSetRandom(...);              // 418 — randomisation
  GagSetInterior(...);            // 309 — interior/exterior placement
  GagSetCoins(...);               // 181 — coins awarded
  GagSetSparkle(...);             // 99  — the visual sparkle hint
  GagSetPersist(...);             // 175 — whether it persists
GagEnd();                         // 419 — close (balanced with GagBegin)
```

`GagBegin` and `GagEnd` match exactly (419/419 — ✅), the same balanced-block invariant as stages (C14.3).
A gag is thus a self-contained definition: position, trigger, sound, animation, reward, and presentation,
all set between the brackets.

**Collectibles.**

- **`AddCollectible(...)`** (689 calls — the second most-used command in the game) — place a pickup.
- **`SetCollectibleEffect(...)`** (337) — what collecting it does (coins, powerup, mission progress).
- **`AddToCountdownSequence(...)`** (176) — collectibles/objects that participate in a timed sequence.

**Why it's built this way.** The gag system turns level comedy into *data*. Rather than hand-coding each
joke, designers describe it — "at this position, when the player does X, play this animation and this
sound, award these coins" — and a generic gag runner executes it. That is why a licensed comedy game could
ship so many set-pieces: each is a short script block, not bespoke code. The collectible system is the same
idea for pickups. Together they make the level's *interactivity* editable text, exactly like its missions.

**Reading the density.** 419 gags and 689 collectibles across the tree tell you how much of SHAR's charm is
scripted content rather than engine features — the world is dense with authored moments. For a modder, this
is the layer where you add *character* to a level: a new gag is a `GagBegin…GagEnd` block referencing an
animation (C8) and a sound (C19).

**What happens if you bend it.**

- *Unbalance `GagBegin`/`GagEnd`* — the gag definition bleeds into the next; keep them matched (419/419).
- *Point `GagSetSound` at a missing sound* — the gag fires silently; ensure the referenced sound is loaded
  (C19).
- *Omit `GagSetTrigger`* — a gag with no trigger never fires. Every gag needs its set-off condition.
