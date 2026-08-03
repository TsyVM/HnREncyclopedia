# C27.3 — The Memory-Card System

**What it is.** The runtime that reads and writes the save (C27.1) — `MemoryCardManager` and the save/load UI.
Its name is a fossil of the game's console origins: on PS2/GameCube/Xbox, saves live on **memory cards**, and
the PC version keeps the same machinery (writing `Save1` to disk instead of a card).

**How it works (✅ verified).** The verified runtime classes:

```
MemoryCardManager (vtable 0x00607514)  — owns save/load, slot management, formatting
DriveOpenRequest / DriveFindFirstRequest / DriveFormatRequest / …  — the async drive/file requests
CGuiScreenMemoryCard / CGuiScreenMemCardCheck  — the memory-card UI (C21.5)
CGuiScreenLoadGame / CGuiScreenAutoLoad        — load-game screens (C21.5)
```

**`MemoryCardManager`** is the singleton that handles saving and loading: it enumerates save slots, reads and
writes the `Save1` career state (C27.1), and manages formatting/errors. The `Drive*Request` family (verified
in the RTTI) are the **asynchronous file/drive operations** it issues — open, find, format, read, write —
the same async, callback-based I/O as `LoadingManager` (C30.4). The UI is a set of Scrooby screens (C21.5):
`CGuiScreenMemoryCard` (manage saves), `CGuiScreenMemCardCheck` (verify a card is present/valid),
`CGuiScreenLoadGame`/`CGuiScreenAutoLoad` (load a save).

**Why "memory card" on PC.** SHAR was built for consoles first, where saves are memory-card files with slot
management, formatting, and "please insert a memory card" prompts. Rather than rewrite the save system for
PC, Radical kept `MemoryCardManager` and pointed it at the hard disk — so the PC version still *thinks* in
memory-card terms (slots, cards, the `MemCardCheck` screen) even though it writes a plain `Save1` file. This
is common in console-to-PC ports: the save abstraction (a "card" with "slots") survives, backed by files.
It's why the PC menus talk about memory cards and why the save is a single fixed-size file (C27.1) — the file
*is* the emulated card.

**Async save/load.** Like level loading (C30.4), save/load is **asynchronous** — `MemoryCardManager` issues
`Drive*Request`s and gets called back on completion, so the game stays responsive during a save (the "saving…"
indicator spins while the write happens in the background). This matters more on a slow memory card than a
hard disk, but the machinery is the same on PC. The auto-save (`CGuiScreenAutoLoad`) uses this to save
progress at checkpoints without interrupting play.

**The tie to the reward economy.** `MemoryCardManager` is what makes the reward economy (C16.6, C32) durable:
when you complete a mission and `RewardsManager` (C32.5) grants a car, `MemoryCardManager` writes it to the
save (C27.2) so it persists. On next launch, it reads the save back and the managers (`RewardsManager`,
`CoinManager`, the mission system) restore their state. The save system is the persistence layer under the
whole progression.

**What happens if you bend it.**

- *Rely on the `MemoryCardManager` singleton address or a member offset* — class/vtable ✅, offset/instance
  ⏳ (or now partially recovered, C23.1). Diff (C4.3).
- *Expect synchronous save/load* — it's async (`Drive*Request` callbacks). Don't block on it.
- *Assume PC saves differ structurally from console* — they share `MemoryCardManager` and the `Save1`
  layout (C27.1); the "card" is emulated by the file.
