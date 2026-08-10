# C42.2 — Attacks: Kick, UFO & Wasps

> Homer's melee and the enemy attacks, as confirmed behaviours and animation tokens.

## Homer's kick — `KickAction` (✅ verified)
Homer's attack is a `KickAction`. Verified animation/string tokens: `jump_kick`, `kickwave`,
and — tellingly — **`"Kick Swaps Character Model"`**: during the kick the character model is
briefly swapped (to a kick-pose/variant rig) then swapped back. The kick is what smashes props,
crates, and gags and knocks down NPCs (ties to C32 combat/collectibles).

## Enemy attacks — `AttackBehaviour` & friends (✅ verified)
- **`AttackBehaviour`** — the general attacker behaviour an NPC/enemy runs.
- **`UFOAttackBehaviour`** — the UFO's attack (with `UFO_ATTACK_ALL`, `ATTACK_PLAYER` tokens) —
  the level 7 alien threat.
- **Wasps** — `Wasp_Attack`/`wasp_attack`: the wasp cameras/drones that attack (tied to the
  police/wasp system, C31, and `ActorAnimationWasp`).

## How an attack runs
The attacker's AI enters an attack state → runs the attack action → plays the attack animation
(`jump_kick`/`kickwave`/`wasp_attack`) → applies the effect (damage/knockback/smash) at the
animation's hit frame → returns to its prior state.

## Why model swap for the kick
Swapping the model for the kick lets the pose/rig be authored specifically for the attack without
bloating the base character rig — a pragmatic 2003-era choice.

## What happens if you bend it
Retime or replace the kick animation; change what the kick affects; hook `AttackBehaviour` to
alter enemy aggression. (Single-player only — C28.6.)

## Cross-references
C32 (combat/health/what the kick breaks), C31 (wasps/UFO threat), C42.5 (animation players),
C34 (animation channels), C42.7 (modding).
