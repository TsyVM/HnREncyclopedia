# Chapter 49 — The Manager Layer

> **Goal of this chapter:** explain the single most important architectural pattern in the running
> game — the **managers**. We've named `ChaseManager`, `PathManager`, `RoadManager`,
> `PedestrianManager` and dozens more throughout the book without ever saying *what a manager is*,
> how they work, why the engine is built this way, and — crucially — how to hook one and what
> breaks if you hook it wrong. This chapter is that reference: the pattern, and a categorized
> catalogue of **all 43 confirmed managers**.

If you asked "what is `ChaseManager`? what is `PedestrianManager`? what is `RoadManager`?" the
honest answer is: they're all the *same kind of thing* — a **manager**. Once you understand the
one pattern, you understand all 43 at once.

> **Note:** there is no `ChaosManager` — the police/pursuit manager (the one that unleashes the
> "chaos" of a cop chase) is **`ChaseManager`** (`0x006077FC`). We use its correct name below.

**Key finding (✅ verified):** SHAR's runtime is organized as a set of **manager singletons** —
one long-lived object per subsystem that **owns** that subsystem's objects, **updates** them each
frame, and is the **single access point** to them. There are **43 confirmed managers** (RTTI, with
vtable addresses), spanning seven domains: World & AI (7), Navigation & World (4), Gameplay &
Mission (10), Rendering & UI (5), Audio (6), Physics & Collision (3), and Engine & Resource (8).
Each is a **singleton** reached through a global/accessor, created at boot/level-load, ticked from
the main frame loop (C30), and torn down in reverse. Because each is one object with a known
vtable, a manager is the **ideal hook target** — hook its update or a specific method to change a
whole subsystem's behaviour at once — but also the most dangerous to hook wrong, because everything
in that subsystem flows through it.

---

## Deep-dive pages

- [C49.1 — What a Manager Is](01-what-is-a-manager.md): the singleton subsystem-owner pattern.
- [C49.2 — How Managers Work](02-how-managers-work.md): create → tick → own → destroy; the frame loop.
- [C49.3 — Why the Manager Pattern](03-why-the-pattern.md): the design reasoning (and trade-offs).
- [C49.4 — The Manager Catalogue](04-the-catalogue.md): all 43, categorized, with what each does.
- [C49.5 — Hooking a Manager](05-hooking.md): how to hook one safely (DonutsSDK + VanHooks).
- [C49.6 — Improper Hooking: What Breaks](06-improper-hooking.md): the failure modes and how to avoid them.

---

## 49.1 What a manager is (✅ verified)

A **manager** is a long-lived **singleton** that owns and drives one subsystem. `PedestrianManager`
owns the crowd; `RoadManager` owns the road network; `ChaseManager` owns the police pursuit. One
object, one subsystem, one access point. [C49.1](01-what-is-a-manager.md).

## 49.2 How they work (✅ verified shape)

Each manager is **created** at boot or level-load, **updated** every frame from the main loop
(C30), **owns** its subsystem's objects (a list/pool it allocates and frees), and is **destroyed**
in reverse order at teardown. You reach it through a global accessor (`GetPedestrianManager()`-style
singleton). [C49.2](02-how-managers-work.md).

## 49.3 Why this pattern (✅ reasoned)

Centralizing each subsystem in one owner gives clear lifetime, one update site, one place to query,
and no ambiguity about who owns what — the standard, pragmatic architecture for a 2003 game engine.
[C49.3](03-why-the-pattern.md).

## 49.4 The catalogue — all 43 managers (✅ verified)

Every confirmed manager, its vtable, and what it does. Full data: `RE-Data-And-Discoveries/data/managers.json` and `DonutsSDK/data/managers.csv`.

### World & AI
| Manager | VA | What it does |
|---|---|---|
| `PedestrianManager` | `0x006078A8` | spawns/updates the pedestrian crowd (C45) |
| `TrafficManager` | `0x00607928` | spawns/updates road traffic (C46) |
| `CharacterManager` | `0x00607ADC` | owns all `Character`/NPC objects (C25) |
| `ActorManager` | `0x00615A8C` | owns the actor pool (`PreallocateActors`, C44) |
| `SpawnManager` | `0x0060785C` | runs locator spawn points (C47) |
| `AvatarManager` | `0x00608D80` | the player avatar(s) |
| `ParkedCarManager` | `0x006077CC` | the parked, enterable cars around the map |

### Navigation & World
| Manager | VA | What it does |
|---|---|---|
| `RoadManager` | `0x0060B6D0` | the road network traffic drives on (C13/C46) |
| `PathManager` | `0x006072A8` | the path/waypoint graph for AI navigation (C13) |
| `InteriorManager` | `0x00613C48` | world↔interior swap (C41) |
| `BreakablesManager` | `0x0060B758` | breakable world objects (C32) |

### Gameplay & Mission
| Manager | VA | What it does |
|---|---|---|
| `GameplayManager` | `0x00612D00` | top-level gameplay state (C30) |
| `MissionManager` | `0x00612B6C` | the active mission + objectives (C16) |
| `ChaseManager` | `0x006077FC` | the police chase/pursuit — the "chaos" (C31) |
| `HitnRunManager` | `0x00608D3C` | the Hit & Run meter (C31) |
| `CoinManager` | `0x006077E0` | coins spawned/collected (C32) |
| `RewardsManager` | `0x006111EC` | unlockable rewards (cards/costumes/cars, C32) |
| `CharacterSheetManager` | `0x0061116C` | the player progress sheet (C27) |
| `TutorialManager` | `0x00610CF0` | tutorial prompts (C44) |
| `SuperSprintManager` | `0x0060688C` | the 2-player SuperSprint bonus mode |
| `GameDataManager` | `0x00607618` | game data / save records (C27) |

### Rendering & UI
| Manager | VA | What it does |
|---|---|---|
| `RenderManager` | `0x0060BFC0` | the render pipeline (C33) |
| `PresentationManager` | `0x00610D84` | presentation / HUD / transitions (C40) |
| `CGuiManager` | `0x00610C48` | the UI screen stack per context (C38) |
| `FeResourceManager` | `0x005F43F4` | front-end (Scrooby) resources (C21) |
| `Scrooby::ResourceManager` | `0x005F4364` | Scrooby UI resources (C21) |

### Audio
| Manager | VA | What it does |
|---|---|---|
| `SoundManager` | `0x0060B300` | top-level sound (C18/C19) |
| `MovingSoundManager` | `0x00608E94` | positional / moving sound sources |
| `Sound::daSoundRenderingManager` | `0x0060A944` | sound mixing / rendering |
| `Sound::daSoundPlayerManager` | `0x0060B1E0` | sound playback voices |
| `Sound::daSoundResourceManager` | `0x0060A8C8` | the sound resource pool |
| `Sound::daSoundDynaLoadManager` | `0x0060B194` | dynamic sound streaming |

### Physics & Collision
| Manager | VA | What it does |
|---|---|---|
| `sim::CollisionManager` | `0x005F339C` | the collision system (C11) |
| `sim::SimUnitsManager` | `0x005F36F8` | the sim rigid-body units (C35) |
| `WorldCollisionSolverAgentManager` | `0x0060895C` | world collision solver agents (C11) |

### Engine & Resource
| Manager | VA | What it does |
|---|---|---|
| `HeapManager` | `0x00612EA0` | memory heap allocation (C39) |
| `LoadingManager` | `0x00613A7C` | the level load sequence (C30) |
| `radLoadManager` | `0x005F829C` | RadCore async resource loading |
| `tLoadManager` | `0x005F8884` | Pure3D asset loading (C1) |
| `InputManager` | `0x00614428` | controller/keyboard/mouse input (C37) |
| `ActionButtonManager` | `0x00616D28` | context action buttons (C42) |
| `AnimEntityDSGManager` | `0x0060B72C` | animated entity DSG objects (C34/C42) |
| `MemoryCardManager` | `0x00607514` | save-device / memory card (C27) |

Full page: [C49.4](04-the-catalogue.md).

## 49.5 Hooking a manager (✅ practical)

A manager is one object with a known vtable — hook its **update** to run each frame, or a specific
method to intercept one operation, using DonutsSDK + VanHooks (C28.5/C28.7). [C49.5](05-hooking.md).

## 49.6 Improper hooking — what breaks (✅ critical)

Because a whole subsystem flows through its manager, a bad hook there is catastrophic: skip the
original update and the subsystem freezes; corrupt `this` and everything it owns is lost; hook on
the wrong thread and you race the main loop. [C49.6](06-improper-hooking.md).

---

## What this chapter established

- The runtime is a **manager layer**: **43 confirmed singletons**, one per subsystem, each owning,
  updating, and gating access to its domain.
- They share one lifecycle — **create → tick → own → destroy** — driven from the frame loop (C30).
- A manager is the **highest-leverage hook target** (change a whole subsystem at once) and the
  **most dangerous** (everything flows through it) — C49.5/49.6.

**Cross-references:** every subsystem chapter names its manager — C13 (Road/Path), C25 (Character),
C31 (Chase/HitnRun), C32 (Coin/Rewards/Breakables), C41 (Interior), C45 (Pedestrian), C46 (Traffic),
C47 (Spawn), C30 (Gameplay/Loading), C33 (Render), C38 (CGui), C11 (Collision), C39 (Heap), C28.5/28.7
(hooking + SAHRDiag). Data: `managers.json` / `managers.csv`.
