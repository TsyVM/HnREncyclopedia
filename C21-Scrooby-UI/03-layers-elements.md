# C21.3 — Layers & Drawing Elements

**What it is.** The second half of a page: the `<Layers>` that stack its content, and the **drawing
elements** — sprites, text, groups, polygons, embedded 3-D — that are the actual UI. This is where a page
becomes a picture.

**How it works (✅ verified).** A page's content is one or more layers, each a tree of drawing elements.
From `HudMap.pag`:

```xml
<Layers>
  <Layer Name="HudMap" Visible="true" Editable="true" Alpha="255">
    <DrawingElements>
      <Group Name="Map0" Alpha="255">
        <DrawingElements>
          <Pure3dObject Name="Map0">
            <Position x="465" y="45"/>
            <Dimension width="120" height="120"/>
            <Justification vertical="centre" horizontal="centre"/>
            <Colour red="255" green="255" blue="255" alpha="255"/>
            <Translucency value="normal"/>
            <Rotation value="0.000000"/>
            <Pure3dFile name="dummy"/>
          </Pure3dObject>
          <Sprite Name="MapGlass0"> … </Sprite>
```

Every element shares the same property vocabulary: **`Position`** (x,y in 640×480 space), **`Dimension`**
(w,h), **`Justification`** (centre/left/top…), **`Colour`** (RGBA), **`Translucency`** (blend mode), and
**`Rotation`**. The verified element types and their game-wide counts:

| Element | Count | What it draws |
|---|--:|---|
| `Sprite` | 436 | a 2-D image (a named `<Image>`, C21.2) |
| `Text` | 274 | a styled, localized text run (C22) |
| `Group` | 252 | a container — a transform applied to its children |
| `Polygon` | 64 | a filled/outlined shape |
| `Pure3dObject` | 32 | an embedded 3-D object (a named `<Pure3dFile>`, C7) — e.g. the rotating map |

**Why layers and groups.** **Layers** give back-to-front ordering — the map background sprite is a lower
layer than the map icons on top of it — the 2-D equivalent of the scene graph's sort order (C10.5).
**Groups** give shared transforms — move a `Group` and all its children move together, and a group's `Alpha`
fades its whole subtree — exactly like a scene-graph branch (C10.2). So a page is a small 2-D scene graph:
layers order it, groups nest it, elements are its leaves. This is why the runtime classes (`Scrooby::Layer`,
`Scrooby::Group`, C21.4) mirror the XML tags one-to-one.

**The `Pure3dObject` element — 2-D UI meets 3-D.** The 32 `Pure3dObject`s are where a page embeds *actual
3-D* into the flat UI: the HUD minimap is a rotating 3-D model (C29) drawn inside a 120×120 UI box, the car
gallery spins a 3-D car. The element gives position/size/rotation in UI space and references a
`<Pure3dFile>` (C21.2) for the 3-D content, which the engine renders into that box. This is how Scrooby
composites 3-D previews into a 2-D menu.

**What happens if you bend it.**

- *Put elements in the wrong layer order* — foreground draws behind background. Order layers back-to-front.
- *Position outside 640×480* — the element draws off-screen. Keep coordinates in the authored resolution
  (C21.1).
- *Reference a `Pure3dFile`/`Image` name not in `<Resources>`* — nothing draws (C21.2). Declare it first.
