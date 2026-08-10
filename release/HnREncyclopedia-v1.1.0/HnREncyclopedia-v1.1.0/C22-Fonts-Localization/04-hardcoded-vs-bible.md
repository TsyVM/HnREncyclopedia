# C22.4 — Hardcoded vs. Bible Strings

**What it is.** The explicit distinction the engine draws between text that gets translated and text that
doesn't — two verified classes that decide, per text element, whether its words come from the TextBible
(C22.3) or are baked into the page.

**How it works (✅ verified).** From `shar_dumps.csv`, a `Text` element's string is one of two child types:

```
FeTextChildTextBibleString   — the string is looked up in a TextBible (C22.3) → TRANSLATED
FeTextChildHardCodedString   — the string is fixed in the page               → NOT translated
```

Plus `CGuiTextBible` / `FeTextBible` / `FeTextBibleLoader` (the bible loading/lookup machinery). So every
piece of on-screen text is explicitly marked, at the class level, as translatable or not. When a page loads a
`Text` element (C21.3), it becomes one of these two children depending on how the string was authored.

**What's hardcoded vs. bibled.** The rule follows *meaning*:

- **Bible strings** (translated): anything the player reads *as language* — menu labels, mission
  instructions (C16.2), subtitles (C19.4), item names, tutorial text. These reference the bible by name so
  each language shows its own words.
- **Hardcoded strings** (fixed): text that is *not* language — numbers (a coin count, a timer), symbols,
  debug labels, or strings that are identical in every language. A "3" is a "3" in French; baking it saves a
  bible lookup and a translation entry.

This is the standard localization discipline: translate meaning, hardcode the language-independent. Marking
it in the type system (two classes) rather than by convention means the engine *knows* which strings to route
through the bible and which to draw as-is — no ambiguity, no accidental un-translated menu label.

**Why make it a class distinction.** Encoding "translated vs. fixed" as two `Text` child classes has two
payoffs. First, **correctness**: a translatable string *must* go through the bible, and making it a distinct
type enforces that at load — you can't accidentally hardcode a menu label if the tooling emits a
`TextBibleString` for it. Second, **efficiency**: a hardcoded string skips the bible lookup entirely, which
matters for text that updates every frame (a live timer or score). The type distinction is both a
correctness guarantee and an optimisation.

**Reading which is which.** A `Text` element that references a bible string name is translatable; one with
literal words baked in is hardcoded. When editing (C22.5), this tells you *where* to change the words: a
bible string is edited in the bible (and affects all uses in that language); a hardcoded string is edited in
the page XML (and affects only that element, in all languages).

**What happens if you bend it.**

- *Hardcode a translatable label* — it shows the same words in every language (untranslated). Route
  player-facing text through the bible (C22.3).
- *Bible-reference a language-independent symbol* — you add a needless translation entry and lookup. Hardcode
  the truly fixed.
- *Rely on a text-child class offset* — classes ✅, offsets ⏳. Diff (C4.3).
