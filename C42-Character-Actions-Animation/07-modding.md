# C42.7 — Modding Actions & Animations

> Actions and animations are confirmed classes plus named animation clips, so they're moddable
> from the asset side (swap clips) and the native side (hook actions).

## Asset-level
- **Swap an animation:** replace the clip a character/prop plays (`getin`, `kickwave`,
  `locomotion8`, an idle) with your own `.p3d` animation of the same rig (C34/C7). The action
  keeps working; the motion changes.
- **Retexture the kick model swap:** the *"Kick Swaps Character Model"* pose model can be swapped
  (C42.2).

## Script-level
- Attach an `ActionButton::PlayAnimLoop`/`AutoPlayAnimInOut` to a prop to make it interactive
  (C42.6) — no code.
- Use `PutMFPlayerInCar` / `SetMissionResetPlayerInCar` in a mission script for scripted entries
  (C42.3).

## Native-level (DonutsSDK + VanHooks)
- **Retime/replace actions:** hook `KickAction`, `CharacterAi::GetIn/GetOut`, or `AnimationPlayer`
  to change timing, skip a phase, or retarget a clip.
- **Alter enemy behaviour:** hook `AttackBehaviour`/`UFOAttackBehaviour`.
- Read the live character via `shar::identify` and the runtime offsets (C28.7).

## Cautions
- **Respect locomotion animation counts** (C42.4/C39) — too few and the engine asserts.
- Keep vehicle entry/exit **atomic** (don't leave a character half-in).
- Per-build address re-verification; reversible; single-player/offline (C28.6).

## Cross-references
C34/C7 (animation & rig assets), C42.1–42.6 (the classes to target), C39 (animation limits),
C28.5/28.7 (hooking + SAHRDiag).
