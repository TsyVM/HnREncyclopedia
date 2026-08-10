# C21.2 — Page Resources

**What it is.** The first half of a page: the `<Resources>` block that declares everything the page draws
*with* — its images, embedded 3-D objects, localized text, and fonts — each given a name the drawing
elements (C21.3) reference.

**How it works (✅ verified).** From `HudMap.pag`:

```xml
<Resources>
  <Images>
    <Image name="mapbgd" data="images\hud\mapbgd.png"/>
    <Image name="mission" data="images\hud\mapicons\mission.png"/> …
  </Images>
  <MovieClips></MovieClips>
  <Pure3dFiles>
    <Pure3dFile name="dummy" data="pure3d\_stubs\dummy.p3d"
                Pure3dInventoryName="dummy" Pure3dCameraName="" Pure3dAnimationName=""/>
  </Pure3dFiles>
  <TextBibles><TextBible name="srr2" data="txtbible\srr2.p3d" inventoryName="srr2"/></TextBibles>
  <TextStyles><TextStyle name="font1_14" data="fonts\font1_14.p3d" inventoryName="Tt2001m__14"/></TextStyles>
</Resources>
```

Five resource types, each a **name → asset** binding:

- **`Images`** — PNG files (C5). `mapbgd` → `images\hud\mapbgd.png`. A `Sprite` element (C21.3) then draws
  "mapbgd" by name.
- **`Pure3dFiles`** — embedded Pure3D objects (C7), with an inventory/camera/animation name. This is how the
  HUD map shows a *rotating 3-D* minimap — a `Pure3dObject` element draws it.
- **`TextBibles`** — localized string tables, stored as `.p3d` (`txtbible\srr2.p3d`) — the source of
  translatable text (C22).
- **`TextStyles`** — fonts, stored as `.p3d` (`fonts\font1_14.p3d`) — the glyph atlas and metrics (C22). The
  `inventoryName` (`Tt2001m__14`) is the font's internal name.
- **`MovieClips`** — animated UI clips (often empty).

**Why declare resources up front.** Separating *what's available* (resources) from *what's drawn* (elements,
C21.3) is the standard resource/instance split (seen also in the scene graph, C10.4, and shaders→textures,
C5.6). It lets one image be drawn by many sprites, lets the loader preload a page's assets before laying it
out, and lets an element reference an asset by a short name rather than a full path. Change the PNG behind
`mapbgd` and every sprite using it updates; the elements don't need editing.

**The name-binding pattern.** Every resource has a `name` used *within the page* and a `data` path to the
*actual file*. Elements reference the `name`; the loader resolves `data` through the VFS (C3.6). So a page is
self-contained: its resource block is its private namespace, and its elements draw from it. This is why you
can read a page in isolation — its resources tell you exactly what art, text, and fonts it needs.

**What happens if you bend it.**

- *Reference an element to a resource name that isn't declared* — nothing draws. Declare the resource first.
- *Point a resource `data` at a missing file* — the page loads with a hole. Ensure the PNG/P3D exists
  (C3.6).
- *Rename a resource without updating its elements* — the elements' references break. Keep names in sync
  within the page.
