# C12.6 — Assembling a Level End-to-End

**What it is.** The whole composition in one view: every piece of a level and the order it comes together,
from terrain to a playable, populated world. This page ties Chapters 5–15 into a single assembly.

**The assembly, in order.**

1. **Terrain** (`L*_TERRA.p3d`, C12.1) — the ground mesh (C7) and its collision (C11); always resident while
   the level is active.
2. **World blocks** (`b**.p3d` + `data` + LODs, C12.2) — the level's regions, split for streaming and detail.
3. **The `level.mfk`** (C12.4) runs: it declares the **missions** (`m0`–`m7`), **bonus missions**, **teleport
   destinations** (with their streaming sets), **vehicle-select info**, and the level's **gags** (C12.5).
4. **Streaming** (C12.3) begins: the zones (`l{level}z*`) and roads (`l{level}r*`) near the player load; as
   you move, the streamer swaps them by proximity, keeping shared roads resident across transitions.
5. **Content resolves**: each mission's `m{N}l.mfk` load file (C14.2) pulls its props, characters (C8), and
   **disposable cars** (`LoadDisposableCar` → a `.p3d` mesh + a `.con` handling, C7/C15); the road graph and
   fences (C13) route traffic and contain it; locators (C8.4) anchor spawns, triggers, and effects.
6. **Population**: traffic fills the roads (`SetMaxTraffic`, C14.5) on the road graph (C13.2); pedestrians and
   ambient NPCs spawn at locators; the gags stand ready.
7. **Play**: the scene graph (C10) draws it all each frame; collision (C11) makes it solid; the mission system
   (C16) runs whichever mission you start.

**Why this order.** Each step depends on the previous: content can't stream without blocks to stream; missions
can't load props without the level script declaring them; traffic can't route without the road graph the
blocks carry. The `level.mfk` sits at the centre because it is the manifest that turns a pile of assets into a
*level* — it decides what exists, where you can go, and what's alive. Everything before it is raw world;
everything after it is the world in motion.

**The whole-book view.** A level is where every chapter meets: textures (C5) on shaders (C6) on meshes (C7),
skinned characters (C8) arranged by the scene graph (C10), made solid by collision (C11), driven on by the
road network (C13), populated and sequenced by MFK scripts (C14/C16) with cars tuned by CON (C15), and
streamed by zone (C12.3). To read a level is to read the whole engine at once — which is why this chapter sits
where the format chapters (Parts I–III) hand off to the scripting and runtime chapters (Parts IV–VII).

**What happens if you bend it.**

- *Change one layer and forget the others* — a level is a composition; a new prop needs loading (C14.2), a
  locator to sit on (C8.4), maybe collision (C11) and a streaming home (C12.3). Trace the whole chain.
- *Break the load order* — content that loads before the block it belongs to has nowhere to go. Respect the
  terrain → blocks → level.mfk → streaming → content → population order.
- *Test only up close* — LODs and streaming mean distant and just-loaded content behaves differently. Test
  across the level, at distance and through transitions.

**Next:** [Chapter 16 — Mission Structure & Objectives](../C16-Missions-Objectives/C16-Missions-Objectives.md).
