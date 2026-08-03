# C17.3 — Body Partitions & Foot IK

**What it is.** Two refinements that make character motion look right: **partitions** (animating different
body parts independently — wave while walking) and **foot IK** (planting feet on the ground so they don't
slide or float). Both are verified `choreo::` subsystems, and both trace back to the `.cho` rig (C8.1).

**Body partitions (✅ verified).** A **partition** is a set of the rig's joints that can be driven
independently. The verified partition classes:

```
choreo::Partition : tEntity
  ├ choreo::CompletePartition    — the whole body
  ├ choreo::ExclusivePartition   — a set that excludes others
  ├ choreo::InclusivePartition   — a set that includes others
  ├ choreo::IntersectPartition   — the overlap of sets
  └ choreo::UnionPartition       — the union of sets
```

Partitions let the engine drive the **upper body** with one animation (an arm gesture, holding an object)
and the **lower body** with another (walking, standing) *at the same time*. The set operations
(Exclusive/Inclusive/Intersect/Union) are how the engine composes these regions — e.g. "upper body =
everything *except* the legs" is an `ExclusivePartition`. This is why a character can walk and wave
simultaneously: the walk drives the lower-body partition, the wave the upper, and the engine combines them.

**Foot IK (✅ verified).** Feet need to *plant* on the ground — stay fixed while the body moves over them,
and adapt to slopes and steps — or they visibly slide and float. The verified foot-IK classes:

```
choreo::FootBlender : poser::PoseDriver
choreo::AnimationFootDriver / BlendFootDriver : choreo::FootBlendDriver
choreo::RigLeg                                  — the leg's IK chain (C17.1, from the .cho, C8.1)
choreo::BlendSlotFootInfo                        — per-blend foot data
```

This is the runtime of the `.cho` **foot-plant channels** (C8.1): the rig declares which channel signals a
foot is planted, and the `FootBlender`/`AnimationFootDriver` solve the `RigLeg`'s IK (thigh→knee→ankle) so
the ankle meets the ground surface. On a kerb or slope, the IK adjusts the leg so the foot lands correctly
instead of clipping into or floating above the ground.

**Why these matter for a cartoon game.** SHAR's characters have exaggerated proportions and walk over a
detailed 3-D world (kerbs, stairs, slopes, C12). Without foot IK they'd moonwalk and float; without
partitions they'd have to animate every combination of upper/lower actions as a separate clip. Both
subsystems are what make the characters feel grounded and expressive despite the cartoon style — and both are
*configured* by the `.cho` rig (C8.1) and *run* by these `choreo::` drivers. The `poser::PoseDriver` base
(the `poser::` namespace) is the low-level joint-posing layer they build on.

**What happens if you bend it.**

- *Break the `.cho` foot-plant channel* (C8.1) — feet stop planting and slide. Keep the channel definition
  intact.
- *Partition the wrong joints* — an arm gesture bleeds into the legs, or vice versa. Define partitions along
  the intended body regions.
- *Rely on a `choreo::`/`poser::` member offset* — classes ✅, offsets ⏳. Diff (C4.3).
