# C39.5 — Sounds & Effects Past Their Caps

> Two of the most-hit ceilings in a content-heavy mod are **sounds** and **particles** — both Tier-2 pool
> limits. This page applies the pipeline (C39.4) and the pool method (C39.3) to audio and effects specifically.

## More sounds

**The cap.** Sound resources come from a pool the live capture showed at ~**5000** (`daSoundResourceData`), and
sound *buffers* from `radSoundHalBufferDataPool` (C39.3). Beyond those, new sounds don't load or don't play.

**Adding a sound (pipeline).**
1. **Author** the sample as **RSD** — mono, 16-bit, 24000 Hz (the format decoded in C18).
2. **Package** it into the right sound RCF (C19): `soundfx.rcf`, `carsound.rcf`, `ambience.rcf`, `dialog.rcf`,
   or the `music*.rcf` set — put it where the bus expects it.
3. **Reference** it — the script/sound-cluster that triggers it (the `SoundCluster` objects seen live) must name
   your sample.
4. **Budget** — if you're adding *many* sounds, you press the sound-resource and buffer pools (C39.3); enlarge
   them at init if needed, paying static heap.
5. The five audio **volume buses** (C37.3) apply unchanged — your new sound rides its bus's gain.

**Note:** more sound *variety* (swapping/adding samples) rarely hits the cap; more *simultaneous* sounds does.
Diagnose which you're actually adding.

## More effects (particles)

**The cap.** Particles come from `tParticlePool`, caught at exactly **1000** live `tSpriteParticle` in the
capture (C39.1/C39.3). A busy effect scene that stops spawning new particles has hit this pool.

**Adding / intensifying effects (pipeline).**
1. **Author** the effect's assets — the sprite/texture and its particle parameters (C33 covers the particle,
   sprite, and billboard systems; `tSprite`/`tSpriteParticle`/`tBillboardQuadGroup` were all live in the
   capture).
2. **Package & reference** like any asset (C39.4) — the effect is triggered by script/gameplay.
3. **Budget** — if your effect wants more concurrent particles than the pool allows, enlarge `tParticlePool` at
   init (C39.3), within static heap.
4. **Render** — particles draw through the sprite/billboard path (C33); ensure the effect enters that path (it
   does automatically when spawned through the particle system).

## Events (cutscene / transition)

Scripted sequences draw on the `AllocPool<FMVEvent/NISEvent/TransitionEvent>` pools (C39.3). A dense custom
cutscene can exhaust these; enlarge at init the same way. This ties to the NIS composition (C17) — an NIS is
audio + Pure3D + choreo + script events, so a big custom NIS spends several pools at once.

## The tie to menus (C38)

Sounds and effects are exactly the kind of thing a mod wants **toggles** for — an effects-density slider, a mute
for a custom sound set, a "spawn test particles" debug action. Build those into a custom menu (C38) so you can
tune pool usage live and see where the caps bite, instead of editing and relaunching.

## Cross-references

- **C18/C19 — RSD & sound archives**: authoring and packaging audio.
- **C33 — Rendering/Effects**: the particle, sprite, and billboard systems.
- **C17 — NIS**: why a cutscene spends multiple event pools.
- **C39.3** — enlarging the sound/particle/event pools; the static-heap budget.
- **C38** — a menu to drive effect/sound tuning live.
