# C9.5 — Round-Trip Validation

**What it is.** The test that proves your import/export pipeline is correct: export a mesh, re-import it
**unchanged**, and diff the result against the original. If they match, the pipeline is lossless and you can
trust it with real edits. It's the acid test of Part II.

**How it works (✅ the C4.3 diff, applied to geometry).**

```
original.p3d  ──export──►  mesh.obj/gltf  ──import──►  rebuilt.p3d
                                                            │
original.p3d  ◄────────── diff ──────────────────────────► rebuilt.p3d
```

Run the export (C9.3) and import (C9.4) with **no edit in between**, then byte-diff `rebuilt.p3d` against
`original.p3d` (or, more forgivingly, compare the *decoded geometry* — positions, UVs, colours, indices —
since a lossless rebuild may reorder bytes but must preserve the geometry). A clean match means:

- The **stream decode** (C7.3) is correct — you read positions/UVs/colours right.
- The **topology handling** (C7.4) is correct — strips convert to triangles and back faithfully.
- The **coordinate boundary** (C9.2) is correct — export then import cancels out (round-trips to identity).
- The **size fix-up** (C9.4/C1.5) is correct — the rebuilt file's sizes balance and it loads.

Any mismatch localises the bug: wrong positions → stream decode; scrambled faces → topology; mirrored →
coordinate boundary; won't load → size tree.

**Why identity first, edits second.** It's tempting to jump to editing geometry, but an edited mesh that
"looks right" in your tool can still fail in-game for pipeline reasons (bad axis, stale size) that you'd blame
on the edit. The identity round-trip **isolates the pipeline from the edit**: if export→import→identity is
lossless, then any later failure is your *edit*, not your pipeline. Establish the lossless round-trip once,
and every real edit afterward stands on proven ground. This is the C4.4 discipline — prove the tool before
trusting its output.

**The two-way check.** For full confidence, validate in *both* directions where you can: geometry that
round-trips to identity (here), and a specific *edit* that produces the *expected* change in-game (move a
vertex, see it moved). The identity test proves losslessness; the edit test proves the edit does what you
meant. Two independent checks converging (C28.6) is the strongest confidence.

**Loading through the real game.** The final validation is the game itself (C1.8): a rebuilt file that the
retail loader accepts and draws correctly is, by definition, a valid file — the engine and your walker run
the same walk (C1.8), so a file the game loads is one your pipeline built correctly. Test through the real
loader before you ship; a file that round-trips in your tools *and* loads in the game is proven twice.

**What happens if you bend it.**

- *Skip the identity round-trip* — you can't tell pipeline bugs from edit bugs. Prove identity first.
- *Diff bytes when a lossless rebuild reorders them* — compare decoded geometry, not raw bytes, if your
  writer reorders. Match on meaning.
- *Trust a tool preview over the game* — the game's loader is the truth (C1.8). Test in-game.

**Next:** [Chapter 10 — The Scenegraph](../C10-Scenegraph/C10-Scenegraph.md).
