# C25.2 — The `CharacterAi` State Machine

**What it is.** The finite state machine that governs what a character is *doing* — walking, riding, getting
in or out of a car, or ragdolling. It is the behavioural core of every person in the game, and it is verified
directly from the class set.

**How it works (✅ verified).** `CharacterAi::State` is a base with these confirmed subclasses in
`shar_dumps.csv`:

```
CharacterAi::State
  ├ Loco     — locomotion: walking / running on foot
  ├ InCar    — riding in / driving a vehicle
  ├ InSim    — "in simulation": a physics body (ragdoll, knocked over)
  ├ GetIn    — transitioning into a vehicle
  ├ GetOut   — transitioning out of a vehicle
  └ NoState  — inactive / default (no active behaviour)
```

A character is in exactly **one** state at a time. The states are the nodes of an FSM and the natural
transitions are its edges:

```
NoState → Loco → GetIn → InCar → GetOut → Loco
                    Loco/InCar → InSim (on being hit)  → Loco (on recovery)
```

`GetIn`/`GetOut` are explicitly *transition* states — the character is mid-animation entering or leaving a
car — which is why they're their own classes: the transition has behaviour (play the enter/exit animation,
attach to the vehicle seat) distinct from the steady states around it.

**Why a state machine.** Character behaviour is naturally modal: you are either on foot *or* in a car *or*
ragdolling, never two at once, and the valid actions differ per mode. An FSM captures exactly this — one
active state, well-defined transitions — and makes the behaviour both correct (you can't drive while
ragdolling) and readable (six states describe the whole character). Making each state a *class*
(`CharacterAi::State` subclass) means each state owns its own update logic and its own entry/exit behaviour,
which is the object-oriented FSM pattern. The six states cover the entire on-foot/in-car/ragdoll loop that is
SHAR's moment-to-moment gameplay.

**The tie to gameplay and missions.** The states connect directly to systems you've decoded:

- **`InSim`** is the ragdoll — a `Character` becoming a pure `DynaPhysDSG` body (C25.1) when hit by a car.
- **`GetIn`/`GetOut`** are driven by the `getin`/`getout` mission objectives (C16.3) and the enter/exit
  animations (C8.2); entering swaps the character's control to the vehicle's controller (C24.2).
- **`Loco`** consumes the `.cho` locomotion animations (C8.2) and the IK rig (C8.1) so feet meet the ground.

So the state machine is the hub where the character's data (C8), the mission verbs (C16), and the physics
(C26) meet.

**What happens if you bend it.**

- *Assume a character can be in two states at once* — it's an FSM; one state at a time. Model behaviour as
  transitions, not overlaps.
- *Rely on a state class member offset* — the states are ✅, offsets ⏳. Diff (C4.3).
- *Force a transition the FSM doesn't allow* (e.g. `InCar`→`InSim` without a valid edge) — behaviour breaks.
  Respect the state graph.
