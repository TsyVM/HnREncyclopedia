<p align="center">
  <img src="../hnrencyclopedia-logo.png" alt="The Simpsons: Hit &amp; Run Encyclopedia" width="440">
</p>

# The Simpsons: Hit & Run Encyclopedia v1.0.0 — Release Notes

**A complete engine-level reference for The Simpsons: Hit & Run (2003, PC — retail).**

The first complete edition: **36 chapters** built from first principles — a single Pure3D chunk header up to
the running game observed frame by frame — plus a **Legend** master index of every named thing in the game.
Every claim is grounded in either a re-runnable parse of the shipped files or the executable's own RTTI, with
confidence markers (✅ Verified / 🟡 Reasoned / ⏳ Open) throughout.

---

## Contents

- **36 chapters (C1–C36)**, each a hub plus 5–9 focused deep-dive pages:
  - **Foundations** — the Pure3D container model, Radical hashing, RCF archives, byte-level toolcraft.
  - **Assets** — textures, shaders, meshes, skeletons/skinning, geometry I/O.
  - **World** — scenegraph, collision, level composition, paths & the road network.
  - **Scripting** — MFK & CON languages, missions & objectives, choreography.
  - **Audio/Video** — RSD sound, the audio archives, Bink video.
  - **UI & text** — the Scrooby XML UI, fonts & localization, maps.
  - **Runtime** — the RTTI class model, vehicles, characters & AI, missions/cameras/physics.
  - **Systems** — GameFlow & loading, police & Hit-&-Run, combat/health/inventory, rendering/lighting/effects,
    animation channels, vehicle physics & drifting, cameras & camera effects.
  - **Persistence & modding** — save data & config, the modding toolchain.
- **The Legend** (`Legend/`) — the categorized master index: every function (212 script commands), vehicle
  (90), character (132), costume, texture name (751), object, mission, level & map, and class.
- **Glossary** (`Glossary/`) — terminology, the 179-ID master chunk table, extensions, file catalogue.
- **Tools** (`tools/`) — the reproducible P3D/RCF scanner that grounds every on-disk claim.

## By the numbers

- 36/36 chapters written to full depth · ~250 markdown files · every internal link resolving.
- 1,941 Pure3D files parsed (0 failures) · 179 chunk IDs · 1,207 RTTI-verified classes.
- Scoped strictly to *The Simpsons: Hit & Run* — no references to any other game.

## Honesty & scope

Confidence markers are used throughout. The handful of ⏳ **Open** items are stated plainly rather than hidden:
the standalone **P3DZ** codec (identified as `p3dcompress v1`, located in the exe, standard codecs ruled out —
C1.9), the undecoded payloads of the long tail of rare chunk IDs, the localized mission *display titles* (in
the TextBibles), and the `credits.rmv` Xbox-artefact container. Everything else is verified.

## Companion

Every format and class documented here is available programmatically in **DonutsSDK** — the C++20 modding SDK
with the verified chunk registry, class database (965 vtable addresses, 1,917 member offsets), and format
structs. Its sister release.

**Start here:** [`README.md`](../README.md) → the chapter map and the Glossary/Legend.
