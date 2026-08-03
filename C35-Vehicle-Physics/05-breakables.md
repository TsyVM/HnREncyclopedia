# C35.5 — Breakables & Destruction

**What it is.** The system behind smashing through glass, fences, and props — **`BreakableObjectDSG`** and its
manager. When a car (or a kick, C32.1) hits a breakable, it breaks, spawning debris and often a camera shake
(C36). It's what makes the world feel destructible.

**How it works (✅ verified).**

```
BreakableObjectDSG (0x0060C664)  — a destructible object in the scene graph (C10)
BreakableObjectLoader (0x0060B85C)  — loads breakables from Pure3D chunks
BreakablesManager (0x0060B758)   — owns/tracks the breakables in a level
```

A **`BreakableObjectDSG`** is a scene-graph entity (a DSG, C23.2) that can be *destroyed*. Storefront glass,
fences (C13.1 as art), crates, signs, and destructible props are breakables. When something hits one with
enough force — a car driving through a window, a kick (C32.1), an explosion — it **breaks**: the intact object
is removed and replaced with a broken version and/or **debris** (particle effects, C33.4 — shards of glass,
splinters of wood), plus a sound (C19) and usually a **camera shake** (`SineCosShaker`, C36). The
**`BreakablesManager`** owns the level's breakables, so it can reset them (some respawn) and budget them.

**Why breakables are their own entity type.** Most of the world is static scenery (C10) that never changes.
A breakable is scenery that has a *destroyed state* — so it needs extra data (what it looks like broken, what
debris it spawns) and logic (detect the impact, switch to broken). Making it a distinct `BreakableObjectDSG`
(rather than tagging every object) keeps the common static case cheap and gives breakables exactly the extra
machinery they need. The `BreakablesManager` centralises them so the game can manage the *set* — reset them
on mission restart, track how many you've smashed (some missions or gags, C14.4, count destruction), and
budget the debris. This is the same "special entity type + manager" pattern as collision (C11), vehicles
(C24.3), and characters (C25.3).

**Smashing through glass — the moment.** Driving through a storefront window is a designed set-piece: the
glass `BreakableObjectDSG` detects the car's impact (a collision, C26.6), breaks into shard debris (a glass-
particle effect, C33.4), plays a shatter sound (C19), and shakes the camera (`SineCosShaker`, C36) — all
triggered by the one break event. This multi-modal feedback (visual debris + audio + camera + haptic rumble,
C33.5) from a single event is the event-driven effect design (C33.5) at work: the break fires effects across
modalities. It's why crashing through glass is so satisfying — the game throws everything at the moment.

**Breakables vs. gags vs. collision.** Three related but distinct systems: a **breakable** (`BreakableObjectDSG`)
is destructible scenery; a **gag** (C14.4) is a scripted interactive joke (which *may* involve breaking
something); **collision** (C11) is what makes any object solid. A window is a breakable (it shatters) that's
also collidable (you hit it before it breaks). A scripted exploding set-piece is a gag that triggers
breakables. Knowing which system owns a behaviour tells you where to edit it: destructibility → the breakable,
the joke → the gag, solidity → collision.

**What happens if you bend it.**

- *Rely on a `BreakableObjectDSG`/`BreakablesManager` member offset* — classes/vtables ✅, offsets ⏳. Diff
  (C4.3).
- *Make static scenery breakable expecting it to just work* — it needs the breakable data (broken model,
  debris) the loader expects. Author it as a breakable.
- *Confuse a breakable with a gag* — destructibility is `BreakableObjectDSG`; a scripted joke is a gag
  (C14.4). Edit the right system.

**Next:** [Chapter 36 — Cameras & Camera Effects](../C36-Cameras-Effects/C36-Cameras-Effects.md).
