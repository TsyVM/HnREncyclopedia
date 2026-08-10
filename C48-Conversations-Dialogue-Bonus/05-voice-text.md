# C48.5 — Voice & Text

> Voice & Text — grounded in the verified level-init dialogue vocabulary.

The spoken conversation lines stream from the dialogue audio archive dialog.rcf (C19) — one of the game's five sound RCFs — as RSD samples (C18). Subtitles/on-screen text come from the localized string tables (C22), so the same scene speaks the right language. The conversation system triggers the right line at the right shot. Why: separating voice (audio archive) from staging (script) from text (localization) lets each be produced and localized independently. Bend it: swap a voice line by replacing its RSD in the archive; change subtitles via the string tables.

## Cross-references
C16 (missions), C36 (cameras), C42 (gesture animations), C19 (dialogue audio), C22 (localized text), C8 (locators), C44 (level init).
