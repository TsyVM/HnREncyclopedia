# C19.5 — The Audio Frame & the HAL

**What it is.** How all the audio systems — positional sound (C19.2), music (C19.3), dialogue (C19.4) —
come together each frame and mix down to what you hear, through the RadSound HAL (C18.5). This closes the
audio chapters by showing the whole pipeline in motion.

**How it works.** Each frame, the audio systems update in concert:

1. **Positional players** (C19.2) update their world positions to follow their sources (cars, characters,
   gags), so pan and attenuation track the moving world.
2. **The music system** (C19.3) checks whether a game event calls for a transition and, via the stitch
   callback, keeps the streamed composition's buffer fed so it never gaps.
3. **The dialogue coordinator** (C19.4) advances its priority queue — starting the next line when the current
   finishes, dropping stale low-priority ones.
4. **The RadSound HAL** (C18.5) mixes every active voice: it takes each player's clip (decoding ADPCM where
   needed, C18.2), applies 3-D pan/attenuation from the `PositionCarrier`, applies **EAX reverb** for the
   current environment (`IRadSoundHalEffectEAX2Reverb`), and sums it all into the output buffer the hardware
   plays.

The result is the layered soundscape: engines and footsteps positioned in space, music responding to the
action, dialogue prioritised and clear, all reverberating appropriately for whether you're in a tunnel or an
open street.

**Why the HAL is the mixing point.** Every sound — a UI blip (C18.4), a car engine (C19.2), a music segment
(C19.3), a voice line (C19.4) — bottoms out at the same place: an `IRadSoundHalBuffer` in the HAL. Funnelling
everything through one HAL is what lets the engine apply consistent 3-D positioning and reverb, manage a
limited number of hardware voices, and run identically across platforms (C18.5). The game logic decides
*what* plays and *where*; the HAL decides *how it sounds coming out* — the clean separation that makes the
audio both portable and coherent.

**EAX and environment.** The EAX 2 reverb (`IRadSoundHalEffectEAX2Reverb`, tied to the shipped `eax.dll`,
C18.5) gives each environment its acoustic character — a reverberant tunnel (the Stonecutters Tunnel, C12.4),
a dead-sounding interior, an open street. The game selects a reverb preset for the area (🟡 — the presence of
EAX reverb is ✅; the per-area preset mapping is ⏳), and the HAL applies it to everything mixed there. This is
the audio equivalent of the visual streaming zones (C12.3): the *place* sets the reverb, and all sound in it
inherits that space.

**The whole audio picture.** Putting C18–C19 together: sounds are **RSD** samples (C18), packed by category
into **seven archives** (C19.1), played by **positional players** (C19.2) that follow the world, layered with
**interactive music** (C19.3) and **prioritised dialogue** (C19.4), and mixed through the **RadSound HAL**
(C18.5) with **EAX** environmental reverb. Every class is ✅ verified; the tuning curves (RPM→engine,
area→reverb) are the ⏳ frontier.

**What happens if you bend it.**

- *Add many simultaneous sounds* — the HAL has finite hardware voices; over-subscribing drops or steals
  voices. Respect the voice budget (the priority queue, C19.4, exists partly for this).
- *Rely on a HAL/reverb offset or preset* — classes ✅, the per-area preset mapping ⏳. Diff/correlate (C4.3).
- *Bypass the HAL for a "direct" sound* — you lose positioning and reverb consistency. Route through the HAL.

**Next:** [Chapter 20 — Bink Video](../C20-Bink-Video/C20-Bink-Video.md).
