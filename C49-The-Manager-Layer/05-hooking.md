# C49.5 — Hooking a Manager

> A manager is one object with a known vtable, so it's the highest-leverage hook in the game: hook
> it once, change a whole subsystem. Here's how to do it safely with DonutsSDK + VanHooks.

## The two useful hook points
1. **The manager's `Update()`** — runs every frame. Hook it to observe or alter a subsystem each
   tick (e.g. cap `ChaseManager` heat, freeze `TrafficManager` spawns, tweak `PedestrianManager`
   density). Call the original, then/before do your work.
2. **A specific method** — e.g. `CoinManager::Collect`, `HitnRunManager::AddHeat`,
   `InteriorManager::Enter`. Hook it to intercept one operation without touching the rest.

## The recipe (DonutsSDK + VanHooks)
```cpp
#include <donutsdk/mod.hpp>
#include <vanhooks/vanhooks.hpp>
using namespace donutsdk;

// 1) DonutsSDK gives the confirmed vtable for the manager class:
const auto* cls = shar::db::find_class("ChaseManager");     // 0x006077FC
void** vt = reinterpret_cast<void**>(shar::process().rebase(cls->vtable_va));

// 2) recover the Update slot (SAHRDiag / vtable layout, C28.7) — build-specific:
constexpr std::size_t kUpdateSlot = /* recovered */ 0;

// 3) VanHooks installs the VTable hook (both use Result<T>):
auto& eng = vanhooks::global_engine();
eng.hook_vtable({ .vtable=vt, .slot_index=kUpdateSlot, .tag="ChaseManager::Update" },
                &hk_update, reinterpret_cast<void**>(&orig_update));
```
In `hk_update`, **call `orig_update` unless you deliberately intend to replace it**, and keep your
work fast (you're on the main thread inside the frame loop).

## Get the live singleton
To *read* a manager's state, get its live instance: the live-object scan / `shar::identify` finds
the one object whose vtable is the manager's (C28.7). From there, walk its owned-object list using
the recovered member offsets.

## Discipline
- Recover slot indices and offsets **per build** (addresses are build-specific).
- Prefer a **VTable hook** (non-destructive, reversible) over byte patching a manager.
- Keep the detour cheap and exception-free; remove the hook on unload.

## Cross-references
C28.5 (VanHooks/hooking), C28.7 (finding the live manager + offsets), C49.6 (what breaks if you get
this wrong), C49.2 (the update you're hooking).
