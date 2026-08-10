# C17.4 — NIS: In-Engine Cutscenes

**What it is.** The system for **Non-Interactive Sequences** — SHAR's *in-engine* cutscenes, where characters
act out scripted scenes using the real game engine (not pre-rendered video). NIS is distinct from the Bink
FMV of C20: FMV is a video file played back; NIS is the live engine choreographing real characters.

**How it works (✅ verified).** The NIS system and its data are both real and confirmed:

- **`nis.rcf`** — a real 88 MB `RADCORE CEMENT LIBRARY` archive (verified magic + size) holding the cutscene
  data.
- **`art/nis/`** — 130 loose NIS asset files (verified on disk).
- **Verified RTTI classes** (`shar_dumps.csv`):

```
NISPlayer / NISPlayerGroup      — play a cutscene (a group of coordinated players)
NISEvent                        — a timed event on the cutscene's timeline
NISSoundPlayer                  — the cutscene's audio (C19.2)
CameraPlayer : SimpleAnimationPlayer, AnimationPlayer   — the scripted camera (C26.3)
ChoreoFileHandler               — loads the .cho choreography (C17.1)
```

An NIS coordinates several systems along a **timeline**: `choreo::` puppets (C17.1–C17.3) act out the
character performances, a `CameraPlayer` runs the scripted camera move, a `NISSoundPlayer` plays the audio
(voice/music/effects, C19), and `NISEvent`s fire at timed points to trigger actions. The `NISPlayer`/
`NISPlayerGroup` drive the whole thing. This is the runtime of the mission scripts' cinematic verbs
(`SetConversationCam`, `SetAnimatedCameraName`, dialogue, C14.6) — those verbs stage an NIS.

**NIS vs. FMV — two kinds of cutscene.** SHAR uses both, for different needs:

- **NIS (in-engine, this page)** — real-time, uses the actual characters and world, can reflect game state
  (your car, your costume), and is cheap on disc (it's choreography data, not video). Used for most story
  and mission scenes — conversations, mission intros, character moments.
- **FMV (Bink video, C20)** — pre-rendered, fixed, higher-fidelity, larger on disc. Used for the polished
  set-pieces and the logos (C20.2).

The choice mirrors the general engine-vs-video trade (C20.2): NIS for interactive, state-aware, frequent
scenes; FMV for the few showcase moments. That the game has a whole in-engine cutscene system (`NISPlayer`
et al.) *and* a video system (C20) is why its storytelling feels seamless — most scenes are live NIS, so
they blend into gameplay without a jarring cut to video.

**What's verified — and the "NIS format" resolved (✅).** The **NIS classes** (✅ from RTTI) and the
**`nis.rcf` archive + `art/nis/` assets** (✅ on disk) are confirmed. A later pass **resolved what was
earlier flagged as an open "NIS byte format": there is no bespoke NIS format** — NIS is a *composition* of
already-decoded formats:

- **`nis.rcf`** contains **240 members, all `RSD4PCM` sound files** (✅ verified by extraction) — it is the
  cutscene **audio** (voice/sound), decoded in [C18](../C18-RSD-Sound/C18-RSD-Sound.md). Not a timeline format.
- **`art/nis/*.p3d`** are **130 standard Pure3D files** (✅ verified — geometry `0x00011003`, collision
  `0x00121xxx`, and the animation chunks `0x00004501/3/4`) — the cutscene **assets and animations**, decoded
  via [C1](../C1-Pure3D-Container-Model/C1-Pure3D-Container-Model.md), [C8](../C8-Skeletons-Locators/C8-Skeletons-Locators.md),
  and the channel system ([C34](../C34-Animation-Channels/C34-Animation-Channels.md)).
- **The runtime logic** is `choreo::` (this chapter) + the mission scripts ([C14](../C14-MFK-Scripts/C14-MFK-Scripts.md)).

So an NIS is: Pure3D assets + RSD audio + choreography + script — every part already documented. The earlier
"⏳ NIS format" was a misconception (assuming `nis.rcf` held a bespoke timeline); it does not. **Resolved.**

**What happens if you bend it.**

- *Confuse NIS with FMV* — NIS is in-engine choreography (this page), FMV is Bink video (C20). Editing one
  doesn't touch the other.
- *Rely on an NIS class offset or the NIS file format* — classes ✅, but member offsets and the `nis.rcf`
  data format are ⏳. Diff/decode before relying on them (C4.3).
- *Expect an NIS to ignore game state* — unlike FMV, an NIS uses the live characters/world, so it reflects
  state. That's its advantage; account for it.
