# C22.2 — Glyphs & Text Rendering

**What it is.** How a string becomes pixels: the runtime font classes and the per-glyph quad-drawing that
lays text out from an atlas (C22.1). This is the render side of text, feeding the Scrooby `Text` element
(C21.3).

**How it works (✅ verified).** The verified font runtime:

```
tTextureFont : … / tTextureFontLoader     — a texture-atlas font (the font{N}_{size}.p3d fonts, C22.1)
tImageFont   : … / tImageFontLoader        — an image-based font variant
```

To draw a string, the renderer walks its characters and, for each, looks up the glyph in the font's table
(C22.1) to get its atlas rectangle and metrics, then draws a **textured quad** sampling that rectangle,
advancing the cursor by the glyph's advance width. Kerning and line breaks come from the metrics and the
`Text` element's `<Dimension>` (C21.3). The quads are drawn through the same texture/shader path as any
sprite (C5/C6) — text is just many small textured quads from the font atlas.

**The `Text` element pipeline.** A Scrooby `<Text>` element (C21.3, 274 of them) ties three things together:
a **string** (from a TextBible or hardcoded, C22.4), a **TextStyle** (a font, C21.2), and layout properties
(position, dimension, justification, colour). At render, the element resolves its string, picks its font
(`tTextureFont`), and lays out the glyphs within its box with the given justification and colour. So the
274 text elements across the UI each become a run of atlas quads, styled and positioned by their page.

**Why texture-font over vector.** Rendering vector fonts (TrueType) at runtime needs a rasterizer and is
costly on 2003 consoles; a pre-baked texture atlas needs only quad-drawing, which the hardware does trivially.
The trade is flexibility (fixed sizes, C22.1) for speed and simplicity. `tImageFont` vs. `tTextureFont` are
two flavours of the same idea — image-based vs. texture-atlas glyphs — letting the engine pick per font. For
a UI with a bounded set of sizes and languages, baked fonts are the right call, and they're why text renders
as cheaply as sprites.

**Colour and style.** A `Text` element's `<Colour>` (C21.3) tints the glyph quads — the atlas glyphs are
typically white so any colour multiplies cleanly (the same tint mechanism as sprite colour, C21.3). This is
how one font atlas serves many colours: white glyphs, tinted per element. Justification centres/aligns the
run within the element's box; translucency blends it (C21.3).

**What happens if you bend it.**

- *Rely on a `tTextureFont`/`FeText` member offset* — the classes are ✅, offsets ⏳. Diff (C4.3).
- *Expect runtime scaling to look crisp* — baked atlases don't scale well (C22.1). Use the right size font.
- *Colour text via the atlas instead of the element* — tint through the `Text` element's `<Colour>`; keep
  the atlas neutral so it's reusable.
