# C14.5 — Peds, NPCs, Traffic & Waypoints

**What it is.** The commands that fill the world with people and cars and tell them where to go. This is
what makes a Simpsons town feel inhabited — pedestrians on the sidewalks, traffic on the roads, named NPCs
for missions — and it is entirely script-driven and verified.

**Populating.**

- **`AddPed(...)`** (444) — place a generic pedestrian.
- **`AddNPC(...)`** (318) / **`AddAmbientCharacter(...)`** (122) — place a named or ambient character.
- **`CreatePedGroup(...)` / `ClosePedGroup()`** (116 each — balanced) and **`UsePedGroup(...)`** (134) —
  define and select reusable groups of pedestrians (a crowd type for an area).
- **`SetMaxTraffic(n)`** (136) — the traffic budget: how many vehicles the level spawns at once.
- **`AddNPCCharacterBonusMission(...)`** (81) — attach a bonus mission to an NPC.

**Routing (the locators/paths bridge).** People and cars move along routes anchored to the locators baked
into geometry (C8) and the path network (C13):

- **`AddSpawnPointByLocatorScript(...)`** (371) — spawn at a named locator in the world.
- **`AddAmbientNPCWaypoint(...)`** (473) / **`AddStageWaypoint(...)`** (442) /
  **`AddObjectiveNPCWaypoint(...)`** (189) — waypoint routes for ambient, stage, and objective movement.
- **`AddAmbientNpcAnimation` / `AddAmbientPcAnimation`** (547 / 570) and
  **`AmbientAnimationRandomize`** (264) — the idle/ambient animations that make crowds look alive.
- **`SetDestination(...)`** (216) — send a character/vehicle to a target.

**Why it's built this way.** Ambient life is expensive to author by hand, so SHAR describes it as data:
spawn points, waypoint routes, animation sets, and a traffic budget. A generic AI (C25) consumes those and
produces the moving world. Grouping (`…PedGroup`) lets one description populate many places. The result is
that a level's *feel* — busy downtown vs. quiet suburb — is tuned with a few numbers (`SetMaxTraffic`) and
a set of spawn/waypoint scripts, not code.

**The three-layer connection.** This page is where the book's layers meet: waypoints reference **locators**
(C8, baked into Pure3D), routes follow the **path network** (C13), and the movers are **AI-driven
characters and vehicles** (C25). MFK is the glue that binds baked geometry, path data, and runtime AI into
a living town.

**What happens if you bend it.**

- *Raise `SetMaxTraffic` far above retail* — more cars, but more memory and CPU; on constrained targets
  this can stutter or crash. Raise it in small steps and test.
- *Spawn at a locator that isn't in the loaded geometry* — the spawn fails silently. Ensure the named
  locator exists in a `LoadP3DFile`'d asset (C14.2).
- *Give an NPC a waypoint route that leaves the path network* — pathing AI (C25) may stall. Keep routes on
  the road/path graph (C13).
