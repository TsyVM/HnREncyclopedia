# C25.5 — Pedestrians, NPCs & Traffic

**What it is.** The runtime of the ambient population — the pedestrians and NPCs that fill Springfield —
built from the same `Character` machinery (C25.1–C25.4) but spawned, budgeted, and routed as a *crowd*.

**How it works (✅ verified).** The population is created by the MFK commands you decoded (C14.5) and run by
the character runtime:

1. **Spawn.** `AddPed`, `AddNPC`, `AddAmbientCharacter`, and ped groups (`CreatePedGroup`/`UsePedGroup`,
   C14.5) create `Character`s (C25.1) at **locators** (C8.4) baked into the level geometry.
2. **Behave.** Each gets a `CharacterAi` (C25.2) starting in `Loco`, with ambient animations
   (`AddAmbientNpcAnimation`, `AmbientAnimationRandomize`, C14.5) so the crowd isn't uniform.
3. **Route.** Waypoints (`AddAmbientNPCWaypoint`, C14.5) send pedestrians along paths; NPCs walking routes
   follow the path/road data (C13).
4. **Budget.** `CharacterManager` (C25.3) keeps the population bounded — spawning near the player, freeing
   the distant — the character analogue of the traffic budget (C24.3).

`NPCharacter` (a mission-relevant person) and bonus-mission NPCs (`AddNPCCharacterBonusMission`, C14.5) are
the named characters missions attach to — the people you `talkto` (C16.3).

**Why the crowd matters.** A licensed comedy game lives on its world feeling *populated* by recognisable
characters. The runtime achieves this with the same `Character` class for everyone — the player, a mission
NPC, and a random pedestrian are all `Character`s — differing only in their controller (C25.3), their AI
goals, and whether a mission references them. This uniformity is efficient (one character system) and
flexible (any pedestrian could, in principle, be promoted to an NPC). The `choreo::` and animation-state
systems (C25.4) then give the crowd variety — different idles, costumes, and behaviours — so a shared class
doesn't mean identical people.

**The three-layer meeting point.** Ambient population is where the book's layers converge at runtime:
**locators** (C8.4, baked in geometry) provide spawn points; **paths/roads** (C13) provide routes;
**MFK scripts** (C14.5) provide the spawn/route/animation commands; the **`Character`/`CharacterAi`** runtime
(this chapter) provides the bodies and behaviour. A busy street corner is all four at once — which is why
"populate the world" touches so many chapters.

**What happens if you bend it.**

- *Raise the ped/traffic budget far beyond retail* — each is a full `Character`/`Vehicle` with physics and
  animation; the crowd gets expensive. Budget it (C14.5) and test.
- *Spawn at a missing locator or route off the path graph* — the spawn/route silently fails (C14.5/C8.4).
  Ensure locators and paths exist.
- *Rely on a runtime character offset* — classes ✅, offsets ⏳. Diff (C4.3).

**Next:** [Chapter 26 — Missions, Cameras & Physics at Runtime](../C26-Missions-Cameras-Physics/C26-Missions-Cameras-Physics.md).
