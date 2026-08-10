# C13.2 — The Road Network (`0x03000003`)

**What it is.** The graph the game's cars and GPS actually drive on: a network of **road nodes** linked
along the streets, with **intersections** where they meet. It is the AI's map of the drivable world —
invisible, but the reason traffic flows and the GPS can route you to a mission.

**How it works (✅ verified).** The `0x03000003` chunk announces itself in plaintext: its data contains the
strings **`RoadNode`** and **`IntersectionLocatorNode`** (verified in `art/b01 - Copy.p3d`). It is a large
container (3,403 bytes in one instance) holding the named nodes of the road graph. A road node is a point on
a drivable road; edges connect adjacent nodes into the lanes cars follow; intersection nodes (C13.3) are the
junctions. Together they form a directed graph — the same structure as a GPS road map.

**Why a separate graph from the visible road.** The visible street is a mesh (C7); the *drivable* road is a
graph. Traffic AI (C25) doesn't drive on triangles — it follows the graph's nodes and edges, which encode
lane direction, connectivity, and speed. Separating the two means the road can *look* however the artists
want while the AI drives a clean, simple network underneath. It also makes routing tractable: finding a path
from A to B is a graph search over hundreds of nodes, not a geometric problem over the whole world. This is
why the GPS can instantly draw a route — it's a shortest-path query on this graph.

**What the graph carries.** Node positions (where on the road), connectivity (which nodes link), and — by the
`IntersectionLocatorNode` naming — special junction nodes. Directionality and lane data let traffic keep
right, turn at junctions, and avoid driving the wrong way. The precise per-node field layout is 🟡 (the
strings and structure are verified; the exact numeric fields are partially decoded), but the *nature* of the
data — a named, connected road graph — is certain from the embedded strings.

**What happens if you bend it.**

- *Delete a road node mid-street* — traffic and GPS routing break at that point; cars vanish or stall. The
  graph must stay connected along every drivable road.
- *Disconnect an intersection* — routes that needed that junction fail; the GPS can't path through. Keep
  junction connectivity intact (C13.3).
- *Assume cars follow the visible road* — they follow the *graph*; if the graph and the mesh disagree, cars
  drive where the graph says. Edit the graph to change where traffic goes.
