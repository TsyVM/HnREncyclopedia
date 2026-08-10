# C46.2 — Spawning onto the Road Network

> Traffic isn't placed — it's streamed onto the roads around you from the active traffic group.

## The mechanism (✅ reasoned from the road system)
The traffic system spawns cars on the **road/path network** (C13) near the player — ahead on the
lanes you're approaching — and despawns them once they fall far behind or out of view. It draws
model choices from the active traffic group (C46.1), weighted. The result is a moving bubble of
traffic that stays populated wherever you drive (the road-constrained version of the crowd bubble,
C45.2).

## Why on the road network
Traffic must obey lanes, intersections, and one-way streets, so it spawns and drives on the
**path/road data** (C13) rather than free space. That data (built from the world's path chunks)
is what gives traffic somewhere legal to go.

## Density & the cap
How many spawn is bounded by `SetMaxTraffic` (C46.4) and the vehicle/actor pools (C39). Near the
cap, no more spawn regardless of the group.

## What happens if you bend it
More/denser traffic needs a higher `SetMaxTraffic` and pool headroom (C39). If cars spawn but don't
drive correctly, the road/path data for that area is the suspect (C13).

## Cross-references
C13 (roads/paths), C46.1 (the pool), C46.4 (the cap), C39 (limits), C45.2 (crowd analogue).
