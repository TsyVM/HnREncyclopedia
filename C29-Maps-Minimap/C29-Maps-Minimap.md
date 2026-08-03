# Chapter 29 — Maps & the HUD Minimap

> **Goal of this chapter:** decode the map system — the 3-D HUD minimap, the per-level map models, the icon
> set, and the full-screen map — and understand how the game shows you where you are and where to go.

The map is how a player navigates Springfield, and it's a neat synthesis of everything the book has covered:
a **3-D model** (C7) rendered inside a **Scrooby UI box** (C21) with **2-D icon sprites** composited on top,
one map per streaming level (C12). This chapter reads it from the retail data — the `HudMap.pag` page, the
seven `l{N}hudmap.p3d` models, and the icon PNGs.

**Key finding (✅ verified):** the HUD minimap is a **3-D Pure3D model per level** (`l1hudmap.p3d` …
`l7hudmap.p3d`) drawn in a `Pure3dObject` element (C21.3) inside `HudMap.pag`, overlaid with a "glass"
sprite and a pool of **icon sprites** (12 icon types: user, mission, aicar, collect, phone, checker, bonus,
camicon, blueflag, harascar, dice, dollar).

---

## Deep-dive pages

- [C29.1 — The HUD Minimap Page](01-hud-map-page.md): `HudMap.pag` — the 3-D map, glass, and icon pool.
- [C29.2 — The Per-Level Map Models](02-map-models.md): `l{N}hudmap.p3d`, one 3-D map per level.
- [C29.3 — The Map Icons](03-map-icons.md): the 12-icon vocabulary and what each means.
- [C29.4 — The Full-Screen Map](04-full-screen-map.md): `ViewMap` and the pause map.
- [C29.5 — Maps at Runtime](05-maps-runtime.md): world→map projection and the HUD classes.

---

## 29.1 The HUD minimap page (✅ verified)

`art/frontend/scrooby2/pages/HudMap.pag` is the minimap — a Scrooby page (C21) that composites three things:

```xml
<Pure3dObject Name="Map0">          <!-- the rotating 3-D map model (C29.2) -->
  <Position x="465" y="45"/> <Dimension width="120" height="120"/>
  <Pure3dFile name="dummy"/>         <!-- the l{N}hudmap.p3d is swapped in per level -->
</Pure3dObject>
<Sprite Name="MapGlass0"/>          <!-- the glass/frame overlay -->
<Sprite Name="IconPhone0_0"/> … IconPhone0_7   <!-- a POOL of icon sprites (C29.3) -->
```

So the minimap sits at (465,45) in a 120×120 box (top-right of the 640×480 screen), shows a 3-D map, and
draws icon sprites on top. The `dummy` Pure3D file is a stub swapped for the level's real map at load.
[C29.1](01-hud-map-page.md).

## 29.2 The per-level map models (✅ verified)

Each level has its own 3-D map: `l1hudmap.p3d` … `l7hudmap.p3d` (seven, one per story level, C12.1). Verified
`l1hudmap.p3d` is a normal Pure3D model — meshes (`0x00011003`/`4`/`5` shader params, C6), textures
(`0x00019000`, C5), and **`0x00007031`/`0x00007032`** frame/locator chunks (the anchor points icons attach
to). The map is a *3-D* model, not a flat image, which is why the minimap can rotate with the player.
[C29.2](02-map-models.md).

## 29.3 The map icons (✅ verified)

The icon set (`images\hud\mapicons\*.png`) is 12 sprites, each a gameplay marker:

| Icon | Marks | Icon | Marks |
|---|---|---|---|
| `user` | the player | `checker` | a race checkpoint |
| `mission` | a mission | `bonus` | a bonus mission |
| `phone` | a mission phone (start) | `camicon` | a camera/view point |
| `aicar` | a target/AI car | `blueflag` | a race flag |
| `collect` | a collectible | `harascar` | a harassing car (wasp) |
| `dice` | gambling | `dollar` | a purchase (shop) |

Icons are drawn as a **pool** (`IconPhone0_0`…`_7`) — a fixed set reused for whatever's currently on the map
(C29.3). [C29.3](03-map-icons.md).

## 29.4 The full-screen map (✅ verified)

`ViewMap.pag` / `ViewMap.scr` is the **pause map** — the full-screen view of the level, opened from the pause
menu. It shows the same per-level map model larger, with icons and teleport destinations (C12.4).
[C29.4](04-full-screen-map.md).

## 29.5 Maps at runtime (✅ verified)

Each frame the map system projects world positions (C12) onto map space — placing the `user` icon at the
player's location, `mission`/`phone` icons at their world spots — and rotates the 3-D map. The runtime is the
GUI/HUD class set (`Hud*`, `CGui*`, C21/C23; names ✅, offsets ⏳). [C29.5](05-maps-runtime.md).

---

## Key takeaways

- The HUD minimap is a **3-D Pure3D model per level** (`l{N}hudmap.p3d`, seven) drawn in a Scrooby
  `Pure3dObject` box (C21.3) with a glass overlay and a **pool of icon sprites**.
- The map is *3-D*, not a flat image — it rotates with the player; icons attach at frame/locator anchors
  (`0x00007031`/`32`).
- The **12-icon vocabulary** (user, mission, phone, aicar, collect, checker, bonus, camicon, blueflag,
  harascar, dice, dollar) marks every gameplay point of interest.
- The full-screen `ViewMap` is the pause map; runtime projects world→map each frame via the HUD classes.
- Maps synthesise the whole book: 3-D models (C7) + UI (C21) + world coords (C12) + gameplay (C16).

**Next:** [Chapter 28 — The Modding Toolchain](../C28-Modding-Toolchain/C28-Modding-Toolchain.md).
