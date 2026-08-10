# C22.3 — TextBibles: the Localized Strings

**What it is.** The store of the game's translatable text — a "TextBible" — and the by-name lookup that lets
the UI reference a string without embedding its words. This is the heart of localization: separate the
*words* from the *layout* so translating the game doesn't touch the pages.

**How it works (✅ verified).** A TextBible is a Pure3D file: `txtbible\srr2.p3d` (verified magic `P3Dÿ`). A
page declares it as a resource (C21.2):

```xml
<TextBibles><TextBible name="srr2" data="txtbible\srr2.p3d" inventoryName="srr2"/></TextBibles>
```

Inside, the bible holds the game's strings keyed by an identifier. A `Text` element (C21.3) that shows
translatable text references a **string name** in the bible rather than the literal words (C22.4). At render,
the text system looks the name up in the loaded bible and draws the resulting string with the element's font
(C22.2). So the page says "show string `MISSION_START`," and the bible provides the actual text — in whatever
language's bible is loaded.

**Why "bible."** It's Radical's term for the master string table — the single source ("bible") of all the
game's words. Centralising every translatable string in one asset (per language) means: translators work on
one file, not scattered through hundreds of pages; the UI layout is language-agnostic; and switching language
is loading a different bible. The name `srr2` is the bible's internal id (the "SRR"/Simpsons lineage tag);
there's one bible per Scrooby tree (`scrooby` and `scrooby2`), the shipped one being `scrooby2/…/srr2.p3d`.

**Why store strings in Pure3D.** Putting the bible in a `.p3d` (rather than a plain text file) lets it ride
the same asset pipeline (C1/C23.4) as everything else — it loads, streams, and is referenced by name through
the VFS (C3.6) exactly like a texture or a font. The strings live in a text chunk inside the container. It's
the same instinct as fonts-in-P3D (C22.1) and the mission scripts being compiled into `scripts.rcf` (C3): one
asset pipeline for everything, including text.

**The localization architecture.** Three pieces make it work: the **page** (C21) references a string by name;
the **bible** (here) maps names to words for one language; the **`CGuiManagerLanguage`** (C21.5) selects the
language and loads the matching bible. Change the language and the same pages, with the same layout and fonts,
show different words — because only the bible changed. This clean separation is why a licensed game could ship
in many languages without re-authoring its UI.

**What happens if you bend it.**

- *Embed translatable words in a page instead of the bible* — they won't translate (they become hardcoded,
  C22.4). Put player-facing text in the bible.
- *Reference a string name not in the bible* — the lookup fails and the text is blank or a fallback. Ensure
  the name exists.
- *Edit words in one language's bible only* — the others still show the old text. Update every language's
  bible (C22.5).
