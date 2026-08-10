# Legend — Transitions, Interiors & Actions

Confirmed classes for screen transitions, the interior system, and character actions/animation. Source: RTTI COL walk of retail `Simpsons.exe`. Chapters: C40 (transitions), C41 (interiors), C42 (actions/animation).

| Class | VA | Subsystem | Role |
|---|---|---|---|
| `Fader` | 0x0060B240 | transition | screen fade to/from black (the interior black-box overlay) |
| `CGuiScreenLetterBox` | 0x0060EC24 | transition | cinematic letterbox bars |
| `CGuiScreenIrisWipe` | 0x0060ED20 | transition | iris wipe open/close (EVENT_GUI_IRIS_WIPE_OPEN/CLOSED) |
| `CGuiScreenIntroTransition` | 0x0060FA88 | transition | intro transition screen |
| `TransitionPlayer` | 0x00610D20 | transition | drives a transition sequence |
| `TransitionEvent` | 0x00610DEC | transition | a queued transition event |
| `choreo::Transition` | 0x005FE57C | transition | choreography transition segment |
| `GuiSFX::Transition` | 0x0060D8B0 | transition | scripted UI-effect: transition |
| `GuiSFX::IrisWipeOpen` | 0x0060D8D0 | transition | scripted UI-effect: iris wipe open |
| `GuiSFX::Show` | 0x0060D880 | transition | scripted UI-effect: show element |
| `GuiSFX::Hide` | 0x0060D760 | transition | scripted UI-effect: hide element |
| `GuiSFX::GotoScreen` | 0x0060D7C0 | transition | scripted UI-effect: go to screen |
| `GuiSFX::Chainable` | 0x0060D9C0 | transition | scripted UI-effect base (sequenced) |
| `InteriorManager` | 0x00613C48 | interior | owns interior enter/leave |
| `InteriorEntranceLocator` | 0x006070D4 | interior | where you enter an interior |
| `InteriorExit` | 0x00613C54 | interior | where you leave an interior |
| `InteriorObjective` | 0x006115E8 | interior | mission objective: be inside an interior |
| `LeaveInteriorCondition` | 0x00611348 | interior | mission condition: leave the interior |
| `ActionButton::EnterInterior` | 0x0061723C | interior | the action-button that enters an interior |
| `AttackBehaviour` | — | action | generic attack behaviour |
| `UFOAttackBehaviour` | — | action | UFO attack behaviour |
| `KickAction` | — | action | Homer's kick/attack action |
| `CharacterAi::GetIn` | — | action | AI state: getting into a car |
| `CharacterAi::GetOut` | — | action | AI state: getting out of a car |
| `CharacterAi::InCar` | — | action | AI state: in a car |
| `CharacterAi::Loco` | — | action | AI state: on-foot locomotion |
| `InCarAction` | — | action | put character in car |
| `CarDoorAction` | — | action | open/close a car door |
| `ReleaseDoorsAction` | — | action | release held car doors |
| `WalkerLocomotionAction` | — | action | on-foot locomotion action |
| `ChangeLocomotion` | — | animation | switch a character's locomotion set |
| `PhysicsLocomotion` | — | animation | physics-driven locomotion |
| `VehicleLocomotion` | — | animation | vehicle locomotion |
| `ActorAnimation` | — | animation | an actor's animation |
| `AnimationPlayer` | — | animation | plays an animation on a rig |
| `PlayAnimationAction` | — | animation | action: play an animation |
| `PlayIdleAnimationAction` | — | animation | action: play idle animation |
| `HoldAnimationAction` | — | animation | action: hold on an animation frame |
| `ActionButton::GetInCar` | 0x0 | action | action-button: get in car |
| `ActionButton::OpenDoor` | 0x0 | action | action-button: open a door |
| `ActionButton::AutoPlayAnimInOut` | 0x0 | animation | action-button: auto play in/out animation |
