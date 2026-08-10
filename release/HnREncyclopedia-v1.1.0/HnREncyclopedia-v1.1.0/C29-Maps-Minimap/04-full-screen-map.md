# C29.4 — The Full-Screen Map

**What it is.** The pause-menu map — `ViewMap.pag` / `ViewMap.scr` — the full-screen view of the level you
open to plan a route. It's the minimap's big sibling: the same per-level map model (C29.2), shown large with
the full set of markers and teleport destinations.

**How it works (✅ verified).** `ViewMap.scr` is a screen (C21.1) holding `ViewMap.pag`, opened from the pause
menu (via `CGuiScreenPauseMission`, C21.5). It draws the current level's `l{N}hudmap.p3d` model (C29.2)
filling most of the screen, with map icons (C29.3) at their world positions and — crucially — the level's
**teleport destinations** (C12.4). Where the minimap (C29.1) is a small always-on navigation aid, the
full-screen map is a *planning* view: bigger, static (not rotating with you), and showing the whole level at
once.

**The teleport tie.** The `AddTeleportDest` entries from `level.mfk` (C12.4) — the 12 named Springfield
locations (Simpsons' House, Kwik-E-Mart, Church, …) with their coordinates — are what the full-screen map
offers as fast-travel points. Select a destination on the map and the game streams that location's zones/roads
(C12.3) and moves you there. So the full-screen map is the UI front-end to the teleport system: the map shows
the destinations, and picking one drives the streaming (C12.3). This is why the map and the level's streaming
plan are two views of the same data — the `AddTeleportDest` list is both.

**Why two maps (minimap + full-screen).** They serve different needs. The **minimap** (C29.1) is *situational
awareness* — always visible, rotates with you, shows nearby points of interest — for moment-to-moment
navigation while driving. The **full-screen map** is *planning and fast-travel* — you stop, open it, see the
whole level, and choose where to go. One is for driving, one is for deciding. Both draw the same 3-D map model
(C29.2) and icon vocabulary (C29.3), so they're consistent, but their framing and interaction differ. This
mirrors the general HUD-vs-menu split (C21.5): in-game overlay vs. paused full-screen.

**Reading it.** The full-screen map inventories a level's content spatially: every mission phone, race,
shop, and collectible as an icon, plus the fast-travel points. Dumping `ViewMap.pag` and cross-referencing
its icons with the level's missions (C16) and `AddTeleportDest` (C12.4) reconstructs the level's whole
"things to do" map — which is exactly what it shows the player.

**What happens if you bend it.**

- *Add a teleport destination in `level.mfk` but not reflect it* — the full-screen map is driven by that data
  (C12.4); keep them in sync.
- *Confuse the minimap and full-screen map pages* — `HudMap.pag` is the overlay, `ViewMap.pag` the pause map.
  Edit the right one.
- *Rely on a map/HUD member offset* — the classes are ✅, offsets ⏳ (C29.5). Diff (C4.3).
