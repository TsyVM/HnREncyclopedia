# C14.6 — Cameras, Dialogue & Rewards

**What it is.** The commands that stage the cinematic and presentational side of a mission — the
conversation cameras, the spoken dialogue, the HUD icons, and the rewards a mission grants. This is the
layer that turns mechanical stages (C14.3) into a *scene*.

**Cameras.**

- **`SetConversationCam(...)`** (399) — frame a conversation between characters.
- **`SetAnimatedCameraName(...)`** (76) / **`SetAnimCamMulticontName(...)`** (76) — reference a scripted
  animated camera (a keyframed cutscene move).
- **`SetCamBestSide(...)`** (130) — pick the best framing side automatically.
- **`SetConversationCamDistance`, `SetConversationCamName`** and related — tune the framing.

These build on the RTTI camera family (`SuperCam`, `BumperCam`, `FollowCam`, `ChaseCam` — 33 classes,
C26; names ✅, offsets ⏳).

**Dialogue.**

- **`SetDialogueInfo(...)`** (138) — attach a dialogue line/exchange to a stage.
- **`SetDialoguePositions(...)`** (107) / **`SetTalkToTarget(...)`** (100) — who speaks, who they face.

Dialogue audio itself lives in `dialog.rcf` (173 MB, C19); these commands cue it. This is why the game's
single largest non-music archive is dialogue — a licensed comedy leans on its voices.

**HUD & presentation.**

- **`SetHUDIcon(...)`** (429) — the on-screen objective icon.
- **`SetPresentationBitmap(...)`** (69) — a mission's presentation image (the mission-intro art).
- **`SetParticleTexture(...)`** (119) — particle effects for the moment.

**Rewards.**

- **`BindReward(...)`** (147) — connect a mission to what completing it unlocks (a car, a costume, a card).
- **Reward files** — `e3rwrds.mfk`/`rewards.mfk` at the mission-tree root define the reward set.

**Why it's built this way.** Separating presentation verbs from logic verbs (C14.3) means a mission's
*what* (stages/objectives) and its *show* (cameras/dialogue/HUD) are authored independently — a designer
can rescore the cinematics of a mission without touching its mechanics, and vice versa. Binding rewards
through a single `BindReward` verb keeps the progression system in one place, so the game's unlock economy
is a readable graph of mission→reward edges.

**Why this closes the chapter.** With C14.1–C14.6 you have the whole MFK picture: files are organised by
role (C14.1), they load assets (C14.2), sequence missions into stages (C14.3), script comedy and pickups
(C14.4), populate and route the world (C14.5), and stage the cinematics and rewards (here). Every one of
these is plain, editable text with a verified vocabulary — which is why MFK, together with CON (C15), is
where most SHAR gameplay modding actually happens.

**What happens if you bend it.**

- *Cue dialogue that isn't in `dialog.rcf`* — the line is silent. Confirm the referenced dialogue exists.
- *Bind a reward that isn't defined* — the unlock does nothing. Define rewards in the reward files before
  binding them.
- *Over-script cameras in a fast mission* — cinematic cuts during action can disorient; use conversation
  cams for talk, not chases.

**Next:** [Chapter 16 — Mission Structure & Objectives](../C16-Missions-Objectives/C16-Missions-Objectives.md),
which builds on this to map the seven levels' full mission rosters.
