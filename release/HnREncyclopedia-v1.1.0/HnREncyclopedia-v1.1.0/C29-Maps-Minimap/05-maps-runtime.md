# C29.5 — Maps at Runtime

**What it is.** How the map comes alive each frame — projecting world positions onto the map, placing the
player marker and points of interest, and rotating the 3-D model. This closes the maps chapter by connecting
the map data (C29.1–C29.4) to the running game.

**How it works.** Each frame the map system:

1. **Reads the player's world position** (from the player `Character`/`Vehicle`, C24/C25) and places the
   `user` icon (C29.3) at the corresponding **map position**, using the map model's anchor chunks (C29.2) to
   calibrate the world→map transform.
2. **Projects points of interest** — active missions (`phone`/`mission`), race markers (`checker`), shops
   (`dollar`), threats (`harascar`) — from their world positions to map positions, assigning each a pooled
   icon sprite (C29.3).
3. **Rotates the 3-D map model** (C29.1) to match the player's heading, so "up" on the minimap is "forward"
   (the standard driving-minimap convention).
4. **Culls** points of interest outside the minimap's range (they reappear on the full-screen map, C29.4).

The world→map projection is the core operation: a linear transform from world XZ (C12) to map XY, calibrated
by the anchor points (C29.2). Once you have that transform, placing any icon is projecting its world position
through it.

**The runtime classes (✅ names / ⏳ offsets).** The map is driven by the HUD/GUI class set (C21/C23): `Hud*`
classes (`HudMissionObjective`, `HudMissionProgress`, C26.1) and the `CGui`/`Scrooby` UI runtime (C21.4/C21.5)
render it, and the map logic reads the player and world state. The **classes are ✅** verified; the **member
offsets** (where the map stores its transform, the player position it reads) are **⏳**, recovered by diffing
(C4.3).

**A real example — reading positions live.** The map reads the player's and objects' world positions every
frame, which is exactly the kind of runtime data the modding tools (C28) recover. The shipped `NoTrafficDiag`
mod (C28) demonstrates the technique on related systems: it identifies live `TrafficVehicle` and `RoadManager`
objects by their vtable (C23.5) and reads their state read-only. The same approach — identify the map/HUD
object by vtable, read its transform — is how a mod would hook the map. The classes are known (✅); the
offsets are the user's to recover and verify per build (C28).

**Why the map synthesises the whole book.** The map is the one screen that touches nearly every system: it
renders a **3-D model** (C7) with **textures** (C5) and **shaders** (C6), inside a **Scrooby UI** (C21),
showing **world positions** (C12) of **missions** (C16), **races** (C16.5), **shops** (C16.6), **traffic**
(C24), and **characters** (C25), driven by the **HUD runtime** (C26.1). To understand the map is to see how
the whole engine composes — which is why it's a fitting near-final chapter.

**What happens if you bend it.**

- *Miscalibrate the world→map transform* (wrong anchors, C29.2) — every icon and the player marker land in
  the wrong place. Keep the anchors and the transform consistent.
- *Rely on a map/HUD member offset* — classes ✅, offsets ⏳. Diff and re-verify per build (C4.3, C28).
- *Rotate the map the wrong way* — "up" no longer means "forward" and navigation becomes confusing. Match the
  rotation to the player's heading.

**Next:** [Chapter 28 — The Modding Toolchain](../C28-Modding-Toolchain/C28-Modding-Toolchain.md).
