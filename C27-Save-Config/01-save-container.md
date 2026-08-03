# C27.1 — The Save Container (`Save1`)

**What it is.** The file that holds a player's whole career — `Save1`, a 7,194-byte binary. This page decodes
its top-level structure: a header, the player-slot name, and the fixed-stride record arrays that follow.

**How it works (✅ verified).** The file opens with a header and the slot name, read from a real `Save1`:

```
@0:   BA 07 EA 07               header word(s) — magic/version or checksum (🟡)
@4:   03 04 0C 19 0B 00 01 00   a timestamp-like field (save date/time — 🟡)
@17:  "Player1"                 the player-slot / profile name (a string)
…     numeric progress region (coins, current level, position — C27.2)
@409: mission-completion records — 32-byte stride, holding "sr1","sr2","sr3","bm1","gr1"
@4397: reward/car records — 24-byte stride, holding "famil_v" then "n/a" placeholders
```

The shape is the classic **console-save layout**: a small header, then **fixed-size record arrays** for each
category of persistent data. Records are addressed by a constant stride (32 bytes for missions, 24 for
rewards), so the game reads them as simple arrays — record *i* is at `base + i·stride`. Empty slots hold a
sentinel (`n/a` for unfilled rewards, `NULL` elsewhere), so the array is always full-size regardless of how
much the player has unlocked.

**Why fixed-stride records.** A save must be written and read fast and reliably on a memory card (C27.3),
where the layout has to be predictable. Fixed-size records in fixed-position arrays make that trivial: the
game knows exactly where every field lives (no parsing, no variable-length structures), can update one record
in place, and can allocate the save at a known size. The `NULL`/`n/a` sentinels mean the arrays are
pre-sized to the maximum (every possible reward slot exists, filled or not), so the file size never changes —
which matters for memory-card allocation. This is the opposite of the chunk-tree formats (C1): where those
are variable and self-describing, a save is flat and fixed, because a save prioritises fast, reliable,
in-place updates over flexibility.

**The header and integrity.** The leading bytes (`BA 07 EA 07`) are a magic/version or a checksum (🟡 — not
byte-proven here), and the following 8 bytes read as a **timestamp** (the save's date/time). Console saves
typically carry a **checksum** to detect corruption or tampering — if `Save1` has one, editing the save body
without fixing the checksum would make the game reject the save. This is the main hazard of save editing
(C27.5): the record *structure* is readable, but an integrity field may guard it.

**Reading a save.** To inspect a save, read the player name (@17), then walk the record arrays: the
32-byte-stride array from @409 lists completed bonus missions; the 24-byte-stride array from @4397 lists
unlocked cars (`famil_v` = the family car unlocked; `n/a` = an empty slot). The numeric regions between hold
coins and progress (C27.2). This gives you the player's whole career state from the bytes.

**What happens if you bend it.**

- *Edit the save body without fixing a checksum* — the game may reject the save as corrupt (C27.5). Identify
  and update any integrity field first.
- *Assume variable-length records* — the arrays are fixed-stride; record *i* is at a computed offset. Don't
  shift records.
- *Overwrite a sentinel expecting an unlock* — `n/a`/`NULL` slots have a specific format when filled; match
  it (C27.2), don't just replace the text.
