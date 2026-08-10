# Legend — The Managers

All **43** confirmed manager singletons (RTTI, retail `Simpsons.exe`), categorized. Each owns, updates, and gates access to one subsystem. Full explanation: **C49 — The Manager Layer** (what they are, how/why they work, how to hook, and what breaks if you hook wrong). Data: `RE-Data-And-Discoveries/data/managers.json`.

## World & AI

| Manager | VA | Role |
|---|---|---|
| `ActorManager` | 0x00615A8C | owns the actor pool (PreallocateActors, C44) |
| `AvatarManager` | 0x00608D80 | the player avatar(s) |
| `CharacterManager` | 0x00607ADC | owns all Character/NPC objects (C25) |
| `ParkedCarManager` | 0x006077CC | the parked, enterable cars around the map |
| `PedestrianManager` | 0x006078A8 | spawns/updates the pedestrian crowd (C45) |
| `SpawnManager` | 0x0060785C | runs locator spawn points (C47) |
| `TrafficManager` | 0x00607928 | spawns/updates road traffic (C46) |

## Navigation & World

| Manager | VA | Role |
|---|---|---|
| `BreakablesManager` | 0x0060B758 | breakable world objects (glass/props, C32) |
| `InteriorManager` | 0x00613C48 | world↔interior swap (C41) |
| `PathManager` | 0x006072A8 | the path/waypoint graph for AI navigation (C13) |
| `RoadManager` | 0x0060B6D0 | the road network traffic drives on (C13/C46) |

## Gameplay & Mission

| Manager | VA | Role |
|---|---|---|
| `CharacterSheetManager` | 0x0061116C | the player's progress sheet/save state (C27) |
| `ChaseManager` | 0x006077FC | the police chase/pursuit (C31) — the 'chaos' manager |
| `CoinManager` | 0x006077E0 | coins spawned/collected (C32) |
| `GameDataManager` | 0x00607618 | game data / save records (C27) |
| `GameplayManager` | 0x00612D00 | top-level gameplay state (C30) |
| `HitnRunManager` | 0x00608D3C | the Hit & Run meter (C31) |
| `MissionManager` | 0x00612B6C | active mission + objectives (C16) |
| `RewardsManager` | 0x006111EC | unlockable rewards (cards/costumes/cars, C32) |
| `SuperSprintManager` | 0x0060688C | the 2-player SuperSprint bonus mode |
| `TutorialManager` | 0x00610CF0 | tutorial prompts (C44) |

## Rendering & UI

| Manager | VA | Role |
|---|---|---|
| `CGuiManager` | 0x00610C48 | the UI screen stack per context (C38) |
| `FeResourceManager` | 0x005F43F4 | front-end (Scrooby) resources (C21) |
| `PresentationManager` | 0x00610D84 | presentation/HUD/transition presentation (C40) |
| `RenderManager` | 0x0060BFC0 | the render pipeline (C33) |
| `Scrooby::ResourceManager` | 0x005F4364 | Scrooby UI resources (C21) |

## Audio

| Manager | VA | Role |
|---|---|---|
| `MovingSoundManager` | 0x00608E94 | positional/moving sound sources |
| `Sound::daSoundDynaLoadManager` | 0x0060B194 | dynamic sound streaming/loading |
| `Sound::daSoundPlayerManager` | 0x0060B1E0 | sound playback voices |
| `Sound::daSoundRenderingManager` | 0x0060A944 | sound mixing/rendering |
| `Sound::daSoundResourceManager` | 0x0060A8C8 | sound resource pool (daSoundResourceData) |
| `SoundManager` | 0x0060B300 | top-level sound (C18/C19) |

## Physics & Collision

| Manager | VA | Role |
|---|---|---|
| `WorldCollisionSolverAgentManager` | 0x0060895C | world collision solver agents (C11) |
| `sim::CollisionManager` | 0x005F339C | the collision system (C11) |
| `sim::SimUnitsManager` | 0x005F36F8 | the sim rigid-body units (C35) |

## Engine & Resource

| Manager | VA | Role |
|---|---|---|
| `ActionButtonManager` | 0x00616D28 | context action buttons (C42) |
| `AnimEntityDSGManager` | 0x0060B72C | animated entity DSG objects (C42/C34) |
| `HeapManager` | 0x00612EA0 | memory heap allocation (C39) |
| `InputManager` | 0x00614428 | controller/keyboard/mouse input (C37) |
| `LoadingManager` | 0x00613A7C | the level load sequence (C30) |
| `MemoryCardManager` | 0x00607514 | save-device / memory card (C27) |
| `radLoadManager` | 0x005F829C | RadCore async resource loading |
| `tLoadManager` | 0x005F8884 | Pure3D asset loading (C1) |

