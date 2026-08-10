# C38.6 — Pitfalls & Discipline

> Adding a menu means living inside the engine's own UI objects. These are the traps that break menu mods, and
> the discipline that keeps them stable.

## 1. Front-end and pause are separate (✅ verified)

The title-screen Options and the pause Options are **different screen instances under different managers**
(`CGuiManagerFrontEnd` vs `CGuiManagerInGame`, C38.1; the mirrored screens, C37.5). A hook on
`CGuiScreenPauseOptions` does **not** touch `CGuiScreenOptions`. If you want your entry in both places, install
both sets of hooks. Test in both — it's the most common "it's missing on the title screen" bug.

## 2. Ownership & lifetime

Screens and items are **engine-owned**. Menus are built and torn down as the player navigates (C38.2), so:

- Don't cache a screen or item pointer across a screen pop — it may be freed. Re-fetch on each build.
- If you allocate an item/screen, be clear about who frees it. Repurposing a stock screen (Approach A, C38.4)
  sidesteps most lifetime questions.
- Rebuild your injected item every time the host screen builds — the stock build recreates its list, so a
  one-time append disappears on the second visit. Hook the build method, don't append once.

## 3. Recover addresses per build (✅ discipline)

Vtable addresses (`0x0060E28C` etc.) and **slot indices** are specific to retail `Simpsons.exe`
(MD5 `b3a47b881eec97745424b1e2c86cdcaf`). On any other build they differ. Recover them with SAHRDiag/DonutsSDK
(C28.7) at load time and fail gracefully if a class isn't found — never hard-code and hope (C28.6).

## 4. Reversibility

Every hook is a non-destructive vtable swap (C28.5). On unload, `remove` them so the menu returns to stock. A
mod that can't cleanly uninstall is a mod that corrupts the UI on reload.

## 5. Input focus & re-entrancy

Only the top screen has focus (C38.2). When you push your screen, the host stops receiving input — don't keep
driving the host from your screen. Return "handled" from your input detour when you consume an event, so it
doesn't also trigger the stock handler.

## 6. Layout realities (Scrooby)

If you repurpose a stock screen (Approach A), you inherit its layout — your labels must fit its text anchors
(C21). If you author a new `FeScreen` (Approach B), it must be present in the front-end project the game loads.
Overlong labels clip; localized strings (C22) change width per language — test with the languages you support.

## 7. Scope

Menu mods are for single-player, offline play on a copy you own (C28.6). Adding menus that alter save state or
progression should follow the same read-first, back-up-first care as any save edit (C27.5).

## The short checklist

- [ ] Hook the **build** method (re-append every build), not a one-time insert.
- [ ] Hook **input**, return handled for your item.
- [ ] Install on **both** front-end and pause screens if you want it in both.
- [ ] Recover vtables **and slots** at load via SAHRDiag; fail gracefully.
- [ ] **Remove** all hooks on unload.
- [ ] Persist options to your **own** config, not the game's.

## Cross-references

- **C37.5** — the mirrored front-end/pause screens.
- **C28.6 / C28.7** — verification ethics and recovering addresses.
- **C38.2 / C38.4** — lifecycle and screen-ownership details.
