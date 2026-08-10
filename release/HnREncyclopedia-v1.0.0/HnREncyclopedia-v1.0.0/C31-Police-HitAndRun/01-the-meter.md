# C31.1 — The Hit & Run Meter

**What it is.** The mechanic the game is named for: a "heat" meter that fills as you cause mayhem and, when
full, brings the police down on you. It's SHAR's version of a wanted level, and it's what gives the open
world stakes.

**How it works (✅ verified).** Two classes run it:

```
HitnRunManager : EventListener   (0x00608D3C)  — the logic
HudHitNRun : HudEventHandler     (0x0060DBDC)  — the on-screen meter
```

`HitnRunManager` is an `EventListener` (C23.3): it listens for "mayhem" events — smashing traffic vehicles
(C24.3), destroying property and gags (C14.4), hitting pedestrians (C25.5) — and fills the meter for each.
`HudHitNRun` shows the meter filling. When the meter reaches maximum, `HitnRunManager` triggers the chase
(C31.2), spawning police. If you *stop* causing mayhem, the meter cools down over time and the threat
subsides.

**Why a meter, not instant police.** A meter gives the player a *warning and a choice*. Rather than police
appearing the instant you bump a car, the meter fills gradually, so you can see the heat rising and decide:
back off and let it cool, or accept the chase. This is the classic open-world "heat" design (the *Most
Wanted* volume documents the same idea in its pursuit system) — a gradient of consequence rather than a
binary. It makes the world feel *reactive* (mayhem has visible, escalating consequences) without being
punishing (you get a chance to avoid the police). The cooldown is what lets you recover, so the game is a
loop of building and releasing heat rather than a permanent punishment.

**The event-driven design.** `HitnRunManager` being an `EventListener` (like the missions, C26.1) means it
reacts to the *same event stream* the rest of the game uses: a smashed traffic car emits an event, the
mission system might listen for it (a "destroy" objective, C16.3), and the Hit & Run manager listens for it
too (filling the meter). One event, multiple listeners — which is why causing mayhem can simultaneously
progress a mission *and* raise your heat. This shared-event design (C23.3) is what lets the systems interact
without knowing about each other.

**The tie to missions.** Whether the meter is active, and how sensitive, is tuned per mission by `SetHitNRun`
(C31.4, 78 uses) — some missions want the pressure of a possible chase, others (a peaceful delivery) suppress
it. So the meter isn't a fixed global; it's a mission-configurable pressure the designers dial per scene.

**What happens if you bend it.**

- *Rely on a `HitnRunManager` member offset or singleton address* — the class and vtable are ✅, offsets and
  the instance pointer ⏳. Diff (C4.3).
- *Assume the meter is always active* — missions can suppress it (C31.4). Check `SetHitNRun` for the mission.
- *Expect instant police* — it's a gradual meter with a trigger threshold and cooldown. Model the heat as a
  gradient.
