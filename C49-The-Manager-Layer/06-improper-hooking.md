# C49.6 — Improper Hooking: What Breaks

> A manager is the most powerful hook target *and* the most dangerous, because an entire subsystem
> flows through it. Here are the specific ways manager hooks go wrong — and how to avoid each.

## 1. Not calling the original `Update()` → the subsystem freezes
A manager's `Update()` *is* the subsystem's per-frame work. If your detour returns without calling
the original, that subsystem **stops**: hook `TrafficManager::Update` and skip it → traffic freezes;
skip `ChaseManager::Update` → the police stop reacting; skip `PedestrianManager::Update` → the crowd
locks in place. **Fix:** always call the original unless total replacement is your goal.

## 2. Wrong slot index → you hook the wrong method
Vtable slot indices are **build-specific**. Hard-code the wrong slot and you replace some other
virtual (maybe the destructor) with your detour — instant crash or corruption. **Fix:** recover the
slot from *this* build (SAHRDiag, C28.7); fail gracefully if the class/slot isn't found.

## 3. Corrupting `this` or its owned list → mass object loss
The manager holds the pool/list of everything it owns. Writing a wrong offset (a guessed member) can
corrupt that list — now every pedestrian/coin/car it owns is leaked or dangling, and the next update
walks garbage. **Fix:** only use **verified** member offsets (C28.7); never guess into a manager.

## 4. Reentrancy / calling back into the manager
Calling a manager method from inside your hook of that same manager can re-enter mid-update and
corrupt its iteration (e.g. spawning during its spawn loop). **Fix:** don't mutate a subsystem from
inside its own update hook; queue the change for after.

## 5. Wrong thread / timing
Managers tick on the **main thread** in a fixed order (C49.2). Touching a manager from another
thread, or installing the hook at a bad time (during load, before the singleton exists), races the
frame. **Fix:** install from a safe point (C28.5 safe-timing), operate on the main thread, and
null-check the singleton (it may not exist yet).

## 6. Breaking the update order
Some managers depend on others having ticked first (physics before render; input before gameplay).
A hook that delays or reorders an update can desync the frame — objects read stale positions, the
HUD lags the world. **Fix:** don't change *when* a manager ticks; only change *what* it does within
its tick.

## The golden rule
A manager hook has blast radius = its whole subsystem. **Call the original, use verified
offsets/slots, stay on the main thread, don't re-enter, and make it cleanly removable.** Test in a
throwaway session; a bad manager hook doesn't misbehave quietly — it takes the subsystem (or the
game) down.

## Cross-references
C49.5 (doing it right), C28.5/28.7 (safe timing + verified offsets/slots), C49.2 (the update &
ordering you must respect), C39 (the pools a corrupted manager leaks).
