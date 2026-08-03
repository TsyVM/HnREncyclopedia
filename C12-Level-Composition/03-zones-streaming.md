# C12.3 — Zones, Roads & Streaming

**What it is.** The residency system that decides which pieces of the world are in memory as the player moves.
The finest units are **zones** (`l{level}z{n}.p3d`) and **roads** (`l{level}r{n}.p3d`), and each location
declares the set it needs.

**How it works (✅ verified).** The `level.mfk` `AddTeleportDest` entries are the clearest evidence — each
names a location, its coordinates, and the exact zone/road blocks to make resident there:

```
AddTeleportDest("Simpsons' House",         220, 3.5, -172, "l1z1.p3d;l1r1.p3d;l1r7.p3d;");
AddTeleportDest("Kwik E Mart",             209, 3.6, -285, "l1z2.p3d;l1r1.p3d;l1r2.p3d;");
AddTeleportDest("Springfield Elementary",  -11, 0.7, -586, "l1z3.p3d;l1r2.p3d;l1r3.p3d;");
AddTeleportDest("Burns' Mansion",         -186, 3.5,  -96, "l1z4.p3d;l1r3.p3d;l1r4a.p3d;");
```

The naming is systematic: **`l{level}z{n}`** is a *zone* (a region of the world — the Simpsons' house area,
the Kwik-E-Mart area), **`l{level}r{n}`** is a *road* connecting zones. Fast-travelling to a destination loads
its listed set; driving between destinations streams the intervening zones and roads in and out by proximity.
Note the overlap — `l1r1` appears for both the Simpsons' House and the Kwik-E-Mart — because adjacent locations
share the roads between them, so the streamer keeps shared pieces resident across the transition.

**Why zones and roads separately.** A zone is a *place* (dense, detailed, where you do things); a road is a
*connection* (long, thinner, where you drive). Separating them lets the streamer keep the road you're on
resident while swapping the zones at either end — you're always driving *on* something even as the scenery
ahead loads and the scenery behind unloads. This zone/road split is the backbone of SHAR's seamless-feeling
world: there are no visible load screens while driving because the road under you is always resident and only
the zones stream.

**The residency budget.** Only a handful of zones and roads are resident at once — the ones near the player.
The `AddTeleportDest` sets (typically one zone + two roads) show the working-set size: small, bounded, and
overlapping at the edges so transitions are smooth. This is the same refcounted-residency idea as any
streaming engine: a block is kept while any nearby location needs it and freed when none do.

**What happens if you bend it.**

- *Add content to a zone that isn't listed for a location* — it won't be resident there and won't appear.
  Add the zone to the relevant `AddTeleportDest`/streaming set.
- *Remove a shared road from a destination's set* — the transition to an adjacent location loses the
  connecting road and may pop or gap. Keep shared roads in both sets.
- *Load every zone at once to "simplify"* — you blow the memory budget the streaming exists to respect. Work
  within the resident set.
