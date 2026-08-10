# C21.1 — Project → Screen → Page

**What it is.** The three-level hierarchy that organises the entire UI: a **Project** is the whole front-end,
a **Screen** is one full-screen view, and a **Page** is a reusable piece of content. All three are XML.

**How it works (✅ verified).** From `scrooby2/backend.prj`:

```xml
<?xml version='1.0'?>
<Project>
  <Version value="0"/>
  <Resolution width="640" height="480"/>
  <Platform value="PC"/>
  <ScreenPath value="screens\"/>
  <PagePath value="pages\"/>
  <ResourcePath value="resource\"/>
  <Screens>
    <Screen file="Blank.scr"/>
    <Screen file="Loading.scr"/>
    <Screen file="LoadingFE.scr"/>
    <Screen file="Demo.scr"/>
  </Screens>
</Project>
```

A **`.prj`** declares the UI's fixed resolution (640×480, the era's SD standard, C20.2), its target platform
(`PC`), the folders where screens/pages/resources live, and the list of screens. A **`.scr`** (e.g.
`Blank.scr`) is minimal — `<Screen><Pages>…</Pages></Screen>` — it composes pages into a full view. A
**`.pag`** is the content (C21.2–C21.3). So the hierarchy is: the project owns screens, a screen shows pages,
a page draws elements.

**Two projects: `scrooby` and `scrooby2`.** The game ships two Scrooby trees. `scrooby` is the older
version; `scrooby2` is the newer one used for the shipped UI (its `backend.prj`/`frontend.prj` drive the
back-end and front-end). This is a live-migration fingerprint — the UI was upgraded from Scrooby 1 to
Scrooby 2 during development, and both trees remain. When editing, work in `scrooby2` (the active one) unless
you've confirmed a screen loads from `scrooby`.

**Why a project/screen/page split.** It's the standard document-model separation applied to UI:

- **Project** = global settings + the catalogue of screens (like a book's front matter + table of contents).
- **Screen** = one view the player sees at a time (a menu, the loading screen).
- **Page** = a reusable content block that can appear on multiple screens (the HUD map page, a button strip).

Splitting screens from pages means a page (the map, say) can be reused across several screens without
duplication, and the platform/resolution live once in the project. It also makes the UI *data* — the whole
front-end is a folder of XML the engine loads, not compiled code, which is why UI modding is so accessible
(C21.6).

**Reading the UI's structure.** To map the game's whole front-end, start at the `.prj`, follow its `<Screen>`
list to the `.scr` files, and follow their pages to the `.pag` files. The result is the complete screen graph
— every view and what it contains — recoverable by reading XML, no game required.

**What happens if you bend it.**

- *Add a page/screen but not reference it* — an unreferenced `.pag`/`.scr` is never shown. List it in its
  parent (screen's `<Pages>` or project's `<Screens>`).
- *Change the project resolution* — every page is authored for 640×480; changing it without re-laying-out
  pages misaligns everything. Keep the authored resolution.
- *Edit the wrong Scrooby tree* — changes in `scrooby` won't show if the game loads `scrooby2`. Confirm which
  tree is active.
