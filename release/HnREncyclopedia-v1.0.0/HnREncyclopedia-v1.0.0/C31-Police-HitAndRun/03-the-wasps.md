# C31.3 — The Wasp Cameras

**What it is.** The flying surveillance robots scattered through every level — the "wasps." They watch the
world, and they're destructible collectible targets: smashing all of a level's wasps earns a reward. They're
SHAR's nod to Springfield's surveillance-camera gags.

**How it works (✅ verified).**

```
ActorAnimationWasp : ActorAnimation   (0x00615D0C)  — the wasp actor and its animation
WaspSoundPlayer : ActorPlayer         (0x00608D94)  — the wasp's hovering/buzzing sound
HudWaspDestroyed : HudEventHandler    (0x0060DB40)  — HUD feedback when you destroy one
```

A wasp is an **actor** (`ActorAnimationWasp`) — a small animated flying camera-robot that hovers at fixed
points in the level. `WaspSoundPlayer` gives it its buzzing sound (positional, C19.2). When you destroy one
(by hitting it, usually with a car or a thrown object), `HudWaspDestroyed` fires the "wasp destroyed" HUD
feedback and increments the level's wasp count. Collect all of a level's wasps for a reward (C16.6). On the
map they're marked (the `harascar`/surveillance-style icons, C29.3).

**Why wasps exist.** Two reasons, one thematic and one design. **Thematically**, they're a Simpsons gag —
Springfield's ubiquitous surveillance, rendered as absurd flying camera-bugs. **In design terms**, they're a
*collection challenge* — a set of hidden/placed targets per level that reward exploration, exactly like the
collectible cards and the gags (C14.4). SHAR is built on collection loops (coins, cards, wasps, gags), and
the wasps are the "destroy these scattered targets" variant. Making them **actors** (`ActorAnimation`) rather
than static props means they can hover and animate (harder to hit than a static object), adding a small skill
element to the collection.

**Actors vs. entities.** A wasp is an `ActorAnimation` — part of the actor system (the `Actor*`/
`ActorAnimation*` classes), which handles scripted animated objects distinct from the DSG world entities
(C23.2) and the choreographed characters (C17). Actors are the game's layer for *animated set-dressing and
targets* — things that move on scripted animation but aren't full characters. The wasps, some gag objects,
and scripted animated props are actors. This is a lighter-weight system than the full character choreography
(C17) — a wasp doesn't need a skeleton and IK, just a hover animation and a sound — so the actor system
gives it exactly that and no more.

**What happens if you bend it.**

- *Rely on a wasp/actor member offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Move a wasp without its anchor* — like locator-based content (C8.4), wasps are placed in the level; move
  the placement, not just the model.
- *Confuse wasps with the police* — wasps are surveillance *targets* (destroy for reward); the police are the
  *pursuit* (C31.2). Different systems, different classes.
