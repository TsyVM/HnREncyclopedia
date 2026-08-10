# C51.5 — Projectiles

> Separate from particles: actual **projectiles** — the wasp's ray — with tunable speed and damage.

## The classes (✅ verified)
`Projectile` and `ProjectileDSG` are the projectile object and its scene-graph drawable/collision
node. A projectile is a moving, colliding entity (unlike a particle, which is a cosmetic sprite) — it
travels, hits, and applies an effect.

## Tuning them (✅ verified)
```
SetProjectileStats( "waspray", "120.0", "6" );
SetProjectileStats( "waspray", "60.0",  "3" );
```
Args: a named projectile type (`"waspray"`), a **speed** (60.0–150.0 across the retail scripts), and a
second parameter (3–6 — 🟡 likely damage or range). Different missions/difficulties set different
values for the **wasp's ray** — the projectile the wasp enemies (C31/C47) fire at the player.

## How it works
```
wasp AI (AttackBehaviour, C42) ─► fire ─► Projectile("waspray") spawned with speed
   ─► travels (ProjectileDSG) ─► collides with player/world (C11) ─► applies effect (damage) ─► despawn
```
The projectile is a first-class colliding entity, so it interacts with the collision system (C11) —
that's why it can hit you and be dodged.

## Why projectiles are separate from particles
A particle is cosmetic (no collision, pooled, drops when full). A projectile *matters to gameplay* (it
must reliably hit and damage), so it's a real entity with collision and its own tuning — never dropped
for being over a cosmetic budget.

## Bend it
- Tune `SetProjectileStats` (speed/param) to make the wasp ray faster/slower or harder/easier.
- Hook `Projectile`/`AttackBehaviour` (C42/C28.5) for custom projectile behaviour.

## Cross-references
C31/C47 (the wasps that fire), C42 (the attack behaviour), C11 (projectile collision), C51.1 (why it's
not a particle), C14 (the `SetProjectileStats` scripts).
