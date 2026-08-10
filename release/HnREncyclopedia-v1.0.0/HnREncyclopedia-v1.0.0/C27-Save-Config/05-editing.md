# C27.5 — Editing Config & Saves

**What it is.** The practical guidance for changing the two persistence files — the safe, easy config
(`simpsons.ini`) and the riskier binary save (`Save1`). This closes the chapter with what you can edit and
what to watch for.

**Editing `simpsons.ini` (safe).** The config is plain text (C27.4), so editing is low-risk and needs only a
text editor:

- **Resolution / display** — set `resolution=` and `display=` in `#System` to a mode the menus don't offer
  (a widescreen or higher resolution). If the game can't create the device, it falls back — so a bad value
  is recoverable.
- **Volumes** — tune the five `#Sound` channels (C27.4) independently: lower `music`, raise `dialogue`, etc.
  Values are 0.0–1.0.
- **Controls** — adjust `mousesensitivityx/y`, `wheelsensitivityx/y`, toggle `mouselook`, `invertmousex/y`,
  `useforcefeedback`, `disabletutorials`. Rebind inputs via the `buttonmap` lines (or, more safely, through
  the in-game menu, which rewrites them).

Because it's text and the game rewrites it, a mistake is easily fixed (edit again, or delete the file to
regenerate defaults). This is the safest file in the game to edit.

**Editing the save `Save1` (careful).** The save is binary (C27.1) and may be integrity-checked, so editing
it is riskier:

- **What's readable** — the record structure is ✅ verified: the player name (@17), the mission-completion
  array (32-byte stride, C27.2), and the reward/car array (24-byte stride, `famil_v`/`n/a`). You can *read* a
  player's progress reliably.
- **What's risky** — the numeric fields (coins, story progress) are 🟡: you'd need to *save-diff* (C4.3) to
  pin a specific field before editing it. And the leading bytes may be a **checksum** (C27.1) — if so,
  editing the save body without recomputing it makes the game **reject the save as corrupt**.
- **The safe way** — if you must edit a save, first identify the checksum (change one in-game value, re-save,
  and see which header bytes change alongside the body), then recompute it after your edit. Better still,
  achieve the change *in-game* (earn the reward) so the game writes a valid, checksummed save for you.

**Why the difference.** The config is *designed* to be edited (by the game and the player), so it's text and
forgiving. The save is *designed* to be written and read by the game only, on a memory card, fast and
tamper-resistant — so it's binary, fixed-layout, and possibly checksummed (C27.3). The formats reflect their
audiences: config for humans, save for the machine. Respecting that — freely editing config, cautiously
editing saves — is the rule.

**The modding perspective.** For most purposes, you don't edit the save at all — you edit the *content* it
records (add a car via `BindReward`, C16.6; retune the economy) and let the game write the save normally.
Save editing is a last resort for forcing a specific state (unlock everything, set coins). The config, by
contrast, is a routine edit — the first thing many players change (resolution, controls). Know which is
which: config is a tool, save-editing is a scalpel.

**What happens if you bend it.**

- *Edit the save body past a checksum* — rejected as corrupt (C27.1). Recompute the checksum or change it
  in-game.
- *Trust an unverified save offset* — the numeric fields are 🟡; save-diff to confirm (C4.3).
- *Fear editing the config* — don't; it's text and regenerates. It's the safe file.

**Next:** [Chapter 28 — The Modding Toolchain](../C28-Modding-Toolchain/C28-Modding-Toolchain.md).
