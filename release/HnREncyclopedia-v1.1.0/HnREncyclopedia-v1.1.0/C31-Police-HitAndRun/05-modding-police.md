# C31.5 — Modding the Police

**What it is.** The practical recipe for changing the pursuit — because it's built from parts you already
know how to edit (a `Vehicle`, a `VehicleAI`, a script command), tuning the police is assembling those edits.
This page is a task-oriented cookbook entry for the enforcement systems.

**The layers you can edit.** The police are the composition of several moddable pieces:

- **The chase car** — `cBlbart` "Black Ferrini (Chase)" is a normal `Vehicle` (C24.1) with a `.con` (C15).
  To change how police *drive* (speed, grip, aggression on impact), edit its `.con` handling (C15.2–C15.5) —
  the safest, fully-verified edit. Want faster or slower police? Change `SetTopSpeedKmh`. Tougher police?
  Raise `SetHitPoints` (but not so far they can't be destroyed, C31.2).
- **The pursuit tuning** — `SetHitNRun` (C31.4) in a mission's script (C14) controls whether and how the
  meter operates. Edit it to make a mission's police more or less aggressive, or to suppress them entirely.
- **The meter behaviour** — how fast heat builds and cools is `HitnRunManager` (C31.1) runtime state. This is
  the native-mod layer: identify `HitnRunManager` by its now-verified vtable (`0x00608D3C`, C23.5) and read/
  adjust its state (offsets ⏳ — recover by diffing, C4.3).

**A worked recipe — "make the police tougher."**

1. **Handling** (data, safe): edit `scripts/cars/cBlbart.con` (C15) — raise `SetTopSpeedKmh` so they keep up,
   raise `SetHitPoints` modestly so they take more ramming.
2. **Aggression** (script): in the target mission's `…i.mfk`, adjust `SetHitNRun` (C31.4) to raise the
   pursuit intensity.
3. **Deep behaviour** (native, DonutsSDK): to change *how* `ChaseAI` pursues, identify it by vtable
   (`ChaseAI` @ `0x00615F60`, C23.5) with `shar::identify` (C28.5), then adjust its state via a *user-supplied*
   offset from a diff (C4.3). Class ✅, offset ⏳ — mark it user-supplied.

Layers 1–2 are data edits (loose-file shadowing, C28.2) — reversible and safe. Layer 3 is native code (C28)
— powerful but needs offset recovery per build (C28.6).

**Why the police are so moddable.** Because SHAR builds the police from *reused, editable parts* (a car, an
AI, a script command) rather than a monolithic hardcoded system (C31.2), almost every aspect is reachable:
the car by its `.con`, the mission tuning by `SetHitNRun`, and the runtime behaviour by the now-verified
vtables. This is the payoff of the engine's controller/component design (C24.2) — a system built from
swappable parts is a system you can mod part by part. Contrast a hardcoded pursuit: you'd have nothing to
edit but raw memory.

**What happens if you bend it.**

- *Make police uncatchable or invincible* — you break the "escape the chase" loop (C31.2). Tune within the
  playable range.
- *Rely on a `ChaseAI`/`HitnRunManager` offset without verifying* — offsets are ⏳ and build-specific (C28.6).
  Diff and re-verify per exe.
- *Edit the chase car's `.con` and expect other cars to change* — it's one specific `Vehicle`. Edit the right
  car (Catalogue).

**Next:** the [Legend](../Legend/README.md) — the named vehicles, characters, missions, and levels.
