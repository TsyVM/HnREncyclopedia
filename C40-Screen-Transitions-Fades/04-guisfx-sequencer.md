# C40.4 — The `GuiSFX` Sequencer

> `GuiSFX::*` is a family of ~25 confirmed **chainable scripted effects** — the vocabulary the
> front-end and transitions are built from. Think of it as a tiny effect timeline.

## The primitives (✅ verified classes)
| Effect | Does |
|---|---|
| `GuiSFX::Show` / `Hide` | reveal / conceal a UI element |
| `GuiSFX::GotoScreen` | switch to another screen |
| `GuiSFX::Transition` | run a transition |
| `GuiSFX::IrisWipeOpen` | open the iris wipe (C40.3) |
| `GuiSFX::ColorChange` | tween a colour |
| `GuiSFX::PulseScale` | pulse an element's scale |
| `GuiSFX::Translator` / `UnderdampedTranslator` | move an element (linear / eased) |
| `GuiSFX::Pause` / `PauseInFrames` | wait (seconds / frames) |
| `GuiSFX::SendEvent` / `RecieveEvent` | fire / await an event |
| `GuiSFX::SwitchContext` / `InputStateChange` | change GameFlow context / input mode |
| `GuiSFX::ResumeGame` / `RestartCurrentMission` / `AbortCurrentMission` | mission verbs |
| `GuiSFX::Chainable` / `Chainable1/3` / `Junction3` / `Dummy` | sequencing plumbing |

## How it works
Effects derive from a `Chainable` base, so each effect, when done, triggers the next — a linked
sequence. `Junction` nodes branch/merge; `Pause` inserts timing; `SendEvent`/`RecieveEvent`
synchronize with the game (e.g. wait for an iris-wipe CLOSED before proceeding). A screen's
scripted behaviour is essentially a graph of these.

## Why a mini-language
Menu and transition choreography (fade this, wait, switch screen, pulse the button, resume) is
data-shaped, not code-shaped. A chainable-effect graph lets designers author flow without new
C++ per screen — the same reasoning behind the Scrooby layout split (C21).

## What happens if you bend it
Assembling your own chain (via the confirmed classes) lets a mod script custom menu/transition
flow; hooking `Chainable::advance` lets you observe or reroute the sequence.

## Cross-references
C40.3 (iris wipe), C40.5 (the player that runs sequences), C21 (Scrooby), C38 (menus), C30 (contexts).
