# C40.3 — LetterBox & Iris Wipe

> Two more full-screen effects, each its own confirmed GUI screen: the cinematic **letterbox**
> bars and the circular **iris wipe**.

## LetterBox — `CGuiScreenLetterBox` (`0x0060EC24`)
Draws black bars top and bottom to force a 2.35:1-style cinematic frame. Used for scripted
moments and cutscenes (NIS, C17) where the game wants a filmic look. As a GUI screen it is
pushed/popped by the UI manager like any other (C38.2), on top of the world.

## Iris Wipe — `CGuiScreenIrisWipe` (`0x0060ED20`)
The classic cartoon circle that closes to a point (or opens from one) — very on-brand for a
Simpsons game. It emits its own events:
```
CGuiScreenIrisWipe => EVENT_GUI_IRIS_WIPE_CLOSED.
CGuiScreenIrisWipe => EVENT_GUI_IRIS_WIPE_OPEN.
```
and is triggered by the script command **`SetIrisWipe`**. `GuiSFX::IrisWipeOpen` (`0x0060D8D0`)
is the scripted-effect wrapper that opens it as part of a sequence (C40.4).

## How they compose
Both are screens the `GuiSFX` sequencer or a mission script can raise. The iris wipe's
CLOSED/OPEN events let a script wait for the wipe to finish before doing the hidden work — the
same START/END discipline as the interior fade (C40.2), just circular instead of a fade.

## What happens if you bend it
- Swap the iris texture/shape for a custom wipe.
- Use `SetIrisWipe` in your own mission script for a themed transition.
- Force letterbox on for a "cinematic mode" mod.

## Cross-references
C40.2 (event discipline), C40.4 (the sequencer), C17 (NIS/cutscenes), C21 (Scrooby screens).
