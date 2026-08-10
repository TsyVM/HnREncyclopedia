# C23.2 — The DSG Spine: `tRefCounted → IEntityDSG`

**What it is.** The base hierarchy that nearly every object in the world sits on — the "Drawable Scene
Graph" spine. Understanding it once explains the shape of `Vehicle`, `Character`, collision, fences, and
static props all at once, because they are all leaves on the same tree.

**How it works (✅ verified from RTTI).** The spine, with the derived-count each base carries:

```
tRefCounted            (386 derived)   — reference-counted lifetime (RadCore)
  └ tEntity                            — a named engine object
      └ tDrawable      (50 derived)    — something that can be drawn
          └ IEntityDSG (32 derived)    — a scene-graph entity (C10)
              ├ StaticEntityDSG
              │   └ InstStatEntityDSG              — instanced static props (C10/C12)
              ├ CollisionEntityDSG (15 derived)    — solid geometry (C11)
              │   ├ AnimCollisionEntityDSG         — animated collision (doors, lifts)
              │   └ FenceEntityDSG                 — the fences of C13
              └ DynaPhysDSG (10 derived)           — dynamic physical objects
                  ├ Vehicle
                  ├ Character
                  └ GagDrawable                    — interactive gags (C14.4)
```

Every arrow is a verified `(base)` relation in `shar_dumps.csv`. Read top-down it says: everything is
refcounted (`tRefCounted`, 386 classes), most world things are drawable (`tDrawable`, 50), and the ones
placed in the scene graph are DSG entities (`IEntityDSG`, 32).

**The key structural fact.** `Vehicle` and `Character` inherit the **identical** base set — `DynaPhysDSG,
StaticPhysDSG, CollisionEntityDSG, IEntityDSG`. A car and a pedestrian are, to the engine, the *same kind of
thing*: a dynamic, physical, collidable, drawable scene entity. This is why the scene graph (C10), collision
(C11), and physics (C26) can treat them uniformly — they share the whole spine and differ only in their
leaf class. It also explains gameplay: a character and a car collide, get pushed, and are drawn by one set
of systems because they *are* one type family.

**Why one deep spine.** A single-rooted, refcounted hierarchy is the classic 2003-era C++ engine design: a
common base gives every object lifetime management (`tRefCounted`), identity (`tEntity`), rendering
(`tDrawable`), and scene placement (`IEntityDSG`) for free, so a new object type is a small leaf that
inherits all of it. The depth (five-plus levels) is what lets the engine write one renderer, one collision
system, and one physics loop that operate on the base classes and work for every leaf. The cost — deep
inheritance and multiple base sub-objects — is exactly what the RTTI records, which is why the spine is so
cleanly recoverable.

**What happens if you bend it.**

- *Assume `Vehicle` and `Character` are unrelated* — they share the whole DSG/phys base; systems that act on
  one act on both. Use the shared base to reason about both.
- *Rely on a spine member offset* — the *inheritance* and base sub-object offsets are ✅, but a specific data
  member (a car's speed) is ⏳. Diff for it.
- *Ignore refcounting when modding lifetime* — 386 classes are `tRefCounted`; releasing or holding a
  reference wrongly corrupts lifetime. Respect the refcount model.
