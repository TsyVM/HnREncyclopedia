# C5.3 — Formats: BMP, PNG & Palettes

**What it is.** What the Image-Data leaf actually contains, and how to know which decoder to point at it.
The Texture header (C5.1) selects the format; the payload is the encoded pixels in that format.

**How it works.** Two signals tell you the encoding: the **name extension** (stored in the clear — C5.1)
and the **`bpp`/`textureType`** fields. Verified names in the retail data carry honest extensions —
`flag.bmp`, `flarebase2.bmp` are BMP-derived — and the loose source art is **930 `.png` files** (28.5 MB)
under `art/`, the pipeline inputs from which the packed textures were built. So the format vocabulary is
small and identifiable: BMP-style true-colour or paletted images, with PNG as the source form.

**Palettes.** A low `bpp` (e.g. 4 or 8) indicates a **paletted** image: the payload is indices into a
colour table rather than direct pixels. Paletted textures were the norm on 2003 hardware for memory
reasons — a 64×64 paletted image is a quarter the size of true-colour. When `bpp` is small, expect a
palette in or alongside the payload and decode indices→colours; when it's large, expect direct RGBA.

**Why it's built this way.** Storing images in a known desktop format (BMP/PNG-derived) rather than a
bespoke codec made the 2003 art pipeline simple — artists worked in PNG, the build packed them — and keeps
extraction easy today: the payload is close to a file you can already open. The `bpp`/`type` selector lets
one Texture chunk describe several encodings without changing structure, so the loader branches on two
numbers rather than parsing a format header.

**Identifying a payload in practice.** Read the Texture header for `bpp`/`type`, check the name extension,
then confirm by peeking the payload's own magic (a BMP starts `42 4D "BM"`, a PNG `89 50 4E 47`). The
[Glossary identifier](../Glossary/extensions.md#a-portable-identifier) already recognises PNG; extend it
with BMP for embedded texture payloads. When header, name, and payload magic agree, you have the format
with confidence (the C4.4 cross-check).

**What happens if you bend it.**

- *Decode a paletted image as true-colour* (or vice versa) — you get noise or a quarter of the image. Read
  `bpp` first and branch.
- *Replace a paletted texture with a true-colour payload without updating `bpp`/dimensions* — the loader
  reserves the wrong size and mis-reads it. Keep the header and payload format in agreement (C5.5).
- *Trust the extension alone* — the name says intent, but the `bpp`/`type` and the payload magic are the
  truth. Cross-check all three.
