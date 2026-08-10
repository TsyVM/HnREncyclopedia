# Chapter 21 — Scrooby UI

> **Goal of this chapter:** decode the front-end and HUD system — the Scrooby XML page format, its
> project/screen/page hierarchy, its drawing elements — and the `CGui`/`Fe` runtime that renders it. After
> this chapter you can read and edit any menu, HUD, or screen in the game.

Every menu, the HUD, the map, the mission-select screen — all of it is **Scrooby**, Radical's UI system. And
Scrooby is unusually approachable: its pages are **XML**. This chapter reads that XML directly from the
retail data (119 pages, all `<?xml>`) and maps it to the 74-class `CGui*`/`Scrooby::`/`Fe*` runtime.

**Key finding (✅ verified):** Scrooby is a **retained-mode, layered 2-D compositor authored in XML**. A
**Project** (`.prj`) lists **Screens** (`.scr`), which hold **Pages** (`.pag`); a page declares **resources**
(images, Pure3D files, text bibles, fonts) and **layers** of **drawing elements** — verified across all
pages: **436 Sprites, 274 Text, 252 Groups, 64 Polygons, 32 Pure3D objects**. The runtime `Scrooby::Page` /
`Layer` / `Group` classes mirror the XML one-to-one.

---

## Deep-dive pages

- [C21.1 — Project → Screen → Page](01-project-screen-page.md): the `.prj`/`.scr`/`.pag` hierarchy.
- [C21.2 — Page Resources](02-page-resources.md): images, Pure3D files, text bibles, text styles.
- [C21.3 — Layers & Drawing Elements](03-layers-elements.md): Sprite, Text, Group, Polygon, Pure3dObject.
- [C21.4 — The Scrooby & `Fe` Runtime](04-scrooby-runtime.md): `Scrooby::Page`/`Layer`, the `Fe*` render layer.
- [C21.5 — `CGui` Managers & Screens](05-cgui-managers.md): the 7 managers and 60 screens.
- [C21.6 — Editing the UI](06-editing-ui.md): modding the XML safely.

---

## 21.1 Project → Screen → Page (✅ verified)

Scrooby has a three-level hierarchy, all XML. Verified from `scrooby2/backend.prj`:

```xml
<Project>
  <Resolution width="640" height="480"/>  <Platform value="PC"/>
  <ScreenPath value="screens\"/> <PagePath value="pages\"/> <ResourcePath value="resource\"/>
  <Screens>
    <Screen file="Blank.scr"/> <Screen file="Loading.scr"/> …
  </Screens>
</Project>
```

A **`.prj`** is the whole UI project (resolution, platform, paths, screen list); a **`.scr`** is a screen
holding pages; a **`.pag`** is a page — the actual content. The game has two projects: `scrooby` (v1) and
`scrooby2` (v2). [C21.1](01-project-screen-page.md).

## 21.2 Page resources (✅ verified)

A page first declares what it draws *with*. Verified from `HudMap.pag`:

```xml
<Resources>
  <Images><Image name="mapbgd" data="images\hud\mapbgd.png"/> …</Images>
  <Pure3dFiles><Pure3dFile name="dummy" data="pure3d\_stubs\dummy.p3d" …/></Pure3dFiles>
  <TextBibles><TextBible name="srr2" data="txtbible\srr2.p3d"/></TextBibles>
  <TextStyles><TextStyle name="font1_14" data="fonts\font1_14.p3d"/></TextStyles>
</Resources>
```

Images are PNGs (C5), Pure3D files embed 3-D objects (C7), **TextBibles** are localized strings (C22), and
**TextStyles** are fonts (C22). [C21.2](02-page-resources.md).

## 21.3 Layers & drawing elements (✅ verified)

The content is layers of drawing elements. Verified element census across all pages:

| Element | Count | Is |
|---|--:|---|
| `Sprite` | 436 | a 2-D image (an `<Image>`) |
| `Text` | 274 | a text run (styled, localized) |
| `Group` | 252 | a container of elements (with its own transform) |
| `Polygon` | 64 | a filled shape |
| `Pure3dObject` | 32 | an embedded 3-D object (C7) — e.g. the rotating map |

Each element has `<Position>`, `<Dimension>`, `<Justification>`, `<Colour>`, `<Translucency>`, `<Rotation>`.
[C21.3](03-layers-elements.md).

## 21.4 The Scrooby & `Fe` runtime (✅ verified)

The XML is loaded into a runtime that mirrors it: `Scrooby::Page`, `Scrooby::Layer`, `Scrooby::Group`,
`Scrooby::BoundedDrawable` (11 classes), rendered through the **`Fe`** (Front-End) entity layer —
`FeDrawable`, `FeText`, `FeGroup`, `FeEntity` (32 classes). The `Scrooby::FeProjectChunkHandler` loads a
project. [C21.4](04-scrooby-runtime.md).

## 21.5 `CGui` managers & screens (✅ verified)

Above Scrooby sits the game's UI logic: **7 `CGuiManager`s**, one per context — `CGuiManagerFrontEnd`,
`CGuiManagerInGame`, `CGuiManagerBackEnd`, `CGuiManagerBootUp`, `CGuiManagerLanguage`,
`CGuiManagerMiniGame` — and **60 `CGuiScreen`** subclasses (mission select, pause, gallery, load…). These
drive *which* Scrooby screen is shown and handle its logic. [C21.5](05-cgui-managers.md).

## 21.6 Editing the UI (✅ verified path)

Because pages are XML, editing the UI is editing text: move an element's `<Position>`, change a `<Colour>`,
swap an `<Image>`'s PNG, add a `Sprite`. [C21.6](06-editing-ui.md).

---

## Key takeaways

- Scrooby is a **retained-mode 2-D UI in XML**: **Project (`.prj`) → Screen (`.scr`) → Page (`.pag`)**.
- A page declares **resources** (images, Pure3D files, TextBibles, fonts) then **layers** of **drawing
  elements** — verified: 436 Sprites, 274 Text, 252 Groups, 64 Polygons, 32 Pure3D objects.
- Elements carry position, dimension, justification, colour, translucency, rotation.
- The runtime mirrors the XML: `Scrooby::Page`/`Layer`/`Group` (11), the `Fe*` render layer (32), driven by
  **7 `CGuiManager`s** and **60 `CGuiScreen`s**.
- Editing the UI is editing XML — the most approachable format in the game.

**Next:** [Chapter 22 — Fonts, Glyphs & Localization](../C22-Fonts-Localization/C22-Fonts-Localization.md).
