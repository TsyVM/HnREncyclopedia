# Chapter 40 — Screen Transitions, Fades & the Interior "Black Box"

> **Goal of this chapter:** decode the screen-covering effects — the fade-to-black "box" that
> wraps entering and leaving interiors/vehicles, the letterbox bars, the iris wipe, and the
> scripted `GuiSFX` sequencer that chains them. This is the answer to "what is that black
> overlay when Homer enters a building?"

When the player enters the Kwik-E-Mart (or is moved between world and interior), the screen
does not cut — it **fades through a black box** while the world swaps behind it. That effect is
a real, confirmed subsystem: a `Fader`, a set of GUI transition screens, and an event protocol
that synchronizes the fade with the interior load.

**Key finding (✅ verified from the exe):** the transition is **event-driven**. The engine
fires, to the in-game GUI manager, `EVENT_ENTER_INTERIOR_TRANSITION_START` →
`EVENT_ENTER_INTERIOR_TRANSITION_END` (and `EVENT_EXIT_INTERIOR_START/END`). Between START and
END the **`Fader`** (`0x0060B240`) covers the screen (the black box) while the interior is
swapped in; the matching END event tears it down. The related full-screen effects are their own
confirmed classes — `CGuiScreenLetterBox` (`0x0060EC24`), `CGuiScreenIrisWipe` (`0x0060ED20`,
which emits `EVENT_GUI_IRIS_WIPE_OPEN/CLOSED`), and `CGuiScreenIntroTransition` (`0x0060FA88`) —
all sequenced by the **`GuiSFX::*`** scripted-effect family via a `TransitionPlayer`
(`0x00610D20`) consuming `TransitionEvent`s (`0x00610DEC`).

---

## Deep-dive pages

- [C40.1 — The `Fader` & the Black Box](01-the-fader.md): the fade-to-black overlay and how it wraps a world swap.
- [C40.2 — The Interior Transition Event Protocol](02-transition-events.md): `EVENT_ENTER/EXIT_INTERIOR_*`, START→END synchronization with the load.
- [C40.3 — LetterBox & Iris Wipe](03-letterbox-iriswipe.md): `CGuiScreenLetterBox`, `CGuiScreenIrisWipe`, and `SetIrisWipe`.
- [C40.4 — The `GuiSFX` Sequencer](04-guisfx-sequencer.md): the chainable scripted-effect vocabulary (Show/Hide/GotoScreen/Pause/Transition…).
- [C40.5 — `TransitionPlayer` & choreo::Transition](05-transition-player.md): how a transition sequence is driven and timed.
- [C40.6 — Modding Transitions](06-modding.md): changing fade timing/colour, disabling the box, adding your own transition.

---

## 40.1 The Fader (✅ verified)

`Fader` (`0x0060B240`) is the screen-covering fade. In the SAHRDiag live capture it was present
as live instances (`Fader ×3`). It is what you *see* as the "black box": a full-screen quad
whose alpha ramps to opaque (hiding the swap) then back to transparent. [C40.1](01-the-fader.md).

## 40.2 The event protocol (✅ verified strings)

The exe contains the literal log lines:

```
CGuiManagerInGame <= EVENT_ENTER_INTERIOR_TRANSITION_START.
CGuiManagerInGame <= EVENT_ENTER_INTERIOR_TRANSITION_END.
CGuiManagerInGame <= EVENT_EXIT_INTERIOR_START.
CGuiManagerInGame <= EVENT_EXIT_INTERIOR_END.
```

START raises the fade and asks the InteriorManager (C41) to swap; END lowers it once the
interior is resident. This START/END bracketing is exactly why the black box lasts precisely as
long as the load. [C40.2](02-transition-events.md).

## 40.3 LetterBox & iris wipe (✅ verified)

`CGuiScreenLetterBox` draws cinematic bars (used for scripted moments/NIS). `CGuiScreenIrisWipe`
does the circular iris open/close and emits `EVENT_GUI_IRIS_WIPE_OPEN` / `..._CLOSED`; the
script command `SetIrisWipe` triggers it. [C40.3](03-letterbox-iriswipe.md).

## 40.4 The GuiSFX sequencer (✅ verified family)

`GuiSFX::*` is a family of ~25 confirmed **chainable scripted effects** — `Show`, `Hide`,
`GotoScreen`, `Pause`/`PauseInFrames`, `Transition`, `IrisWipeOpen`, `ColorChange`,
`PulseScale`, `Translator`, `SendEvent`, `SwitchContext`, mission verbs
(`RestartCurrentMission`, `AbortCurrentMission`, `ResumeGame`), and `Junction`/`Chainable`
plumbing. They compose front-end and transition sequences. [C40.4](04-guisfx-sequencer.md).

## 40.5 The transition player (✅ verified)

`TransitionPlayer` (`0x00610D20`) runs a sequence of `TransitionEvent`s (`0x00610DEC`);
`choreo::Transition` (`0x005FE57C`) and `tStateTransition` (`0x005F8A6C`) are the animation/state
sides. [C40.5](05-transition-player.md).

## 40.6 Modding (✅ practical)

Fade timing/colour, disabling the box for instant swaps, or adding a custom transition are all
reachable by hooking `Fader`/`TransitionPlayer` (verified vtables) with DonutsSDK + VanHooks.
[C40.6](06-modding.md).

---

## What this chapter established

- The enter/exit-interior "black box" is a **`Fader`** driven by a verified **START/END event
  protocol** that synchronizes it with the interior swap (C41).
- The full-screen effect set — letterbox, iris wipe, intro transition — are distinct confirmed
  GUI screens.
- A `GuiSFX::*` chainable sequencer and a `TransitionPlayer` orchestrate all of it.

**Cross-references:** C41 (Interiors — what the box is hiding), C30 (GameFlow — contexts &
loading), C21 (Scrooby UI — the screens), C33 (Rendering — the fade quad), C17/C34
(choreo/animation transitions), C28.5/C28.7 (hooking + the vtables).
