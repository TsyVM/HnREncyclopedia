# C42.5 — The Animation Players

> What actually drives a rig's bones over time. Several confirmed players, plus action wrappers.

## The players (✅ verified)
- **`AnimationPlayer`** (with `AnimationPlayer::LoadDataCallBack`) — the main player: binds an
  animation to a rig and advances it.
- **`ActorAnimation`** — an actor's animation instance (variants `ActorAnimationUFO`,
  `ActorAnimationWasp` for those enemies).
- **`SimpleAnimationPlayer`** — a lightweight player for simple cases.
- **`PresentationAnimator`**, **`Scenegraph::TransformAnimationController`**,
  **`StatePropDSGProcAnimator`** — animators for presentation/transform/prop channels.

## The action wrappers (✅ verified)
- **`PlayAnimationAction`** — play a named animation.
- **`PlayIdleAnimationAction`** — play the idle loop.
- **`HoldAnimationAction`** — hold on a frame (freeze a pose).

## How it fits the stack
```
Action (PlayAnimationAction / KickAction / GetIn) 
   └─► AnimationPlayer  ──► animation channels (C34) ──► rig bones ──► drawable (C7/C10)
```
An action asks a player to run a clip; the player samples the animation's typed channels (C34 —
translation/rotation/compressed-quaternion tracks) and writes the rig's bone transforms, which the
scenegraph then draws.

## Why multiple players
Different content needs different players: a full actor with locomotion vs a simple animated prop
vs a presentation element. Sharing one heavy player everywhere would waste memory (recall the
pooled `AnimationPlayer`s the live capture implies).

## What happens if you bend it
Hook `AnimationPlayer` to retarget or retime clips; use the play/idle/hold actions from a mod to
drive your own animations.

## Cross-references
C34 (animation channels — the keyframe data), C7/C10 (rig → drawable → scenegraph), C42.1 (actions),
C42.4 (locomotion uses these players).
