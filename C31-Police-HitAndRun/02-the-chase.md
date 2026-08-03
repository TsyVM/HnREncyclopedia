# C31.2 — The Chase

**What it is.** What happens when the Hit & Run meter maxes out (C31.1): the police spawn and pursue you.
The chase is three verified classes plus an ordinary `Vehicle` — the police car is just a car with a pursuit
AI attached.

**How it works (✅ verified).**

```
ChaseManager : SpawnManager  (0x006077FC)  — spawns the pursuit vehicles
ChaseAI : VehicleAI          (0x00615F60)  — drives them after the player (C24.2)
ChaseCam : SuperCam          (0x006154B4)  — the pursuit camera (C26.3)
```

When `HitnRunManager` triggers, **`ChaseManager`** (a `SpawnManager`) spawns police cars near the player.
Each is a normal **`Vehicle`** (C24.1) — the verified roster includes **`cBlbart` "Black Ferrini (Chase)"**,
a fast black car built for pursuit — driven by **`ChaseAI`**, which is a `VehicleAI` (C24.2) specialised to
*hunt the player*: it reads the road network (C13) to route toward you, rams you to raise your heat further,
and keeps up through junctions. **`ChaseCam`** (a `SuperCam`, C26.3) frames the pursuit so you can see the
threat behind you.

To *lose* the chase you either destroy the police cars (they're destructible `Vehicle`s with hit points,
C15.5) or outrun them until the meter cools (C31.1) and `ChaseManager` despawns them.

**Why the police are "just a car with a chase AI."** This is the elegant part: SHAR doesn't build police as a
special object type — it reuses the `Vehicle`/`VehicleAI` machinery (C24). A police car is a `Vehicle` (same
physics, collision, handling, C24.1) with a `ChaseAI` controller (C24.2) instead of a traffic AI. This means
the police inherit everything cars already have — they crash, take damage, and drive on the same road graph —
and the *only* new part is the pursuit *behaviour* (`ChaseAI`) and the *spawning logic* (`ChaseManager`).
It's the controller pattern (C24.2) at its best: swap the AI, and a traffic car becomes a pursuer, no new
vehicle type needed. The distinct chase car (`cBlbart`) is a *content* choice (a menacing black car), not an
engine requirement.

**`ChaseManager` as a `SpawnManager`.** Being a `SpawnManager`, `ChaseManager` handles the *population* of
the chase — how many police, where they spawn (near you, on the road network, C13), and when they despawn (on
cooldown). This mirrors the traffic spawning (`VehicleCentral`/`TrafficVehicle`, C24.3): a manager that
maintains a bounded set of spawned vehicles. The chase is thus a *managed spawn* layered over the normal
vehicle system — which is why it can escalate (spawn more police as heat rises) and de-escalate (despawn on
cooldown) cleanly.

**What happens if you bend it.**

- *Rely on a `ChaseManager`/`ChaseAI` member offset or the manager singleton* — classes/vtables ✅, offsets
  and instance pointers ⏳. Diff (C4.3).
- *Edit the chase car expecting it to change traffic* — `cBlbart` is a specific `Vehicle`; editing it changes
  the police car, not general traffic. Know which car you're editing (Catalogue).
- *Make the police invincible* — they're destructible `Vehicle`s by design (losing the chase depends on it).
  Raising their hit points (C15.5) too far breaks the "ram to escape" loop.
