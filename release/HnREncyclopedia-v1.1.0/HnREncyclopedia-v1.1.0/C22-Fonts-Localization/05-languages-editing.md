# C22.5 — Languages & Editing Text

**What it is.** How the game switches languages and how you change or add text — the practical close to the
UI block. It follows directly from the bible/hardcoded split (C22.4): where a string lives determines how you
edit it.

**How language switching works (✅ verified).** `CGuiManagerLanguage` (C21.5) is the manager for language
selection; selecting a language loads that language's **TextBible** (C22.3). Because every translatable `Text`
element references its string *by name* (C22.4), the same pages — same layout, same fonts — resolve those
names against the newly-loaded bible and show the new language's words. Nothing about the UI's structure
changes; only the bible does. This is the whole point of the bible architecture (C22.3): language is a
data swap, not a re-layout.

**Editing text — three cases.**

1. **Change a translated string** → edit the **TextBible** (C22.3). The bible is a `.p3d`, so this means
   editing the string chunk inside it (extract, edit, repack — C1). The change affects every place that
   string name is used, in that language. To change all languages, edit each language's bible.
2. **Change a hardcoded string** → edit the **page XML** (C21). The words are baked into the `Text` element
   (C22.4); change them there. This affects only that element, in all languages.
3. **Add new text** → declare a bible string (translated) or hardcode it (fixed), then add a `<Text>` element
   (C21.3) referencing it, styled with a `<TextStyle>` font (C21.2/C22.1).

**Fitting the layout.** Translated text varies in length — German is famously longer than English — so a
`Text` element's box (`<Dimension>`, C21.3) must accommodate the longest language, or the text clips or
overflows. This is why the layout is language-agnostic but the *boxes* are sized for the worst case: the
page author leaves room, and each language's bible fills it. When adding text, size the box for the longest
translation, not just English.

**The font constraint.** A language needs glyphs for its characters, and the fonts are baked atlases (C22.1)
with a fixed glyph set. Languages using characters outside a font's atlas need a font that includes them —
which is why localized builds may ship different font atlases. When adding text in a new script, ensure the
font has the glyphs (C22.1), or add them to the atlas and glyph table.

**The whole text picture.** Putting C22 together: text renders from **font atlases** (C22.1) as per-glyph
quads (C22.2); translatable words come from **TextBibles** (C22.3) looked up by name; the engine explicitly
marks each string **translated or hardcoded** (C22.4); and switching language swaps the bible (here). Fonts
and bibles are both Pure3D (C7), riding the one asset pipeline. Editing text is editing the bible or the page
XML — approachable, like the rest of Scrooby (C21.6).

**What happens if you bend it.**

- *Add text longer than its box* — it clips or overflows. Size `<Dimension>` for the longest language
  (C21.3).
- *Use a character the font lacks* — it draws nothing or a fallback. Ensure the font atlas has the glyph
  (C22.1).
- *Edit one language's bible and call it done* — the others are unchanged. Update every language's bible.

**Next:** [Chapter 27 — Save Data & `simpsons.ini`](../C27-Save-Config/C27-Save-Config.md).
