# C49.2 — How Managers Work

> Every manager follows the same lifecycle: **create → tick → own → destroy**, wired into the main
> frame loop. Know the shape and you know how to observe or hook any of them.

## The lifecycle (✅ verified shape)
1. **Create.** At boot (engine managers) or level-load (`leveli.mfk`-driven ones like
   `ChaseManager`, C44), the manager singleton is constructed and registered.
2. **Tick.** Each frame, the main loop (GameFlow's GameplayContext, C30) calls each manager's
   **update** in a fixed order — physics before render, input before gameplay, etc. This is where
   the subsystem *happens*: peds walk, traffic drives, the chase escalates.
3. **Own.** Between ticks the manager holds its subsystem's state — the list/pool of objects it
   created, plus its own counters and settings.
4. **Destroy.** At level unload or shutdown, managers are torn down in **reverse** creation order,
   freeing their objects.

## Access (✅ reasoned)
Each manager is reached through a **global accessor / singleton pointer** (a `GetXManager()` or a
static instance). Code that needs the roads asks `RoadManager`; code that needs the mission asks
`MissionManager`. The SDK locates a live manager by its vtable (C28.7).

## The update order matters
Managers tick in a deliberate order because they depend on each other: input feeds gameplay;
physics/collision runs before things that read positions; render runs last. This ordering is why a
hook that reorders or skips a manager's update can desync the frame (C49.6).

## Ownership = the object list
A manager's most important field is its **collection** of owned objects (often an intrusive list or
a pool, C39). This is what the live-object scan sees (C28.7): the manager plus the objects hanging
off it. To enumerate a subsystem's objects, you walk the manager's list.

## Cross-references
C30 (the frame loop / contexts), C39 (the pools managers allocate from), C28.7 (finding a manager +
its objects live), C49.5 (hooking the update).
