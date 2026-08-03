# Legend — Functions (Script Commands)

The complete script vocabularies. ✅ verified by extraction from the retail scripts. Occurrence counts are raw call counts across the shipped files. See Chapter 14 (MFK) and Chapter 15 (CON).

## MFK — level/mission commands (172 distinct)

### Asset loading

- `LoadP3DFile` — 1013
- `SetDynaLoadData` — 154
- `LoadDisposableCar` — 128
- `StreetRacePropsLoad` — 23
- `GagSetSoundLoadDistances` — 2

### Cameras

- `SetConversationCam` — 399
- `SetCamBestSide` — 130
- `SetAnimCamMulticontName` — 76
- `SetAnimatedCameraName` — 76
- `SetConversationCamNpcName` — 21
- `SetConversationCamPcName` — 21

### Collectibles

- `AddCollectible` — 689
- `SetCollectibleEffect` — 337
- `BindCollectibleTo` — 36
- `SetCoinDrawable` — 16
- `SetCoinFee` — 7
- `AddCollectibleStateProp` — 4
- `AttachStatePropCollectible` — 2

### Dialogue

- `SetDialogueInfo` — 138
- `SetDialoguePositions` — 107
- `SetCompletionDialog` — 45
- `TurnGotoDialogOff` — 43

### Gags

- `GagBegin` — 419
- `GagEnd` — 419
- `GagSetCycle` — 419
- `GagSetPosition` — 418
- `GagSetRandom` — 418
- `GagSetTrigger` — 414
- `GagSetSound` — 406
- `GagSetInterior` — 309
- `GagSetCoins` — 181
- `GagSetPersist` — 175
- `GagSetSparkle` — 99
- `GagSetAnimCollision` — 22
- `AddGagBinding` — 21
- `ClearGagBindings` — 11
- `GagPlayFMV` — 11
- `GagSetIntro` — 8
- `GagSetOutro` — 8
- `SetTotalGags` — 7
- `GagSetCameraShake` — 4
- `GagCheckCollCards` — 2
- `GagCheckMovie` — 2

### HUD/UI

- `SetHUDIcon` — 429
- `ShowHUD` — 1

### Level setup

- `AddTeleportDest` — 78

### Missions/stages

- `AddObjective` — 671
- `CloseObjective` — 671
- `AddStage` — 670
- `CloseStage` — 670
- `SetStageMessageIndex` — 495
- `AddStageWaypoint` — 442
- `AddCondition` — 435
- `CloseCondition` — 435
- `AddObjectiveNPCWaypoint` — 189
- `AddStageVehicle` — 177
- `CloseMission` — 154
- `SelectMission` — 154
- `ShowStageComplete` — 120
- `SetStageTime` — 107
- `SetMissionResetPlayerInCar` — 82
- `AddNPCCharacterBonusMission` — 81
- `AddStageTime` — 74
- `SetMissionResetPlayerOutCar` — 68
- `AddMission` — 64
- `SetStageAIRaceCatchupParams` — 64
- `SetMissionStartCameraName` — 61
- `SetMissionStartMulticontName` — 61
- `AddBonusMission` — 46
- `AddBonusMissionNPCWaypoint` — 45
- `SetBonusMissionDialoguePos` — 29
- `NoTrafficForStage` — 21
- `SetStageMusicAlwaysOn` — 18
- `SetConditionPosition` — 17
- `AddStageCharacter` — 16
- `StageStartMusicEvent` — 15
- `AddStageMusicChange` — 13
- `SetStageAITargetCatchupParams` — 8
- `AllowMissionAbort` — 3

### Other

- `AddBehaviour` — 351
- `SetDestination` — 216
- `AddToCountdownSequence` — 176
- `SuppressDriver` — 162
- `RESET_TO_HERE` — 135
- `SetParticleTexture` — 119
- `SetCondMinHealth` — 113
- `SetCondTime` — 100
- `SetTalkToTarget` — 100
- `SetHitNRun` — 78
- `SetPresentationBitmap` — 69
- `StartCountdown` — 43
- `SetDurationTime` — 27
- `DisableHitAndRun` — 25
- `StreetRacePropsUnload` — 23
- `SetRaceLaps` — 21
- `SetNumValidFailureHints` — 20
- `PreallocateActors` — 19
- `EnableTutorialMode` — 17
- `SetObjDistance` — 17
- `AddCharacter` — 16
- `CreateChaseManager` — 16
- `SetActorRotationSpeed` — 16
- `SetFadeOut` — 16
- `SetProjectileStats` — 16
- `RACE` — 14
- `SetHitAndRunDecay` — 14
- `AddShield` — 12
- `GasSound` — 12
- `SetFollowDistances` — 12
- `SetSwapPlayerLocator` — 12
- `MustActionTrigger` — 10
- `SetMusicState` — 9
- `SetInitialWalk` — 8
- `SetParTime` — 8
- `SetDemoLoopTime` — 7
- `SetRaceEnteryFee` — 7
- `UseElapsedTime` — 7
- `RemoveDriver` — 6
- `SetFMVInfo` — 6
- `SetIrisWipe` — 6
- `SetPostLevelFMV` — 6
- `SetStatepropShadow` — 6
- `StayInBlack` — 6
- `AddSafeZone` — 4
- `SetCharacterToHide` — 4
- `SetObjTargetBoss` — 4
- `SetPickupTarget` — 4
- `AddFlyingActorByLocator` — 3
- `GoToPsScreenWhenDone` — 3
- `SetLevelOver` — 3
- `Attributes` — 2
- `AddDriver` — 1
- `AllowRockOut` — 1
- `Race` — 1
- `SetGameOver` — 1
- `SetHitAndRunMeter` — 1

### Peds/NPCs

- `AddAmbientPcAnimation` — 570
- `AddAmbientNpcAnimation` — 547
- `AddAmbientNPCWaypoint` — 473
- `AddPed` — 444
- `AddSpawnPointByLocatorScript` — 371
- `AddNPC` — 318
- `AmbientAnimationRandomize` — 264
- `SetMaxTraffic` — 136
- `UsePedGroup` — 134
- `AddAmbientCharacter` — 122
- `ClosePedGroup` — 116
- `CreatePedGroup` — 116
- `AddTrafficModel` — 64
- `ClearAmbientAnimations` — 28
- `AddPurchaseCarNPCWaypoint` — 26
- `CloseTrafficGroup` — 16
- `CreateTrafficGroup` — 16
- `AddSpawnPoint` — 7
- `RemoveNPC` — 4
- `SetChaseSpawnRate` — 1

### Rewards

- `BindReward` — 147
- `AddPurchaseCarReward` — 32

### Vehicles

- `SetCondTargetVehicle` — 136
- `SetObjTargetVehicle` — 101
- `SetCarAttributes` — 74
- `SetVehicleAIParams` — 61
- `ActivateVehicle` — 48
- `PlacePlayerCar` — 36
- `InitLevelPlayerVehicle` — 32
- `AddVehicleSelectInfo` — 28
- `PutMFPlayerInCar` — 28
- `SetForcedCar` — 16
- `SetNumChaseCars` — 16
- `SetSwapDefaultCarLocator` — 12
- `SetSwapForcedCarLocator` — 12
- `SwapInDefaultCar` — 12

## CON — vehicle handling commands (40 distinct)

| Command | Cars using |
|---|---:|
| `SetBrakeScale` | 90 |
| `SetCMOffsetX` | 90 |
| `SetCMOffsetY` | 90 |
| `SetCMOffsetZ` | 90 |
| `SetDamperC` | 90 |
| `SetEBrakeEffect` | 90 |
| `SetGasScale` | 90 |
| `SetHighSpeedSteeringDrop` | 90 |
| `SetMass` | 90 |
| `SetMaxWheelTurnAngle` | 90 |
| `SetNormalSteering` | 90 |
| `SetSlipGasScale` | 90 |
| `SetSlipSteering` | 90 |
| `SetSpringK` | 90 |
| `SetSuspensionLimit` | 90 |
| `SetTireGrip` | 90 |
| `SetTopSpeedKmh` | 90 |
| `SetHitPoints` | 89 |
| `SetCharactersVisible` | 88 |
| `SetBurnoutRange` | 87 |
| `SetDonutTorque` | 87 |
| `SetGamblingOdds` | 87 |
| `SetMaxSpeedBurstTime` | 87 |
| `SetSlipEffectNoEBrake` | 86 |
| `SetSlipSteeringNoEBrake` | 86 |
| `SetWheelieOffsetY` | 86 |
| `SetWheelieOffsetZ` | 86 |
| `SetWheelieRange` | 86 |
| `SetShadowAdjustments` | 85 |
| `SetWeebleOffset` | 83 |
| `SetSuspensionYOffset` | 79 |
| `SetDriver` | 55 |
| `SetHasDoors` | 55 |
| `SetIrisTransition` | 36 |
| `SetShininess` | 33 |
| `SetCharacterScale` | 30 |
| `SetHighRoof` | 28 |
| `SetGasScaleSpeedThreshold` | 17 |
| `SetHighSpeedGasScale` | 17 |
| `SetAllowSeatSlide` | 4 |
