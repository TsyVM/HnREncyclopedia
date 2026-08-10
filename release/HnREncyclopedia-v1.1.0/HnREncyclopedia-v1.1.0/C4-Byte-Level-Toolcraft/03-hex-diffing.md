# C4.3 — Hex Diffing: Finding What a Change Touched

**What it is.** The highest-yield reverse-engineering technique for a game like this: to find where a
value lives, **change exactly one thing, then diff the bytes.** The bytes that differ are the field. It
turns "where is top speed stored?" from a research project into a two-minute experiment.

**How it works.** Take a file (or a live memory region), record it, make a single minimal change through
the game's own tools or UI, record it again, and compare byte-for-byte:

```python
def diff(a, b):
    """Yield (offset, old, new) for every differing byte between two equal-length blobs."""
    n = min(len(a), len(b))
    i = 0
    while i < n:
        if a[i] != b[i]:
            j = i
            while j < n and a[j] != b[j]: j += 1
            yield i, a[i:j], b[i:j]        # a run of changed bytes
            i = j
        else:
            i += 1
    if len(a) != len(b):
        yield n, a[n:], b[n:]              # tail: a length change
```

A run of four changed bytes that reads as a float you recognise (e.g. `130.0 → 160.0` on a
`SetTopSpeedKmh` edit) is your field, at that offset, of that type. Cross-reference the offset against a
[tree dump](02-tree-dumpers.md) of the same file and you also know *which chunk* it belongs to.

**Why it's so effective in SHAR specifically.** Two reasons this game rewards diffing more than most:

1. **The tunables are in plain text.** Vehicle handling, mission parameters, and level setup live in
   `.con`/`.mfk` scripts (Chapters 14–16). You often don't even need a binary diff — you change
   `SetTireGrip(2.5)` to `3.5`, and the "diff" is one legible line. The script layer is a giant,
   pre-labelled field map.
2. **Length-preserving edits are common.** Overwriting a float with a float, a DXT block with a DXT
   block, keeps the file the same length, so the diff is a clean set of point changes with no offset
   shift — the easiest kind to read.

**Diffing live memory vs. files.** The same technique works against the running process: freeze a value
with a trainer or the DonutsSDK runtime, note the address, change it in-game, and the address that
tracks the on-screen value is your runtime field. This is how ⏳-Open member offsets get promoted to
known ones — the file diff finds the *on-disk* field, the memory diff finds the *runtime* field, and a
chapter's job is often to connect the two (the value read from the `.con` at load into the offset it
occupies in the live `Vehicle`).

**Discipline: change one thing.** The method only works if a single variable moved. Change two sliders
and you cannot tell which bytes belong to which. Minimise the edit, diff, record, then change the next
thing. Keep a log of `(what I changed) → (offset, type, chunk)`; that log *is* your reverse-engineering of
the format.

**What happens if you bend it.**

- *Change several values at once* and the diff is ambiguous — you get a set of changed offsets with no
  mapping to causes. One variable per diff.
- *Diff files of different lengths and assume aligned offsets* — a length change shifts everything after
  it, so a naive byte-diff reports the whole tail as "changed." Diff length-preserving edits, or align on
  chunk boundaries first.
- *Trust one diff as proof of type* — confirm by making a *second*, different change to the same field and
  checking the same offset moves. One diff suggests; two confirm.
