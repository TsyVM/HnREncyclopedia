# C15.6 — Visual, Meta & the Runtime Bridge

**What it is.** The remaining `.con` commands — occupants, doors, shadow, scale, and assorted flags — plus
the bridge this whole chapter has been building toward: how a value parsed from a text file ends up
driving the live `Vehicle` object at runtime (Chapter 24).

**Occupants & body.**

- **`SetCharactersVisible(0|1)`** — whether driver/passengers are drawn (88 cars). Ambulance `1`.
- **`SetHasDoors(0|1)`** — whether the car has opening doors (55 cars); affects enter/exit animation.
- **`SetDriver("name")`** — the character assigned to drive (55 cars); a string naming a character asset
  (🟡 — resolution is C24/C25).
- **`SetCharacterScale(x)`** — scale applied to occupants (30 cars). Ambulance `0.9`; used so oversized
  or undersized characters fit their vehicle — a very *Simpsons* touch.
- **`SetHighRoof(0|1)`** — a body-class flag (28 cars) affecting enter/exit and camera.
- **`SetAllowSeatSlide(0|1)`** — occupant seat adjustment (4 cars).

**Presentation.**

- **`SetShadowAdjustments(8 floats)`** — the blob-shadow shape under the car (85 cars). Eight numbers
  describing the shadow quad's extents/offsets. A cheap 2003-era shadow, tuned per car so the blob fits
  the silhouette.
- **`SetShininess(x)`** — specular highlight strength (33 cars).
- **`SetIrisTransition(0|1)`** — the iris-wipe transition flag when entering this car (36 cars); ties the
  car to the front-end transition system (C21).

**The runtime bridge (✅ names / ⏳ offsets).** When the game builds a car, it constructs a `Vehicle`
object — an RTTI-confirmed class, along with `VehicleCentral` and `VehicleController` (C24) — and runs the
`.con` to fill it. Each `Set…` corresponds to writing one member of that object (or a sub-object like its
handling/physics block). The **class names are ✅ verified** from `Simpsons.exe`'s RTTI; the **exact member
offset each `Set…` writes is ⏳ Open** and is recovered by the diff method of [C4.3](../C4-Byte-Level-Toolcraft/03-hex-diffing.md):
change one `.con` value, observe which member of the live object moves. This chapter gives you the *source*
side of that bridge — the complete, verified set of values a car exposes; Chapter 24 walks the *destination*
side.

**Why the split matters.** Because the `.con` layer is fully in the clear and the runtime layer is only
partly recovered, the honest state of vehicle modding is: **you can change any handling value with total
confidence today** (edit the `.con`, C15.2–C15.5), and you can reach the *same* values live via the SDK
once you supply the offset from a diff. The text file is the safe, complete, verified interface; the memory
offsets are the frontier.

**What happens if you bend it.**

- *Set `SetCharactersVisible(0)` on the player car* — the driver vanishes; fine for a ghost car, jarring
  otherwise. These flags are cosmetic but very visible.
- *Give a `SetShadowAdjustments` shape that doesn't match the model* — the blob shadow floats or clips.
  Copy the eight numbers from a similarly-shaped car as a starting point.
- *Point `SetDriver` at a character that isn't loaded* — the driver may not appear or the car may fail to
  populate. Ensure the named character is loaded by the level/mission (Chapter 14) before assigning it.

**Next:** [Chapter 16 — Mission Structure & Objectives](../C16-Missions-Objectives/C16-Missions-Objectives.md).
