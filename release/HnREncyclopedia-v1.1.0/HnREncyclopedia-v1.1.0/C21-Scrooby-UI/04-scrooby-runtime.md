# C21.4 — The Scrooby & `Fe` Runtime

**What it is.** What the XML pages (C21.1–C21.3) become when loaded — the `Scrooby::` classes that mirror the
XML structure, and the `Fe` (Front-End) entity layer that actually renders it. This is the bridge from
authored XML to pixels.

**How it works (✅ verified).** From `shar_dumps.csv`, two families:

```
Scrooby:: (11)                    — mirrors the XML tags
  Scrooby::Page                   ↔ <Page>
  Scrooby::Layer                  ↔ <Layer>
  Scrooby::Group                  ↔ <Group>
  Scrooby::Drawable / BoundedDrawable / HasBoundingBox   ↔ drawing elements
  Scrooby::FeProjectChunkHandler  — loads a .prj/.scr/.pag project

Fe* (32)                          — the render/entity layer
  FeApp                           — the front-end application
  FeEntity → FeDrawable → FeBoundedDrawable   — renderable UI entities
  FeGroup, FeText, FeTextBible    — group, text, localized-text entities
```

The mapping is **one-to-one**: a `<Page>` loads into a `Scrooby::Page`, its `<Layer>`s into
`Scrooby::Layer`s, its `<Group>`s into `Scrooby::Group`s, its elements into `Scrooby::Drawable`s. This is why
reading the XML *is* reading the runtime — the tag names are the class names. The `Fe*` layer is the actual
rendering: a `Scrooby::Drawable` is realised as an `FeDrawable`, text as `FeText`, and so on. `FeApp` is the
front-end app that owns the whole thing.

**Why mirror the XML in classes.** A retained-mode UI keeps a live object tree that matches the authored
document, so it can re-layout, animate, and hit-test without re-parsing the XML each frame. Making each XML
tag a class (`Scrooby::Layer` for `<Layer>`) means loading a page is a direct deserialization — walk the
XML, construct the matching object — and the live tree is inspectable and manipulable (a menu can hide a
layer, fade a group, move an element) exactly as the XML describes. The `Fe` split (Scrooby structure vs. Fe
rendering) separates *what the UI is* from *how it's drawn*, the same structure/render split as the scene
graph and its DSG entities (C10.6).

**The loader.** `Scrooby::FeProjectChunkHandler` is the chunk handler (C23.4) that loads a Scrooby project.
Note it's a *chunk* handler — the XML pages, once processed, are carried in the Pure3D pipeline (the fonts and
text bibles are literally `.p3d` files, C21.2/C22), so Scrooby integrates with the same loader registry
(C1.8/C23.4) as everything else. The UI isn't a bolted-on system; it rides the engine's asset pipeline.

**The render path.** Each frame, `FeApp` walks the live `Scrooby::Page` tree, applies group transforms and
layer ordering (C21.3), and draws each `FeDrawable` — sprites as textured quads (from the `<Image>` PNGs,
C5), text through the font system (C22), `Pure3dObject`s by rendering their 3-D content into the UI box. It's
a 2-D compositor pass over the retained tree — the UI equivalent of the scene-graph render walk (C10.6).

**What happens if you bend it.**

- *Rely on a `Scrooby::`/`Fe` member offset* — the classes are ✅ (43 total), offsets ⏳. Diff (C4.3).
- *Expect the runtime to differ from the XML* — it mirrors it. If a page looks wrong, the XML is the source
  of truth; read it (C21.1–C21.3).
- *Bypass the Fe layer to draw UI directly* — you lose the retained tree's ordering and transforms. Author in
  Scrooby XML and let `FeApp` render it.
