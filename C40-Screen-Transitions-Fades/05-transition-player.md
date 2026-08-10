# C40.5 — `TransitionPlayer` & choreo::Transition

> What actually *runs* a transition over time: `TransitionPlayer` consuming `TransitionEvent`s,
> with `choreo::Transition` / `tStateTransition` on the animation-state side.

## The players (✅ verified)
- **`TransitionPlayer`** (`0x00610D20`) — drives a transition sequence frame by frame, raising
  its `TransitionEvent`s (`0x00610DEC`) at the right times. `TransitionEvent`s come from a fixed
  event pool (C39.3), which is why a very dense scripted sequence can exhaust it.
- **`choreo::Transition`** (`0x005FE57C`) — the choreography segment that blends one animation
  state into another (used by NIS/cutscene playback, C17/C34).
- **`tStateTransition`** (`0x005F8A6C`) — a state-machine edge; the low-level "move from state A
  to state B" used across animation and gameflow.

## How they fit together
```
mission/UI script ─► GuiSFX chain (C40.4) ─► TransitionPlayer ─► TransitionEvent(s)
                                                    │
world/interior swap (C41) ◄── Fader (C40.1) ◄───────┘  (START/END, C40.2)
animation blends ◄── choreo::Transition / tStateTransition (C34)
```
The GuiSFX chain decides *what* transition; the TransitionPlayer decides *when* each beat fires;
the Fader/iris/letterbox are *what the player sees*; choreo/state transitions handle the
*animation* side of a character or camera moving through the change.

## Why separate players
Screen transitions (fades) and animation transitions (blends) are different domains with
different timing needs, so they get different players sharing the same event/state vocabulary.

## What happens if you bend it
Hook `TransitionPlayer`'s update to retime or skip beats; watch the `TransitionEvent` pool if
you author long sequences (C39.3).

## Cross-references
C40.4 (GuiSFX), C40.1/40.2 (fader/events), C34 (animation channels), C17 (NIS), C39.3 (event pools).
