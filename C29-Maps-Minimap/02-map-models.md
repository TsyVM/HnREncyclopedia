# C29.2 — The Per-Level Map Models

**What it is.** The seven 3-D models that *are* the maps — `l1hudmap.p3d` through `l7hudmap.p3d`, one per
story level (C12.1). Each is a simplified 3-D representation of its level, drawn in the minimap box (C29.1)
and the full-screen map (C29.4).

**How it works (✅ verified).** Each `l{N}hudmap.p3d` is a normal Pure3D file (C1). Verified `l1hudmap.p3d`
(74 KB, 128 chunks) contains:

```
0x00019000/1/2 Texture/Image/ImageData  ×3   the map's textures (C5)
0x00011003/4/5 shader int/colour/float params  the map's materials (C6)
0x00007031 / 0x00007032  ×6 / ×9             frame/locator anchor chunks (🟡)
```

So a map model is: **meshes** (C7) shaped like the level's road layout, **textured** (C5) and **shaded**
(C6) to be readable at a glance, plus **`0x00007031`/`0x00007032`** frame/locator chunks — the named anchor
points icons and labels attach to. It's a purpose-built, simplified model — not the full level geometry
(C12), but a clean map version of it, small enough (74 KB) to keep resident while its level is active.

**Why a separate map model.** The playable level (C12) is millions of chunks of detailed geometry — far too
much and too busy to show as a map. A dedicated map model is *authored for legibility*: simplified roads,
clear landmarks, flat readable colours, at a scale that fits the 120×120 minimap box. Making it a separate
`.p3d` per level means the map can be designed as a map (clarity first) rather than derived from the world
(detail first), and it's cheap to load and rotate. This is the same "authored representation, not derived"
choice as the road *graph* being separate from the road *mesh* (C13.2) — the map you see and the world you
drive are different data tuned for different jobs.

**The anchor chunks.** The `0x00007031`/`0x00007032` chunks (frame/locator family, C8.5) are the map's
**registration points** — named positions on the map that correspond to world locations, so the runtime knows
where to place icons (C29.3) and where the player marker goes. When the map projects the player's world
position (C29.5), these anchors calibrate the world→map transform: a known world point maps to a known map
point, and everything else follows. This is why the map model carries locators, not just geometry — they're
the map's coordinate reference.

**One per level, streamed.** The seven maps mirror the seven levels (C12.1); the current level's map is
swapped into the `HudMap.pag` `Pure3dObject` slot (C29.1) when the level loads, and freed when it unloads —
the same streaming residency as the rest of a level (C12.3). Only one map model is resident at a time,
because you're only in one level at a time.

**What happens if you bend it.**

- *Edit the map model's geometry without its anchors* — icons and the player marker misalign (C29.5). Keep
  the `0x00007031`/`32` anchors consistent with the geometry.
- *Make the map too detailed* — it becomes unreadable at 120×120 and costs more to draw. Keep it simplified,
  as authored.
- *Swap in the wrong level's map* — you'll navigate by a map of a different place. The streaming system
  matches map to level (C12.3); respect it.
