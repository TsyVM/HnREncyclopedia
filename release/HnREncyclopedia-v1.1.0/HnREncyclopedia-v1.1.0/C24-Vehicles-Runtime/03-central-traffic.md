# C24.3 — `VehicleCentral` & Traffic

**What it is.** The management layer above individual cars: `VehicleCentral`, which loads and tracks
vehicles, and `TrafficVehicle`, the ambient-traffic car type that populates the roads. Together they run the
*population* of vehicles rather than any single car.

**How it works (✅ verified).** From `shar_dumps.csv`:

```
VehicleCentral : LoadingManager::ProcessRequestsCallback      — the vehicle manager
TrafficVehicle                                                 — an ambient traffic car
AIVehicleSoundPlayer : VehiclePositionalSoundPlayer, …         — traffic/vehicle audio
```

`VehicleCentral` is a **manager singleton** (a loading-manager callback): it handles requests to load and
spawn vehicles, keeps the set of active cars, and coordinates the disposable cars missions request
(`LoadDisposableCar`, C14.2). `TrafficVehicle` is the type the ambient traffic system spawns to fill the
streets up to the `SetMaxTraffic` budget (C14.5), driven by `AiVehicleController`s (C24.2) over the road
network (C13.2).

**Why a central manager.** Vehicles are created and destroyed constantly — traffic spawns ahead and despawns
behind you, missions load disposable cars and free them. Centralising that lifecycle in `VehicleCentral`
means one place owns the budget (how many cars exist), the loading (pulling a car's mesh + `.con`), and the
recycling (freeing distant traffic). Without it, every spawner would manage memory independently and the car
population would be uncontrolled. The manager is what keeps the streets busy but bounded — the vehicle
equivalent of the streaming residency that bounds the world (C12.3).

**Traffic as a system.** A `TrafficVehicle` is a lightweight, AI-driven, disposable car: spawned near the
player, given an AI controller and a route on the road graph, and freed when it's far away. The `SetMaxTraffic`
value (C14.5) is `VehicleCentral`'s budget for how many exist at once. This is why raising `SetMaxTraffic`
raises both the liveliness and the cost — each traffic car is a full `Vehicle` (C24.1) with physics,
collision, and sound. The manager trades population against performance.

**The manager pointer (⏳).** `VehicleCentral` is a singleton, and its **address is ⏳** — a mod that wants to
enumerate live vehicles needs that pointer, which is recovered by disassembly/diffing (C4.3), not from RTTI
(C23.1). The *class* is verified; the *instance address* is the open part. Once found, it's the entry point to
"every car in the world."

**What happens if you bend it.**

- *Raise `SetMaxTraffic` far beyond retail* — `VehicleCentral` spawns more full `Vehicle`s; memory and CPU
  rise and can stutter. Raise it in steps and test (C14.5).
- *Rely on the `VehicleCentral` singleton address* — it's ⏳; recover it for your build before using it.
- *Assume traffic cars are "fake"* — they're full `Vehicle`s (C24.1). Editing the vehicle model/handling
  affects traffic too.
