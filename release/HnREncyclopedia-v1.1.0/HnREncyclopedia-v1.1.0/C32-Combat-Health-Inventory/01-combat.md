# C32.1 — Combat: the Kick & Attack Behaviours

**What it is.** SHAR's on-foot offense — the player's **kick** and the **attack behaviours** of the enemies
that fight back. It's deliberately light combat (this is a comedy driving game), but it's a real system with
verified classes.

**How it works (✅ verified).**

```
KickAction          (0x0061647C)  — the player's kick attack
AttackBehaviour     (0x00615A30)  — a generic enemy attack behaviour
UFOAttackBehaviour  (0x006156F0)  — the UFO/alien enemy's attack
```

**`KickAction`** is the player character's melee — the kick you use on foot to smash breakable objects, set
off gags (C14.4), and hit enemies. Its animation/effect is the verified **`*_kickwave`** character states
(C8, one per playable character: `homer_kickwave`, `bart_kickwave`, `lisa_kickwave`, `marge_kickwave`,
`apu_kickwave`) — the "wave" is the kick's impact effect. So the kick is a `KickAction` (the logic) driving a
`kickwave` animation state (the visuals) on the character (C25).

Enemies attack via **`AttackBehaviour`** — an AI behaviour that makes an NPC aggress the player — with
**`UFOAttackBehaviour`** as a specialised variant for the game's alien/UFO enemies (a recurring Simpsons
sci-fi gag). These plug into the character AI (C25.2) as behaviours the enemy runs.

**Why combat is light.** SHAR is a *driving and collecting* game with platforming and comedy, not a
brawler. Combat exists to give the on-foot sections stakes — you can kick things and be attacked — without
becoming a fighting game. A single kick action plus a couple of enemy attack behaviours is exactly enough:
it makes the world interactive on foot (smash that, kick that enemy) without a deep combat system the game
doesn't need. This is a deliberate scope choice, and the small class count (one kick, two attack behaviours)
reflects it — compare the dozens of classes in the driving (C24), mission (C16), or UI (C21) systems.

**The tie to characters and objects.** The kick connects the character system (C25) — the `kickwave` state,
the `KickAction` — to the interactive world (gags C14.4, breakable objects). It's how a character *acts on*
the world on foot, the on-foot equivalent of ramming in a car (C24/C26.6). The enemy attack behaviours tie
into the AI (C25.2) as behaviours the `CharacterAi` runs.

**What happens if you bend it.**

- *Rely on a `KickAction`/`AttackBehaviour` member offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Expect deep combat mechanics* — it's a single kick plus enemy attacks. Don't over-model it.
- *Edit the kickwave animation without the `KickAction`* — the visual and the logic are separate (C25.4);
  the kick's *effect* is `KickAction`, its *look* is the animation state.
