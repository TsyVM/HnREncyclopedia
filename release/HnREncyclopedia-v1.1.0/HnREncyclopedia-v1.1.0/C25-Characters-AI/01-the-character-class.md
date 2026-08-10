# C25.1 — The `Character` Class

**What it is.** The runtime type of every person in the game — player avatars, mission NPCs, ambient
pedestrians. Like `Vehicle` (C24.1), a `Character` is a leaf on the DSG spine (C23.2), not a standalone
special case.

**How it works (✅ verified).** From `shar_dumps.csv`:

```
Character : DynaPhysDSG, StaticPhysDSG, CollisionEntityDSG, IEntityDSG, tDrawable, tEntity, tRefCounted, …
```

These bases are **byte-for-byte the same set as `Vehicle`** (C24.1). So everything true of a car's *physical
nature* is true of a character's: drawn (`tDrawable`, C10), solid (`CollisionEntityDSG`, C11), dynamically
simulated (`DynaPhysDSG`, C26), refcounted (`tRefCounted`, C23.2). On top of the shared base, a `Character`
adds person-specific state — its skeleton and skin (C8.3), its animation state (C8.2), and its AI (C25.2).

**Why a person and a car share a base.** This is the most consequential structural fact in the runtime.
Because `Character` and `Vehicle` are the same *kind* of entity, the engine's collision, physics, and
rendering all operate on them uniformly:

- A car **hits** a pedestrian because both are `CollisionEntityDSG` — one collision system, both entities.
- A knocked-down character **ragdolls** through the same `DynaPhysDSG` physics that tumbles a car (the
  `CharacterAi::InSim` state, C25.2, is literally "the character is now a physics body").
- Both are **drawn and culled** by one scene-graph walk (C10).

Designing people and vehicles as one family is what makes SHAR's core loop — driving *through* a populated
world where you can also get out and walk — coherent: there's no seam between "car physics" and "character
physics," because there's one physics acting on one entity family.

**The character-specific layer.** What makes a `Character` a *person* rather than a car sits on top of the
shared base: a skeleton (C8.1) posing a skinned mesh (C8.3), an animation-state graph (C8.2) choosing clips,
and a `CharacterAi` (C25.2) deciding behaviour. The `.cho` file (C8) configures this layer, the way the
`.con` (C15) configures a vehicle's — same pattern, different domain.

**What happens if you bend it.**

- *Treat characters and vehicles as unrelated at runtime* — they share the whole physical base; collision and
  physics act on both. Reason from the shared spine (C23.2).
- *Rely on a `Character` member offset* — the class and bases are ✅, offsets ⏳. Diff (C4.3).
- *Expect editing the character mesh to change its animation* — the mesh (C7) and the rig/animation (C8) are
  separate layers. Edit the layer you mean.
