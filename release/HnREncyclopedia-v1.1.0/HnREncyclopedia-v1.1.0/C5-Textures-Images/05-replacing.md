# C5.5 — Replacing Textures

**What it is.** Putting a new picture *into* a `.p3d` so the game loads it. This is the most common art
mod, and it splits cleanly into the easy case (same size) and the careful case (different size).

**The easy case — length-preserving.** If your replacement encodes to **exactly** the same number of bytes
as the original Image-Data leaf, overwrite the payload in place and you are done: no size changes, no
ancestor fix-ups (C1.5). Same-dimension, same-format retextures fall here — a new 64×64 paletted skin over
an old one. This is why retexturing is the safest mod in the game.

```python
def replace_same_size(buf, leaf_off, leaf_size, new_payload):
    assert len(new_payload) == leaf_size, "use the resize path (C5.5) for a different length"
    return buf[:leaf_off+12] + new_payload + buf[leaf_off+12+leaf_size:]
```

**The careful case — resizing.** If the new image is a different byte length (bigger, smaller, or a
different format/dimensions), you must:

1. Replace the Image-Data payload.
2. Update the **Texture descriptor** (C5.1) if width/height/bpp/mips changed — the header must match the
   new pixels.
3. Run the **ancestor size fix-up** (C1.5): the Image-Data `chunkSize`, then the Image, then the Texture,
   then the file header, each adjusted by the byte delta.

The safe way to do all three is to parse the file into a tree, swap the payload and header, and re-emit
bottom-up with the C4.1 writer — which recomputes every size, so no ancestor can be left stale.

**Why the two cases matter.** The length-preserving path lets a modder change every texture in the game
with a hex editor and never think about the size tree — which is exactly how most SHAR skins are made. The
resize path is where mistakes happen, and the whole reason C1.5 exists: one forgotten ancestor size and the
file desyncs on load. Knowing which case you are in *before* you start is half the battle.

**Matching the format.** Keep the replacement in the *same* encoding as the original unless you also update
the descriptor: a paletted slot wants a paletted image (C5.3). Re-encoding a PNG source to the game's format
is the pipeline step; the loose `.png` art (C5.3) shows what the originals looked like before packing.

**What happens if you bend it.**

- *Overwrite with a different-length payload on the "easy" path* — you shift every following byte and break
  the size tree. Check the length; if it differs, take the resize path.
- *Change dimensions but not the descriptor* — the loader reserves the old size and mis-reads the new
  pixels. Header and payload must agree.
- *Resize and forget an ancestor* — desync on load (C1.7). Re-emit the tree with the size-computing writer
  rather than poking bytes.
