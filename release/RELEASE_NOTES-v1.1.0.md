# HnREncyclopedia v1.1.0

A complete engine-level reference for *The Simpsons: Hit & Run* (2003, PC retail),
byte-level and RTTI-verified.

## New since v1.0.0
- **39 chapters** (was 36). Three new chapters extend the modding coverage:
  - **C37 — Options: Display, Audio, Controls & Graphics Settings**: the in-game
    Options menu, all 13 confirmed settings-screen classes, every `simpsons.ini`
    key, and why PC has no separate graphics-quality menu.
  - **C38 — Extending the Menu System**: the five-layer UI stack and how to add
    your own menu/screen to the internal game menu.
  - **C39 — Engine Limits**: the three-tier limit taxonomy (script-configurable /
    pool-bounded / hard), how to raise each safely, and the add-content pipeline.
- **Redesigned README** with a full clickable chapter index (all 39 chapters).
- Grounded in the new **SAHRDiag** static + live-capture evidence (the C28.7
  page documents the tool and the 100%-verified runtime findings).

## Contents
- 39 chapters (a hub + 5–9 deep-dive pages each), the 10-file **Legend** master
  index, and the **Glossary** (terminology, chunk-ID table, extensions, file
  catalogue).
- `tools/p3d_rcf_scan.py` — reproduce every on-disk claim against your own copy.

## Provenance
On-disk findings are reproducible with `tools/`; runtime findings come from
`Simpsons.exe`'s own RTTI (carried by DonutsSDK, re-derivable with SAHRDiag).
MIT licensed.
