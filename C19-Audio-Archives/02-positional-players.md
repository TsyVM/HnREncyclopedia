# C19.2 — Positional Sound Players

**What it is.** The system that places a sound in 3-D space and attaches it to a moving source, so a passing
car sounds like it's passing and a character's voice comes from where they stand. It's a verified hierarchy
of "sound players," each specialised for a kind of source.

**How it works (✅ verified).** From `shar_dumps.csv`:

```
SimpsonsSoundPlayer
  └ PositionalSoundPlayer
VehiclePositionalSoundPlayer : PositionCarrier
  ├ AIVehicleSoundPlayer      — AI/traffic car engines (C24.5)
  └ TrafficSoundPlayer        — ambient traffic, with a timer callback
AvatarSoundPlayer             — the player character
AnimObjSoundPlayer            — animated objects and gags (C14.4)
PlatformSoundPlayer           — moving platforms
NISSoundPlayer                — non-interactive sequences / cutscenes (C20)
```

The key base is **`PositionCarrier`** — it gives a sound player a world position, which the audio HAL (C18.5)
uses to pan and attenuate the sound (louder and centred when near, quieter and off to one side when far).
Each player subclass attaches to its source and updates that position each frame: a `VehiclePositionalSound
Player` follows its car, an `AvatarSoundPlayer` follows the player, an `AnimObjSoundPlayer` follows a gag's
animated object.

**Why a player per source type.** Different sources need different sound logic. A **vehicle** player picks
engine sounds by RPM/speed (from `carsound.rcf`) and follows the car; **traffic** players (with their
`IRadTimerCallback`) manage many ambient engines cheaply; an **avatar** player handles footsteps and voice;
a **gag** player fires a one-shot at a gag's location (C14.4). Making each a subclass of the positional base
means they all get 3-D placement for free (via `PositionCarrier`) and add only their source-specific
behaviour — the same inheritance economy as the DSG entities (C23.2).

**The tie to the world.** Positional sound is what makes Springfield feel *alive* rather than just *look*
alive (C25.5): every `TrafficVehicle` (C24.3) carries a `TrafficSoundPlayer`, so the streets you populated
with cars also hum with their engines; every gag (C14.4) has an `AnimObjSoundPlayer`, so the comedy has
sound. The population systems (C14.5) and the sound players are two halves of one living world — one places
the objects, the other gives them voice.

**Reading the RPM→engine bridge (🟡).** A vehicle's engine sound changes with revs — a real-time mapping from
the car's physics state (C26.5) to which engine sample plays and at what pitch. The classes involved
(`ICarSoundParameters`, `AIVehicleSoundPlayer`) are verified; the exact RPM→sample curve is ⏳, recovered by
correlating the car's speed with the sound (C4.3). The *system* is clear (positional player + car parameters
→ engine audio); the *tuning* is the open part.

**What happens if you bend it.**

- *Rely on a sound-player member offset* — classes ✅, offsets ⏳. Diff (C4.3).
- *Give a sound no position carrier* — it plays non-positionally (flat, centred), which is wrong for a world
  source. Attach it to a `PositionCarrier`.
- *Raise traffic without accounting for its sound* — each traffic car adds a `TrafficSoundPlayer` (C24.3);
  the audio cost scales with the population.
