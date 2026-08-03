# Chapter 25 — Characters & AI

> **Goal of this chapter:** decode the runtime of characters and their AI — the verified `Character` class,
> the `CharacterAi` state machine, controllers, and how the `.cho` rigs and animations of C8 drive a live
> pedestrian or NPC.

Characters are the people of Springfield — the player's avatars, the mission NPCs, the ambient crowds. This
chapter reads their runtime from the verified RTTI set, building on the character *data* of C8 (rigs,
skinning, animation states). Every class below is ✅ from `shar_dumps.csv`; offsets are ⏳.

**Key finding (✅ verified):** `Character` shares the **identical** base as `Vehicle` — `DynaPhysDSG,
StaticPhysDSG, CollisionEntityDSG, IEntityDSG` — so a person and a car are the same kind of physical scene
entity (C23.2), which is why they collide and interact seamlessly. Character AI is a real **finite state
machine**: `CharacterAi::State` has the verified subclasses `Loco`, `InCar`, `InSim`, `GetIn`, `GetOut`,
`NoState`.

---

## Deep-dive pages

- [C25.1 — The `Character` Class](01-the-character-class.md): the shared DSG/physics base.
- [C25.2 — The `CharacterAi` State Machine](02-characterai-states.md): Loco / InCar / GetIn / GetOut / InSim / NoState.
- [C25.3 — Controllers & the `CharacterManager`](03-controllers-manager.md): who drives a character, and the manager.
- [C25.4 — Rigs, Animation & Choreography](04-rigs-animation.md): how C8's `.cho` data drives the live character.
- [C25.5 — Pedestrians, NPCs & Traffic](05-peds-npcs.md): the ambient population at runtime.

---

## 25.1 The `Character` class (✅ verified)

```
Character : DynaPhysDSG, StaticPhysDSG, CollisionEntityDSG, IEntityDSG, tDrawable, tEntity, tRefCounted, …
```

The bases are **identical to `Vehicle`** (C24.1): a character is drawn (`tDrawable`), lives in the scene
graph (`IEntityDSG`), is solid (`CollisionEntityDSG`), and is physically simulated (`DynaPhysDSG`). A person
and a car are one type family — which is exactly why a car can hit a pedestrian, why both rest on the ground,
and why one physics loop moves both. [C25.1](01-the-character-class.md).

## 25.2 The `CharacterAi` state machine (✅ verified)

Character behaviour is a finite state machine. The verified `CharacterAi::State` subclasses:

```
CharacterAi::State
  ├ Loco      — locomotion (walking / running on foot)
  ├ InCar     — riding in a vehicle
  ├ InSim     — in physics simulation (ragdoll / knocked about)
  ├ GetIn     — transitioning into a vehicle
  ├ GetOut    — transitioning out of a vehicle
  └ NoState   — inactive / default
```

A character is always in exactly one state; transitions (`GetIn`→`InCar`→`GetOut`→`Loco`) are the verbs of
character behaviour. The `getin`/`getout` mission objectives (C16.3) drive these transitions. [C25.2](02-characterai-states.md).

## 25.3 Controllers & the manager (✅ verified)

Like vehicles, characters separate *body* from *driver*:

```
CharacterController : tRefCounted, radLoadObject
  CameraRelativeCharacterController : PhysicalController, CharacterController   — player, camera-relative input
CharacterManager : EventListener, LoadingManager::ProcessRequestsCallback      — the manager
CharacterMappable / BipedCharacterMappable : Mappable                          — input mapping
```

`CameraRelativeCharacterController` is the player-on-foot controller (movement relative to the camera);
`CharacterManager` loads and tracks all characters. [C25.3](03-controllers-manager.md).

## 25.4 Rigs, animation & choreography (✅ verified data → runtime)

The `.cho` rig and animation-state graph (C8.1–C8.2) drive the live character: the skeleton poses the skinned
mesh (C8.3), and the animation states map to clips. The `choreo::` namespace (46 classes, C23.3) stages
scripted character performances — the runtime of the choreography documented in C17. [C25.4](04-rigs-animation.md).

## 25.5 Pedestrians, NPCs & traffic (✅ verified)

Ambient characters are spawned by the population commands (`AddPed`, `AddNPC`, ped groups, C14.5) at locators
(C8.4), given a `CharacterAi` (C25.2) in the `Loco` state, and routed along waypoints on the path/road data
(C13). `NPCharacter` and the bonus-mission NPCs (`AddNPCCharacterBonusMission`, C14.5) are mission-relevant
people. [C25.5](05-peds-npcs.md).

---

## Key takeaways

- `Character` shares the **identical DSG/physics base as `Vehicle`** (C23.2/C24.1) — people and cars are one
  physical-entity family, which is why they interact seamlessly.
- Character AI is a verified **finite state machine**: `Loco`, `InCar`, `InSim`, `GetIn`, `GetOut`,
  `NoState` — transitions driven by gameplay (e.g. `getin`/`getout` objectives, C16).
- Body and driver are separated: `CharacterController` (e.g. `CameraRelativeCharacterController` for the
  player) attaches to a `Character`; `CharacterManager` runs them all.
- The `.cho` rigs and animation states (C8) and the `choreo::` classes (C17) drive the live character.
- Ambient population spawns via C14.5 at locators (C8.4), routed on the road/path graph (C13).

**Next:** [Chapter 26 — Missions, Cameras & Physics at Runtime](../C26-Missions-Cameras-Physics/C26-Missions-Cameras-Physics.md).
