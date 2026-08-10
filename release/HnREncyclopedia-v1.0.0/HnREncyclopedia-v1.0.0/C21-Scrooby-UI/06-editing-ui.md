# C21.6 — Editing the UI

**What it is.** How to actually change the game's UI — which, because Scrooby pages are XML (C21.1), is the
most approachable modding in the whole game: edit text, save, done. This page is the practical payoff of the
chapter.

**How it works.** UI edits fall into three tiers, easiest first:

1. **Reposition / recolour / restyle (edit XML attributes).** Move an element's `<Position>`, change its
   `<Colour>` or `<Dimension>`, flip `<Justification>`, adjust `<Rotation>` or `<Translucency>` (C21.3). No
   asset changes, no size tree — just edit the `.pag` text and save. Nudging the HUD, recolouring a menu,
   resizing the map: all one-line XML edits.
2. **Swap an image (edit a resource).** Change an `<Image>`'s `data` path to a new PNG, or overwrite the PNG
   it points at (C5, C21.2). Every `Sprite` using that image updates. Reskinning the UI is swapping PNGs.
3. **Add or remove elements (edit structure).** Add a `<Sprite>`/`<Text>`/`<Group>` to a `<Layer>`,
   declaring any new resource in `<Resources>` first (C21.2). Adding a HUD element or a menu button is adding
   an element and (if needed) its behaviour in the `CGuiScreen` (C21.5).

Because it's XML, tiers 1–2 need only a text editor and (for images) an image editor — no repacking, no
size-tree fix-ups (contrast the binary formats, C1.5). This is why community UI mods for SHAR are common: the
barrier is reading XML, not reverse-engineering a binary.

**What you can't do in XML alone.** The page is *appearance*; behaviour lives in the `CGuiScreen` class
(C21.5), which is compiled code. You can move the "Load Game" button (XML) but not change *what it loads*
without touching the screen logic (⏳ — code, needs the runtime). So UI modding splits cleanly: layout and
art are open (XML/PNG); logic is closed (compiled `CGui` classes). Most UI mods live entirely in the open
half.

**The safe workflow.** Edit a copy, load the game, check the screen. Because pages are validated as XML,
malformed XML simply fails to load that page (a blank or missing screen) rather than corrupting the game —
a forgiving failure mode. Keep the 640×480 coordinate space (C21.1), keep resource names in sync with their
elements (C21.2), and edit the active Scrooby tree (`scrooby2`, C21.1).

**Why the UI is the modder's entry point.** Of all the formats in this book, Scrooby XML is the one you can
edit with the least tooling and the least risk. It's where a new modder starts — move a HUD element, recolour
a menu — before graduating to textures (C5), handling (C15), missions (C16), and eventually the binary
formats. The XML UI is the shallow end of the modding pool, and this chapter is the map of it.

**What happens if you bend it.**

- *Write malformed XML* — the page fails to load (blank screen). Validate the XML; the failure is safe but
  visible.
- *Move an element off the 640×480 canvas* — it draws off-screen. Stay in the authored resolution.
- *Add an element referencing an undeclared resource* — nothing draws. Declare resources first (C21.2).

**Next:** [Chapter 22 — Fonts, Glyphs & Localization](../C22-Fonts-Localization/C22-Fonts-Localization.md).
