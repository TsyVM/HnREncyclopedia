# C4.2 — Tree Dumpers & Annotation

**What it is.** The tool you run *first* on every file: a recursive dumper that prints the chunk tree as
an indented outline, annotated with chunk-type names from the [master table](../Glossary/chunk-ids.md)
and, where you have them, recovered asset names (C2.5). It converts "2,325 bytes of binary" into a page
you can read.

**How it works.** Walk the tree (C1.3), and at each chunk print depth-indentation, the id, its role, its
sizes, and any name you can attach:

```python
def dump(path, type_names=None, asset_names=None):
    buf = open(path, 'rb').read()
    assert buf[:4] == b'P3D\xff', "not Pure3D"
    _, hs, fs = struct.unpack_from('<III', buf, 0)
    type_names = type_names or {}
    for cid, off, h, d, depth in walk_tree(buf, hs, min(fs, len(buf))):
        role = 'C' if h < d else 'L'
        tname = type_names.get(cid, '')
        # Optional: if this chunk carries a name in its own data, resolve it (C2.5)
        print(f"{'  '*depth}0x{cid:08X} [{role}] {tname:<22} h={h} d={d} @{off}")
```

Feed it the type-name table and the output reads like a table of contents: `0x00019000 [C] Texture`,
`0x00011000 [C] Old Primitive Group`, `0x03F00003 [C] Scenegraph Transform`. Feed it a recovered
name map and a shader's texture reference prints as `-> homer_body` instead of `-> 0x1A2B3C4D`.

**Why dump first.** Three payoffs before you decode a single field:

1. **Classification.** The dominant id family (C2.3) tells you what the file *is* — art, collision, scene
   graph, level — and therefore which chapter to open.
2. **A map for diffing.** When you diff two versions of a file (C4.3), the dump tells you which *chunk*
   the changed bytes fell in, turning a raw byte offset into "the third param of the shader."
3. **A desync detector.** A dump that ends before the file does, or prints an id not in the master table,
   is a desync (C1.7) — the dumper is also your first validator.

**Annotation levels.** Build the dumper to take three optional maps and it scales from anonymous to fully
named:

- *type_names* — the closed 179-id table (always available, generated).
- *asset_names* — your recovered hash→name dictionary (C2.4), growing over time.
- *decoders* — per-family functions that print a chunk's decoded fields inline (added chapter by chapter,
  C4.6). Early on you have only the first; by the end the dump reads like source.

**A histogram mode.** For triage across many files, a counting dump (no per-chunk print, just totals) is
what produced the census and the master table. The same walk, a `Counter` instead of a `print` — that is
literally [`tools/p3d_rcf_scan.py`](../tools/p3d_rcf_scan.py). Keep both modes in one tool.

**What happens if you bend it.**

- *Dump without the master table* and you are reading raw hex ids — workable, but you lose the instant
  classification and the desync check the name lookup gives you. Always pass the table.
- *Trust the type names as proven* — they are 🟡 (C2.6). The *structure* the dump shows (roles, sizes,
  nesting) is ✅; the names are signposts. Decode the chunk to confirm.
- *Let the dumper swallow exceptions* to "get through" a file — a dump that hides a desync is worse than
  one that stops at it. Let it raise; the raise is the finding.
