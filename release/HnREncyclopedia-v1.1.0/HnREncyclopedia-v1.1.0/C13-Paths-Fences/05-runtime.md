# C13.5 — Traffic, GPS & Routing at Runtime

**What it is.** How the invisible driving data (C13.1–C13.4) becomes live behaviour: the traffic that fills
the streets, the GPS route to your objective, and the containment that keeps you on the road.

**How it works.** Three consumers, each reading a different part of the family:

- **Traffic AI** reads the **road network** (C13.2) and **intersections** (C13.3): ambient cars spawn at
  road nodes (up to `SetMaxTraffic`, C14.5), follow lane edges, and negotiate junctions. This is what makes
  Springfield feel populated with cars going about their business.
- **The GPS** runs a **shortest-path search** over the same road graph to draw the on-screen route from the
  player to the current objective (C16). Every "drive to X" mission is a query on this graph.
- **Vehicle containment** reads the **fences** (C13.1): the physics system (C26) pushes a car back when it
  crosses a fence segment from the inside, keeping it on the road smoothly.
- **Scripted movement** reads **path segments** (C13.4): NPCs, chase cars, and cameras follow authored routes
  bound by name in mission scripts (C14.5).

**The runtime classes (✅ names / ⏳ offsets).** The RTTI set names the consumers: `AiVehicleController` and
the `CharacterAi` family (C25) drive traffic and chase behaviour; the vehicle/physics classes (C24/C26)
apply fence containment. Names and inheritance are **verified**; the exact fields where a car stores its
current road node or target path are **⏳**, recovered by diffing (C4.3).

**Why this is the driving game's backbone.** Everything that makes SHAR a *driving* game — traffic to weave
through, a GPS to follow, roads that contain you, chases that keep up — rests on this one invisible family.
The visible streets (C7, C12) are the stage; the road graph, fences, and paths are the machinery that makes
the stage a place you can drive. It parallels the collision system (C11): both are invisible geometry the
runtime tests against, one for *touching* the world, one for *driving* it.

**The modding consequence.** To change where traffic goes, edit the road graph (C13.2); to open or seal a
shortcut, edit the fences (C13.1); to route a scripted chase, edit a path (C13.4). Because the road data is
separate from the visible road, you can reshape driving behaviour without remodelling the streets — and
because the consumers are RTTI-verified classes, a native mod can identify them live (offsets ⏳).

**What happens if you bend it.**

- *Edit the mesh road but not the graph* — the street looks different but traffic still drives the old graph.
  Edit the graph to move traffic.
- *Rely on an AI/vehicle member offset* — it's ⏳; diff for it first (C4.3). Names are safe; offsets are not.
- *Seal every fence gap* — you remove shortcuts the game (or players) rely on. Change containment
  deliberately, and test that routes still work.

**Next:** [Chapter 12 — Level Composition](../C12-Level-Composition/C12-Level-Composition.md).
