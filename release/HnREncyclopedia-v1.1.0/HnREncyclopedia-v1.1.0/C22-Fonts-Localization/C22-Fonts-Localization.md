# Chapter 22 — Fonts, Glyphs & Localization

> **Goal of this chapter:** decode how the game renders text — the font atlases behind every glyph — and
> how it localizes it: the TextBibles that hold translatable strings and the hardcoded-vs-bible distinction
> that decides what gets translated.

Every word on screen — menu labels, mission instructions (C16.2), subtitles (C19.4) — is drawn from a
**font** and, if translatable, sourced from a **TextBible**. This chapter reads both from the retail data:
fonts and text bibles are Pure3D files (C7), and the text runtime is the verified `FeText`/`tTextureFont`
class set.

**Key finding (✅ verified):** a **font is a Pure3D texture atlas plus a glyph chunk** — `font1_14.p3d`
contains a `0x00019000` Texture (C5) and `0x00022000`/`0x00022001` font/glyph chunks. Localization runs
through **TextBibles** (`txtbible\srr2.p3d`, also Pure3D), and text elements are explicitly one of two kinds:
**`FeTextChildHardCodedString`** (fixed) or **`FeTextChildTextBibleString`** (translated).

---

## Deep-dive pages

- [C22.1 — Fonts as Pure3D Atlases](01-fonts-as-p3d.md): `font{N}_{size}.p3d` — a texture + a glyph table.
- [C22.2 — Glyphs & Text Rendering](02-text-rendering.md): `tTextureFont`, `FeText`, and laying out a string.
- [C22.3 — TextBibles: the Localized Strings](03-textbibles.md): `txtbible\*.p3d` and string lookup.
- [C22.4 — Hardcoded vs. Bible Strings](04-hardcoded-vs-bible.md): what gets translated, and what doesn't.
- [C22.5 — Languages & Editing Text](05-languages-editing.md): changing and adding text.

---

## 22.1 Fonts as Pure3D atlases (✅ verified)

A font is a `.p3d` file (C7) named `font{typeface}_{size}` — the retail set is `font0_16`, `font0_24`,
`font1_14`, `font2_12`, `font3_12` (typeface number + point size). Verified: `font1_14.p3d` contains:

```
0x00019000 Texture   +  0x00019001 Image  +  0x00019002 ImageData   → the glyph atlas (C5)
0x00022000 Font       +  0x00022001 Glyph table                      → char → atlas-position map
```

So a font is a **texture atlas** (all glyphs packed into one image) plus a **glyph table** mapping each
character to its rectangle in the atlas and its metrics. [C22.1](01-fonts-as-p3d.md).

## 22.2 Glyphs & text rendering (✅ verified)

Text is rendered by drawing, per character, a textured quad from the atlas. The runtime font classes:

```
tTextureFont / tTextureFontLoader     — texture-atlas font (the fonts above)
tImageFont / tImageFontLoader         — image-based font
```

A `Text` element (C21.3) with a `TextStyle` (C21.2 — a font) and a string lays out its glyphs left-to-right,
each a quad sampling the atlas, positioned by the glyph metrics. [C22.2](02-text-rendering.md).

## 22.3 TextBibles: the localized strings (✅ verified)

Translatable text lives in a **TextBible** — `txtbible\srr2.p3d` (Pure3D). A page declares it as a resource
(C21.2); a `Text` element references a **string by name** in the bible rather than embedding the words. To
translate the game you swap the bible, not the pages. [C22.3](03-textbibles.md).

## 22.4 Hardcoded vs. bible strings (✅ verified)

The runtime distinguishes two text sources explicitly:

```
FeTextChildTextBibleString   — text looked up in a TextBible (translated)
FeTextChildHardCodedString   — a fixed string baked into the page (not translated)
```

A number, a debug label, or a symbol is hardcoded; anything the player reads as language is a bible string.
[C22.4](04-hardcoded-vs-bible.md).

## 22.5 Languages & editing (✅ verified path)

Because bible strings are looked up by name, the game localizes by loading the language's TextBible. Editing
text is editing the bible (for translated text) or the page XML (for hardcoded text). [C22.5](05-languages-editing.md).

---

## Key takeaways

- A **font is a Pure3D texture atlas + a glyph chunk** (`0x00019000` Texture + `0x00022000`/`01`); the set is
  `font{typeface}_{size}.p3d` (5 fonts).
- Text renders as per-glyph textured quads via `tTextureFont`/`FeText`.
- **Localization** runs through **TextBibles** (`txtbible\*.p3d`): a `Text` element references a string *by
  name*, so translation swaps the bible, not the layout.
- The runtime explicitly splits **`FeTextChildTextBibleString`** (translated) from
  **`FeTextChildHardCodedString`** (fixed).
- Editing text = editing the bible (translated) or the page XML (hardcoded).

**Next:** [Chapter 27 — Save Data & `simpsons.ini`](../C27-Save-Config/C27-Save-Config.md).
