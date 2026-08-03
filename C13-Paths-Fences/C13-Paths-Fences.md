# Chapter 13 — Paths, Fences & Road Data

> **Goal of this chapter:** decode the `0x03000xxx` family — the invisible navigation and barrier geometry
> that keeps cars on the road, routes traffic and the GPS, and defines the drivable network. After this
> chapter you can read a level's road graph, its barriers, and its scripted paths.

Beneath the visible streets of Springfield sits a second, invisible world: the **road network** the AI and
GPS drive on, the **fences** that keep cars from leaving the road, and the **paths** scripts send characters
along. All of it is the `0x03000xxx` family, and all of it was decoded from `art/b01 - Copy.p3d`, a level
block carrying 49 fences and 37 path segments.

**Key finding (✅ verified):** the road system is a **named graph** — the `0x03000003` chunk literally
contains the strings `RoadNode` and `IntersectionLocatorNode` — and fences are **line-segment barriers**
stored as start point, end point, and normal.

---

## Deep-dive pages

- [C13.1 — Fences: Barrier Segments (`0x03000000`)](01-fences.md): the invisible walls, as line segments with normals.
- [C13.2 — The Road Network (`0x03000003`)](02-road-network.md): `RoadNode`s and the drivable graph.
- [C13.3 — Intersections (`0x03000004`)](03-intersections.md): `IntersectionLocatorNode`s and junctions.
- [C13.4 — Path Segments (`0x03000009`/`0x0300000B`)](04-path-segments.md): scripted routes for characters and events.
- [C13.5 — Traffic, GPS & Routing at Runtime](05-runtime.md): how AI cars and the GPS consume the graph.

---

## 13.1 Fences (✅ verified)

A `0x03000000` **Fence** is a barrier line segment. Verified own data from `art/b01 - Copy.p3d` (36 bytes,
9 floats):

```
start = (-29.83, 0.0, -29.35)
end   = (-29.92, 0.0,  34.73)
normal= (-1.0,   0.0,   …)
```

Two ground-plane points and a facing normal — an invisible wall segment. A level block holds **49** of them,
chaining into the barriers that keep cars on the streets and out of the scenery. [C13.1](01-fences.md).

## 13.2 The road network (✅ verified)

The `0x03000003` chunk is the **road graph**, and it says so in plaintext: its data contains the strings
**`RoadNode`** and **`IntersectionLocatorNode`**. This is the AI/GPS driving graph — nodes along the
drivable roads, linked into a network that traffic follows and the GPS routes across. [C13.2](02-road-network.md).

## 13.3 Intersections (✅ verified)

`0x03000004` carries **`IntersectionLocatorNode2`** — the junctions where roads meet. Intersections are
special nodes in the graph: they have multiple connections, they govern how traffic turns and yields, and
they anchor the GPS route decisions. [C13.3](03-intersections.md).

## 13.4 Path segments (✅ verified)

`0x03000009` is a **named path segment** (verified name `pCubeShape43`) carrying counts and float
coordinates — a scripted route, distinct from the road graph, that missions and events send characters and
cameras along (`SetDestination`, waypoints — C14.5). `0x0300000B` groups segments into a path.
[C13.4](04-path-segments.md).

## 13.5 Runtime

At runtime the road graph drives **traffic AI** (ambient cars, `SetMaxTraffic`, C14.5) and the **GPS**
(the on-screen route to your objective); fences feed the **vehicle containment** in physics (C26); path
segments feed **scripted movement**. The consuming classes are in the AI/vehicle RTTI set (`AiVehicleController`,
etc. — names ✅, offsets ⏳). [C13.5](05-runtime.md).

---

## Key takeaways

- The `0x03000xxx` family is the **invisible driving world**: fences, the road graph, intersections, and
  scripted paths.
- **Fences** (`0x03000000`) are line-segment barriers: start, end, normal (✅ verified coordinates).
- The **road network** (`0x03000003`) is a **named graph** — literally contains `RoadNode` /
  `IntersectionLocatorNode` — that traffic and GPS use.
- **Path segments** (`0x03000009`) are named scripted routes, separate from the road graph.
- Runtime consumers are the traffic/GPS/AI classes (names ✅, offsets ⏳; C25/C26).

**Next:** [Chapter 14 — MFK Level & Mission Scripts](../C14-MFK-Scripts/C14-MFK-Scripts.md) (already written), or [Chapter 12 — Level Composition](../C12-Level-Composition/C12-Level-Composition.md).
