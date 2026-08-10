# C30.4 — The `LoadingManager` & Streaming

**What it is.** The engine that does the actual work during a loading context (C30.3): `LoadingManager`,
which streams a level's assets into memory, and its relationship to the residency system (C12.3) and the
world it hands to `GameplayManager`.

**How it works (✅ verified).** `LoadingManager : FileHandler::LoadFileCallback` (0x00613A7C) processes
asynchronous file-load requests. During a loading context it:

1. **Reads the load list** — the level and mission scripts' `LoadP3DFile`/`LoadDisposableCar` calls (C14.2)
   enumerate every asset the level needs.
2. **Requests each file through the VFS** (C3.6) — resolving loose-or-packed, streaming from disc.
3. **Builds objects via the loader** (C1.8/C23.4) — each `.p3d` becomes live objects (meshes, textures,
   characters, collision) through the chunk-handler registry.
4. **Reports progress** — feeding the loading screen (C30.3) so the bar advances.
5. **Signals completion** — when residency is satisfied, it tells `GameFlow` to advance to gameplay.

`GameplayManager : EventListener` (0x00612D00) then owns the running world — the loaded objects, the active
mission (C16), the population (C24/C25).

**The streaming residency (recap, C12.3).** Loading isn't only at level start — the world **streams** as you
move (C12.3): zones (`l{level}z*`) and roads (`l{level}r*`) load and free by proximity. `LoadingManager`
handles the initial bulk load in the loading context; the in-play streaming (loading the next zone as you
drive toward it, freeing the one behind) is the same machinery running continuously during
`GameplayContext`. So there are two loading regimes: the **upfront** load (loading screen) and the
**continuous** stream (seamless, no screen). Both go through `LoadingManager`; the difference is only whether
`GameFlow` is waiting on it (loading context) or the world is already running (gameplay context).

**Why asynchronous.** `LoadingManager` is a *callback*-based async loader (`LoadFileCallback`) precisely so
loading doesn't block the frame. During the loading screen, the engine keeps drawing and stays responsive
because loads happen asynchronously and report back via callbacks. During gameplay, this is essential — the
world must keep running at frame rate while the next zone streams in, so the load *cannot* block. The async
design is what makes SHAR's world feel seamless while driving (C12.3): you never see a load screen mid-level
because `LoadingManager` streams zones in the background of `GameplayContext`.

**The modding consequence.** Everything you add to a level goes through `LoadingManager`: a new car
(`LoadDisposableCar`), a new prop (`LoadP3DFile`), a bigger texture. All of it extends load time (upfront) or
streaming cost (in-play) and consumes residency budget (C12.3). This is why heavy mods lengthen loading
screens and can stutter while streaming — you've given `LoadingManager` more to do. Budget assets against the
residency the level can hold (C12.3), and prefer streaming-friendly sizes.

**What happens if you bend it.**

- *Add assets without budgeting residency* — longer loads and stream stutters (C12.3). Respect the budget.
- *Rely on a `LoadingManager`/`GameplayManager` offset or singleton address* — classes/vtables ✅, offsets and
  instance pointers ⏳. Diff (C4.3).
- *Assume all loading is upfront* — much is continuous streaming (C12.3). Distant/late assets load as you
  approach.
