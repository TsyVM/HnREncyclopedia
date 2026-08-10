# C13.4 — Path Segments (`0x03000009` / `0x0300000B`)

**What it is.** Named, scripted routes — distinct from the road graph — that missions and events send
characters, cameras, and objects along. Where the road network (C13.2) is *ambient* driving, path segments
are *authored* movement for specific gameplay.

**How it works (✅ verified).** A `0x03000009` Path Segment is **named** (verified `pCubeShape43`) and carries
counts and float coordinates — the points of a route. Decoded own data begins with the name, then counts
(`1, 1`), then coordinate floats. `0x0300000B` groups segments into a complete **Path**. The Maya-style name
(`pCube…`) shows these were authored as curves/shapes in the art tool and exported as navigation data — a
designer draws the route, and it becomes a path the game can follow.

**Why separate from the road graph.** The road network is for *traffic and GPS* — generic, ambient, driven by
AI. Path segments are for *specific scripted moments*: a character walking a set route, a chase car following
a designed course, a camera sweeping along a spline, an object on a track. These need *authored* paths, not
graph search — the designer wants the movement to follow *exactly this curve*, not the shortest route. Keeping
them separate means scripts (C14) can bind precise movement to a named path (`SetDestination`, the waypoint
commands, C14.5) without touching the ambient road system.

**How scripts use them.** A mission references a path segment by name to route an NPC or a mission vehicle;
the waypoint commands (`AddStageWaypoint`, `AddObjectiveNPCWaypoint`, C14.5) place route points that may lie
along these paths. Because the segments are named, the binding is by string — the same locator-style
indirection as spawn points (C8.4): author the path in the geometry, reference it by name in the script.

**Reading and authoring.** To find a level's scripted routes, walk for `0x03000009`/`0x0300000B` and read the
named segments and their coordinates. To add one, author the curve, export it as a path segment, and
reference it from a mission script. The float coordinates are the route in world space (read straight, with
the coordinate-boundary rule of C7.5 if exporting).

**What happens if you bend it.**

- *Reference a path name a script expects but that isn't loaded* — the scripted movement has no route and the
  character stalls (C14.5). Ensure the path's `.p3d` is loaded.
- *Confuse a path segment with a road node* — path segments are authored routes, not the ambient graph;
  editing one doesn't change traffic. Edit the right system for the effect you want.
- *Break a path's continuity* — a character following it stops or teleports at the gap. Keep segment
  endpoints connected within a path.
