# C49.3 — Why the Manager Pattern

> Why did Radical build the whole runtime as manager singletons? Because in 2003, for a big
> open-world game, it's the pragmatic architecture that gives clarity without ceremony.

## The reasons (✅ reasoned)
- **Clear ownership.** Every object has exactly one owner (its manager), so lifetime is
  unambiguous — no "who frees this?" bugs. Level unload = destroy the managers = everything freed.
- **One update site.** The frame loop calls a fixed list of manager updates in a known order. The
  whole game's per-frame behaviour is legible in one place, and ordering (physics→render) is
  explicit.
- **One access point.** Any code that needs traffic asks `TrafficManager`; there's no searching or
  passing pointers everywhere. Singletons make cross-subsystem access trivial.
- **Encapsulation.** Each subsystem's complexity is hidden behind its manager's interface; the rest
  of the game treats it as a black box.
- **Cheap.** No dependency-injection framework, no message bus for the common path — just objects
  with an `Update()`. Perfect for the era's constraints.

## The trade-offs (honest)
- **Global state.** Singletons are globals; they make testing and reasoning about coupling harder,
  and any code can reach any manager.
- **Order coupling.** The fixed update order is an implicit dependency graph — fragile to reorder.
- **A single point of failure.** Everything in a subsystem flows through its manager, so a bug (or a
  bad hook) there takes the whole subsystem down (C49.6).

For a shipped 2003 title these trade-offs are the *right* call: simplicity and clarity beat purity.

## Why it's good news for modders
The same properties that make managers a clean architecture make them a **great hook surface**: one
object, one update, one access point per subsystem. Change the manager, change the whole subsystem —
which is exactly the leverage C49.5 exploits (and C49.6 warns about).

## Cross-references
C49.5/49.6 (the modding consequences), C30 (the update loop), C39 (the pools), the SDK design notes.
