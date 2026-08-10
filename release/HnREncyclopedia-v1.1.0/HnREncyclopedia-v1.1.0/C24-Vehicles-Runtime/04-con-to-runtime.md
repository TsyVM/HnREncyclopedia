# C24.4 — From CON to the Live Car

**What it is.** The bridge this chapter has been building toward: how the plain-text handling values of a
`.con` file (C15) become the numbers that govern a live `Vehicle`. It is the single most-requested piece of
vehicle modding — and the clearest example of the book's ✅-name / ⏳-offset split.

**How it works (✅ path; ⏳ exact offsets).** When `VehicleCentral` (C24.3) builds a car, it constructs a
`Vehicle` (C24.1) with default handling, then applies the car's `.con`: each `Set…` call (C15) writes one
handling parameter into the `Vehicle`'s handling/physics state. So the chain is:

```
scripts/cars/ambul.con   →  parsed  →  SetMass(2500) … SetTireGrip(2.5) …
                                          │  each writes one member of…
                                          ▼
                              the live Vehicle's handling block  →  physics (C26)  →  motion
```

The **class** the values land in is verified (`Vehicle` and its physics bases, C24.1); the **exact byte
offset** each `Set…` writes is **⏳**. That is not a gap in understanding the *system* — the path is clear —
only in the *addresses*, which RTTI doesn't provide (C23.1).

**Recovering an offset (the diff method).** The offsets are recoverable, one at a time, with C4.3: freeze the
game, change one `.con` value (e.g. `SetTopSpeedKmh(130)` → `160`), reload the car, and diff the live
`Vehicle`'s memory. The four bytes that changed from `130.0` to `160.0` are top speed's offset. Repeat per
parameter and you build a verified `layout::Vehicle` — each entry promoted from ⏳ to ✅ by a citable diff, and
each safe to use because it's your own measurement against your own build.

**Why the split is honest, not evasive.** SHAR vehicle modding has two fully-usable interfaces *today*: the
`.con` file (edit any handling value with total confidence — C15.2–C15.5, no offsets needed) and the SDK's
type-checked access (identify a `Vehicle` by vtable, C23.5, then write a *user-supplied* offset). The `.con`
route is the complete, verified interface; the live-memory route needs one diff per field. Saying "the class
is `Vehicle` (✅) and top speed is at some offset you can find by diffing (⏳)" is the exact, honest state — and
it's *actionable*, because it tells you precisely what to measure.

**What the parameters become.** The `.con` groups (C15) map onto the physics body (C26): mass and drivetrain
(C15.2) set the `DynaPhysDSG` body's mass and drive forces; grip and steering (C15.3) tune the tyre/steering
model; suspension and centre of mass (C15.4) configure the `sim::` physics (C26). So the `.con` is really the
*designer's control panel over the physics simulation*, and this page is where that panel meets the machine.

**What happens if you bend it.**

- *Guess a `Vehicle` offset from another trainer without verifying it on your build* — offsets shift; treat
  any offset as user-supplied and re-verify (C4.3). Mark it as such.
- *Edit live memory when a `.con` edit would do* — for handling, the `.con` is the complete, verified,
  reversible interface (C15). Reserve live edits for things the `.con` can't reach.
- *Expect one `.con` value to map to exactly one obvious member* — some feed derived physics quantities.
  Confirm each mapping by diffing both directions (C4.4).
