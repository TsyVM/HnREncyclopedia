# C24.1 — The `Vehicle` Class

**What it is.** The runtime type of every car in the game. A `Vehicle` is not a special standalone object —
it is a leaf on the DSG spine (C23.2) that adds vehicle behaviour to the same base every world entity shares.

**How it works (✅ verified).** From `shar_dumps.csv`:

```
Vehicle : DynaPhysDSG, StaticPhysDSG, CollisionEntityDSG, IEntityDSG, tDrawable, tEntity, tRefCounted, …
```

Read the bases and you have the car's whole nature:

- **`IEntityDSG` / `tDrawable`** — it lives in the scene graph (C10) and is drawn each frame.
- **`CollisionEntityDSG`** — it is solid; it collides with the world and other entities (C11).
- **`DynaPhysDSG`** — it is *dynamically* simulated: physics moves it (C26), unlike static scenery.
- **`StaticPhysDSG`** — it also participates as a physics body others can rest/collide against.
- **`tRefCounted`** — its lifetime is reference-counted (C23.2).

So a `Vehicle` *is* a physical scene entity, plus the vehicle-specific state (wheels, engine, handling) that
the `.con` configures (C24.4) and the controller drives (C24.2). Nothing about being a car replaces the base
machinery — it extends it.

**Why build a car this way.** Inheriting the full DSG/physics spine means a car gets rendering, collision,
and physics for free and behaves consistently with everything else in the world — it can be hit by another
car, rest on the ground, be drawn and culled — all through systems that don't know or care it's a car.
The car-specific part (the handling model) is then a thin specialisation on top. This is the payoff of the
deep hierarchy (C23.2): a new physical object type is mostly inherited, and `Vehicle` is exactly that plus a
handling model.

**The tie to the mesh and collision.** A `Vehicle`'s *appearance* is its mesh (C7, referenced through the
scene graph, C10); its *solidity* is its collision (C11); its *motion* is physics (C26). The runtime object
binds these: it is drawn as its mesh, collides as its collision entity, and moves as its physics body. The
`.con` (C15) tunes how the physics body behaves (mass, grip, suspension), which is the subject of C24.4.

**What happens if you bend it.**

- *Treat `Vehicle` as unrelated to scenery/characters* — it shares their base; systems that act on
  `IEntityDSG`/`CollisionEntityDSG` act on cars too. Reason from the shared spine.
- *Rely on a `Vehicle` member offset* — the class and its bases are ✅, but a specific member (speed, wheel
  angle) is ⏳. Diff for it (C4.3).
- *Assume the mesh and the vehicle are one object* — the mesh is referenced through the scene graph; the
  `Vehicle` is the physical entity that uses it. Edit the right one for the effect you want.
