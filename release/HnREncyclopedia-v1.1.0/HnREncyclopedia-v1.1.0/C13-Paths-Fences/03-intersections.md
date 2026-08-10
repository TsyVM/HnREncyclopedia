# C13.3 — Intersections (`0x03000004`)

**What it is.** The junction nodes of the road network — where roads cross, merge, or branch. Intersections
are the decision points of the driving graph: where traffic turns, yields, and where the GPS chooses a
direction.

**How it works (✅ verified).** `0x03000004` carries the plaintext **`IntersectionLocatorNode2`** (verified in
`art/b01 - Copy.p3d`). An intersection is a special road node (C13.2) with **multiple connections** — three
for a T-junction, four for a crossroads — plus the data that governs how the junction behaves. Where an
ordinary road node has one incoming and one outgoing link (a lane), an intersection has several, and the
graph search (routing) and the traffic AI both treat it specially: it is where a route *decides* and where
traffic *negotiates*.

**Why intersections are their own node type.** A straight stretch of road is trivial — follow it. A junction
is where all the interesting driving-AI behaviour lives: choosing an exit, yielding to cross traffic, not
piling up. Marking junctions as a distinct node type (`IntersectionLocatorNode`) lets the AI apply junction
logic only where needed, and lets the router treat them as the branch points of its search. It also anchors
the GPS: a route is essentially a list of "at this intersection, take this exit" decisions, so the
intersections are the route's waypoints.

**The connection to gameplay.** Missions that involve driving to a location (C16) route the GPS across these
intersections; traffic density (`SetMaxTraffic`, C14.5) fills the roads between them; and the chase/pursuit
behaviour (cars following you) uses the graph to keep up through junctions. So the intersection graph, though
invisible, is what makes the driving *game* — not just the driving — work.

**What happens if you bend it.**

- *Reduce an intersection's connections* — some turns become impossible; traffic and routing avoid or fail at
  that junction. Preserve the junction's arms.
- *Add a road without linking it to an intersection* — the new road is unreachable by AI/GPS (an island in
  the graph). Connect new roads at a junction node.
- *Mislabel a junction as an ordinary node* — the AI won't apply junction logic and cars drive through each
  other or the wrong way. Keep intersections typed as intersections.
