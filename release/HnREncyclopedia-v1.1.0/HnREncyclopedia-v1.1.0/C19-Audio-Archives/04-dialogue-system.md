# C19.4 — The Dialogue System

**What it is.** The system that manages the game's voice — its single largest audio category (173 MB) — and
decides *which* line plays when several want to at once. Dialogue in a talkie comedy is constant and
competing, so it needs coordination, and SHAR gives it a priority queue.

**How it works (✅ verified).** From `shar_dumps.csv`:

```
DialogCoordinator : EventListener                                    — the manager
DialogPriorityQueue : DialogLineCompleteCallback, DialogCompleteCallback  — orders competing lines
DialogLine : PlayableDialog, SelectableDialog                        — one spoken line
DialogList, DialogSelectionGroup                                     — collections / random pools
DialogQueueElement : IRadTimerCallback, SimpsonsSoundPlayerCallback  — a queued line with timing
DialogueObjective : MissionObjective, EventListener                  — the "dialogue" mission objective (C16.3)
```

A **`DialogLine`** is one voice clip (an RSD in `dialog.rcf`, C18/C19.1). The **`DialogCoordinator`** (an
`EventListener`) receives requests to play lines from all over the game — mission dialogue (C14.6), ambient
character barks (C25.5), reaction lines — and feeds them to the **`DialogPriorityQueue`**, which decides the
order: a mission-critical line outranks an ambient one, and the queue holds or drops the losers. Each queued
line is a `DialogQueueElement` with timing (`IRadTimerCallback`) and a completion callback so the coordinator
knows when a line finishes and the next can play.

**Why a priority queue.** In a busy scene, many things want to speak: the mission NPC, passing pedestrians,
the player character reacting. Playing them all at once is cacophony; playing them first-come is wrong (an
ambient bark shouldn't cut off a mission line). A **priority queue** solves both — every line has a priority,
the most important plays, and lesser ones wait or are dropped. This is exactly the design a comedy game needs
to keep its constant chatter intelligible: the important line is always heard, the flavour lines fill the
gaps. `DialogSelectionGroup`/`DialogList` add *variety* — a random pool of lines so a repeated situation
doesn't say the identical thing every time.

**The mission tie.** `DialogueObjective : MissionObjective` is the runtime of the `dialogue` objective
(C16.3 — 139 uses, the second-most-common objective). So when a mission stage is "play this conversation,"
it constructs a `DialogueObjective` that feeds lines to the coordinator and completes when they finish. The
`talkto` objective (99 uses) similarly cues dialogue. This is why dialogue is the biggest archive: it's not
just cutscene voice — it's woven through the mission system as a core objective type.

**The subtitle/label tie.** Spoken lines pair with on-screen text via the localization labels (C22) and the
mission `SetDialogueInfo`/`SetStageMessageIndex` (C14.6/C16.2). The audio plays from `dialog.rcf`; the
matching subtitle comes from the string tables — two halves of one line, cued together.

**What happens if you bend it.**

- *Rely on a dialogue class offset* — classes ✅, offsets ⏳. Diff (C4.3).
- *Play lines without the coordinator* — you bypass the priority queue and get overlapping speech. Route
  dialogue through the coordinator.
- *Replace a line without matching its subtitle* — the audio and the on-screen text (C22) diverge. Update
  both.
