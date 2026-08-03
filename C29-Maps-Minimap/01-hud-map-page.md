# C29.1 — The HUD Minimap Page

**What it is.** The Scrooby page that *is* the minimap — `HudMap.pag`. It composites a 3-D map model, a glass
overlay, and a pool of icon sprites into the small map in the corner of the screen. It's a textbook example
of a Scrooby page (C21) doing real work.

**How it works (✅ verified).** `art/frontend/scrooby2/pages/HudMap.pag` declares its resources (the 12 icon
PNGs, a Pure3D stub) and lays out three kinds of element (C21.3):

```xml
<Group Name="Map0">
  <Pure3dObject Name="Map0">                 <!-- the 3-D map (C29.2) -->
    <Position x="465" y="45"/>
    <Dimension width="120" height="120"/>
    <Justification vertical="centre" horizontal="centre"/>
    <Rotation value="0.000000"/>
    <Pure3dFile name="dummy"/>               <!-- swapped for l{N}hudmap.p3d per level -->
  </Pure3dObject>
  <Group Name="MapGlass0"><Sprite Name="MapGlass0"/></Group>   <!-- glass/frame overlay -->
  <Sprite Name="IconPhone0_0"/> … <Sprite Name="IconPhone0_7"/> <!-- icon pool (C29.3) -->
</Group>
```

The map lives at **(465, 45)** in a **120×120** box — the top-right corner of the 640×480 screen (C21.1). It
draws in three layers: the **3-D map model** at the bottom, a **glass** sprite over it (the frame/reflection
that makes it look like a device), and **icon sprites** on top marking points of interest. The `Rotation`
property is animated at runtime so the map turns as the player turns.

**The `dummy` stub.** The `<Pure3dFile name="dummy" data="…\_stubs\dummy.p3d"/>` is a placeholder: the page
is authored with a stub map, and the *real* per-level map (`l{N}hudmap.p3d`, C29.2) is swapped in when a level
loads. This is why the page is level-agnostic — one `HudMap.pag` serves all seven levels, and the streaming
system (C12.3) supplies the current level's map model into the `Pure3dObject` slot. Author once, fill per
level — the same resource-indirection pattern as everywhere else (C21.2).

**Why 3-D in a 2-D HUD.** A flat map image can't rotate convincingly or show elevation; a 3-D model can tilt,
turn, and convey the world's shape. Rendering it inside a Scrooby `Pure3dObject` box (C21.3) lets the minimap
be genuinely 3-D while still being a UI element positioned and framed like any sprite. This is the single
most sophisticated use of the `Pure3dObject` element (32 of them exist, C21.3) — the minimap and the car
gallery are why that element exists.

**The icon pool.** The eight `IconPhone0_0…_7` sprites are a **pool** — a fixed set of icon slots reused for
whatever needs marking right now (C29.3). Rather than create/destroy icon sprites as things appear, the page
pre-declares a pool and the runtime assigns each active point of interest to a free slot, setting its image
and position. This is the standard UI object-pooling pattern — allocate once, reuse — which keeps the HUD
cheap.

**What happens if you bend it.**

- *Move the `Pure3dObject` box off-screen* — the map vanishes. Keep it in the 640×480 canvas (C21.1).
- *Remove the glass sprite* — the map loses its framing but still works; it's cosmetic. The 3-D model and
  icons are the function.
- *Assume the map is a fixed image* — it's a 3-D model swapped per level (C29.2). Edit the model, not a PNG,
  to change the map itself.
