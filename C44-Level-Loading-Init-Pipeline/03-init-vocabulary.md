# C44.3 — The Init Vocabulary

> Every level-wide command `leveli.mfk` uses, grouped by what it sets up. Counts are from
> level 1's init (✅ verified by extraction).

## World & player
| Command | Does |
|---|---|
| `EnableTutorialMode( 1 )` | turn the tutorial prompts on/off for the level |
| `InitLevelPlayerVehicle("famil_v","level1_carstart","DEFAULT")` | the player's starting car + start locator |
| `AddCharacter("homer","homer")` | the player character |
| `SetActorRotationSpeed(...)` | how fast actors turn |

## Police (C31)
| Command | Does |
|---|---|
| `CreateChaseManager("cPolice","Pursuit\L1cop.con",1)` | arm the police, with the cop car config |
| `SetNumChaseCars("1")` | how many cop cars pursue |
| `SetHitAndRunDecay(3.0)` | how fast the Hit & Run meter decays |

## Population (own chapters)
| Command | Does | Chapter |
|---|---|---|
| `CreatePedGroup(N)` / `AddPed("model",w)` / `ClosePedGroup()` | crowd pools | C45 |
| `AddAmbientCharacter("apu","place",r)` | named ambient NPCs | C45 |
| `AddAmbientNPCWaypoint("ped","wp")` | wander paths (×55 in L1) | C47 |
| `CreateTrafficGroup(N)` / `AddTrafficModel("model",w[,f])` / `CloseTrafficGroup()` | traffic pools | C46 |
| `AddSpawnPointByLocatorScript(...)` | locator-driven spawns (wasps) | C47 |
| `AddBehaviour(...)` | attach a behaviour to an actor | C47 |

## Economy & tuning (C32)
| Command | Does |
|---|---|
| `SetCoinDrawable("coinShape_000")` | the coin pickup model |
| `SetProjectileStats(...)` | projectile tuning |
| `PreallocateActors(...)` | reserve the actor pool (C44.4/C39) |

## Conversations & bonus (C48)
`AddNPCCharacterBonusMission`, `SetBonusMissionDialoguePos`, `SetConversationCam`,
`AddAmbientNpcAnimation`/`AddAmbientPcAnimation`, `SetCamBestSide`.

## Cross-references
C44.4/44.5 (deep on preallocation + player/police), C45–C48 (the population subsystems), C31/C32.
