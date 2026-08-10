# C22.1 — Fonts as Pure3D Atlases

**What it is.** How the game stores a font: not as a TrueType file, but as a Pure3D asset (C7) combining a
**texture atlas** of all the glyphs with a **glyph table** that says where each character sits in the atlas.
It's the classic game-font design, and it reuses the engine's existing texture pipeline.

**How it works (✅ verified).** A font is a `.p3d` file named `font{typeface}_{size}`. The retail set:

```
font0_16.p3d   font0_24.p3d    (typeface 0 at 16 and 24 point)
font1_14.p3d   font2_12.p3d   font3_12.p3d
```

Decoded, `font1_14.p3d` contains two things:

```
0x00019000 Texture → 0x00019001 Image → 0x00019002 ImageData   the glyph ATLAS (C5)
0x00022000 Font    +  0x00022001 Glyph table                    the char → atlas map (🟡 name)
```

The **atlas** is an ordinary texture (C5) — a single image with every glyph drawn into it, packed to save
space. The **glyph table** (`0x00022000`/`0x00022001`) maps each character code to its rectangle in the
atlas plus its metrics (width, bearing, advance) so the renderer knows where to sample and how much to
advance the cursor. Together they are everything needed to draw text: the pixels (atlas) and the layout data
(table).

**Why one font per size.** Note `font0_16` and `font0_24` are the *same typeface* at *different sizes* — the
game bakes each point size as its own atlas rather than scaling one font. This is a 2003-era choice: scaling
a texture-atlas glyph blurs it, so pre-rendering each needed size at full crispness looks far better on
low-resolution SD displays (C21.1). The cost is a few extra atlases; the benefit is sharp text at every size
the UI uses. Five fonts cover the game's needs — a couple of typefaces at the handful of sizes the menus and
HUD require.

**Why a texture atlas.** Packing all glyphs into one texture means drawing text is drawing quads from one
already-loaded texture — no per-glyph texture switches, which are expensive on the hardware. It also lets the
font ride the engine's normal texture pipeline (C5): a font atlas loads, uploads, and binds exactly like any
other texture, so text rendering reuses the whole shader/texture path (C6/C5) rather than needing a separate
font system. The `0x00022000` glyph chunk is the only font-specific addition; everything else is the texture
machinery you already know.

**Reading a font.** Open the `.p3d` (C1), extract the atlas texture (C5.4) to see the glyphs, and decode the
`0x00022000` glyph table for the character map. The `inventoryName` a page's `<TextStyle>` uses
(`Tt2001m__14`, C21.2) is the font's internal name — the handle the text system looks it up by.

**What happens if you bend it.**

- *Scale a font atlas to a new size* — glyphs blur. Use (or bake) the atlas at the size you need, as the
  game does.
- *Edit the atlas image but not the glyph table* — glyph rectangles no longer match the pixels; text draws
  the wrong regions. Keep the atlas and table consistent.
- *Add a character to the atlas without a glyph-table entry* — the renderer can't find it; it draws nothing
  or a fallback. Update the table.
