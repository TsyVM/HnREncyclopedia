# RE-Data & Discoveries

The machine-readable backbone of the HnR Encyclopedia: every dumped dataset as JSON, so a
reader (or a tool) can consume the raw facts the chapters explain. This mirrors the discipline
of the companion **DonutsSDK** data set and the **SAHRDiag** diagnostic — one extraction, many
consumers, all reproducible on a retail copy.

- **[`data/`](data/README.md)** — 24 JSON tables: the class model (vtables, offsets, sizes,
  composition), the Pure3D chunk table, the full script command vocabulary, gags, interiors,
  the transition/animation class map, event names, and the engine's own limit strings. Each is
  indexed with row counts and provenance in [`data/README.md`](data/README.md).

Everything is tagged ✅ verified / 🟡 reasoned / ⏳ open, and every address is bound to retail
`Simpsons.exe` (MD5 `b3a47b881eec97745424b1e2c86cdcaf`). Regenerate from your own copy with the
tools in `../tools/` and `../../DonutsSDK/tools/`.
