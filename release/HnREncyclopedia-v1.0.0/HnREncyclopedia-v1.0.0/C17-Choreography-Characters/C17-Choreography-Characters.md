# Chapter 17 — Choreography & Characters

> **Goal of this chapter:** decode the runtime of character performance — the `choreo::` engine that turns
> the `.cho` rig files (C8) into live, animated, IK-solved characters, and the NIS system that stages
> in-engine cutscenes. This closes the character arc from data (C8) through runtime (C25) to performance.

Chapter 8 decoded the `.cho` files (rigs, animation-state maps); Chapter 25 decoded the `Character`/
`CharacterAi` runtime. This chapter is the layer between them: the **`choreo::` engine** (46 verified
classes) that actually poses, blends, and IK-solves characters, and the **NIS** cutscene system that
choreographs them for scripted scenes. Every class below is ✅ from the RTTI set.

**Key finding (✅ verified):** `choreo::` is a full **animation engine** — `Rig`/`RigLeg` (the runtime rig,
C8.1), `Puppet` (a driven character), `Animation`/`Blend`/`Transition` (the clip/blend system), body
**`Partition`s** (upper/lower-body separation), foot IK (`FootBlender`), and a `ScriptReader` that reads the
`.cho` files. **NIS** (`NISPlayer`/`NISEvent`/`CameraPlayer`) stages in-engine cutscenes (distinct from the
Bink FMV of C20), backed by `nis.rcf` (88 MB).

---

## Deep-dive pages

- [C17.1 — The `.cho` Runtime: Rig & Puppet](01-cho-runtime.md): `choreo::ScriptReader`, `Rig`, `RigLeg`, `Puppet`.
- [C17.2 — The Animation Engine: Banks, Blends & Transitions](02-animation-engine.md): clips, blending, state transitions.
- [C17.3 — Body Partitions & Foot IK](03-partitions-ik.md): upper/lower-body separation and foot planting.
- [C17.4 — NIS: In-Engine Cutscenes](04-nis-cutscenes.md): `NISPlayer`/`NISEvent`/`CameraPlayer` and `nis.rcf`.
- [C17.5 — A Character End-to-End](05-character-end-to-end.md): model + skin + rig + choreo + AI, assembled.

---

## 17.1 The `.cho` runtime: rig & puppet (✅ verified)

The `.cho` rig files (C8.1) are read at runtime by `choreo::ScriptReader`/`StringFileReader` into the live
choreography objects:

```
choreo::Rig : tEntity          — the runtime skeleton rig (the .cho `rig` block, C8.1)
  choreo::RigLeg               — a leg's IK chain (the .cho `leg` blocks, C8.1)
choreo::Puppet : tEntity       — a character driven by choreography ("puppet")
choreo::ScriptReader           — reads the .cho script
```

A **`Puppet`** is a character under choreographic control; its **`Rig`** (and `RigLeg`s) is the runtime form
of the `.cho` skeleton and IK definition (C8.1). So the text rig you decoded becomes these objects.
[C17.1](01-cho-runtime.md).

## 17.2 The animation engine: banks, blends & transitions (✅ verified)

Animation is a full clip/blend system:

```
choreo::Bank / MultiBank       — collections of animation clips (the states→clips of C8.2)
choreo::Animation / AnimationDriver / AnimationFrame   — a playing clip
choreo::Blend / BlendDriver / BlendSlot / BlendPhase   — blending between clips
choreo::Transition : choreo::Animation                 — a transition (the C8.2 state changes)
choreo::Engine                 — the choreography engine that runs it all
```

Clips live in **banks**; the engine **blends** between them and plays **transitions** — the runtime of the
`.cho` state→clip map (C8.2). [C17.2](02-animation-engine.md).

## 17.3 Body partitions & foot IK (✅ verified)

Characters animate different body parts independently and plant their feet:

```
choreo::Partition (Complete / Exclusive / Inclusive / Intersect / Union)   — body-part sets
choreo::JointBlender / RootBlender / FootBlender : poser::PoseDriver        — pose drivers
choreo::AnimationFootDriver / BlendFootDriver / RigLeg                      — foot IK / planting
```

**Partitions** let the upper body do one thing (wave) while the lower body does another (walk); **foot IK**
(the `.cho` foot-plant channels, C8.1) keeps feet on the ground. [C17.3](03-partitions-ik.md).

## 17.4 NIS: in-engine cutscenes (✅ verified)

Scripted character scenes are **NIS** (Non-Interactive Sequences) — real-time in-engine cutscenes, *distinct*
from the pre-rendered Bink FMV (C20):

```
NISPlayer / NISPlayerGroup     — plays a cutscene
NISEvent                       — a timeline event within a cutscene
CameraPlayer : SimpleAnimationPlayer   — the scripted camera (C26.3)
NISSoundPlayer                 — the cutscene's audio (C19.2)
ChoreoFileHandler              — loads .cho choreography
```

An NIS choreographs `choreo::` puppets, a `CameraPlayer` camera, and `NISSoundPlayer` audio along a
`NISEvent` timeline. The data is in `nis.rcf` (88 MB). [C17.4](04-nis-cutscenes.md).

## 17.5 A character end-to-end (✅ verified)

A full character assembles: a **model** (C7) + **skin** (C8.3) + **skeleton** + a **`.cho` rig** (C8.1) run
by **`choreo::`** (here) + a **`CharacterAi`** (C25.2) + a **controller** (C25.3). [C17.5](05-character-end-to-end.md).

---

## Key takeaways

- `choreo::` (46 classes) is a full **character-animation engine**: `Rig`/`RigLeg`/`Puppet` (runtime of the
  `.cho` rig, C8.1), `Bank`/`Animation`/`Blend`/`Transition` (runtime of the state→clip map, C8.2), body
  `Partition`s, and foot IK — read from `.cho` by `choreo::ScriptReader`.
- **Partitions** animate body parts independently; **foot IK** (`FootBlender`, `RigLeg`) plants feet.
- **NIS** (`NISPlayer`/`NISEvent`/`CameraPlayer`) are **in-engine** cutscenes (≠ Bink FMV, C20), backed by
  `nis.rcf` (88 MB), staging choreo puppets + camera + audio on a timeline.
- A character is model (C7) + skin (C8.3) + rig (C8.1) + choreo (here) + AI (C25) + controller (C25.3).

**Next:** [Chapter 18 — RSD Sound Format](../C18-RSD-Sound/C18-RSD-Sound.md).
