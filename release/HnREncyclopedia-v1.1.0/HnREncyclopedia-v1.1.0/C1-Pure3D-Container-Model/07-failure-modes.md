# C1.7 — Failure Modes & Forensics

**What it is.** A field guide to a **desynced walk** — what it looks like, and how to find the exact
byte where a good parse went bad. Since the whole format is one repeated step (`off += chunkSize`), a
single wrong step poisons everything after it, so the skill is locating step zero of the failure.

**How a desync presents.** After the walk steps to a wrong offset, it reads whatever bytes happen to be
there as a header. That produces one of three tells:

1. **Absurd sizes.** A `chunkSize` of `0x6C620000` or a `headerSize` larger than the file — you are
   reading data bytes (often ASCII, floats, or pixels) as a size field. This is the most common tell.
2. **An id that never occurs.** The [master table](../Glossary/chunk-ids.md) is the closed set of 179
   ids that exist in the retail data. An id outside it (especially one that looks like ASCII, e.g.
   `0x74736166` = "fast") means the cursor is inside a name or a data blob, not on a header.
3. **`headerSize > chunkSize`.** Structurally impossible in a good file (C1.2); it means the two `uint32`
   you read straddle a real boundary — you are half a chunk off.

**The forensic method.** Walk with a log of `(offset, id, headerSize, chunkSize)` and find the **last
plausible chunk** — the last one whose id is in the master table and whose sizes are sane. The desync
began at *its* `off + chunkSize`. Now inspect that offset by hand:

```python
def diagnose(path, names):
    buf = open(path, 'rb').read()
    _, hs, fs = struct.unpack_from('<III', buf, 0)
    off, last_good = hs, None
    while off + 12 <= min(fs, len(buf)):
        cid, h, d = struct.unpack_from('<III', buf, off)
        sane = (12 <= h <= d) and (off + d <= len(buf)) and (cid in names)
        if not sane:
            print(f"DESYNC at @{off}. Last good chunk ended here.")
            if last_good: print(f"  suspect parent/leaf: {last_good}")
            print("  bytes:", buf[off:off+16].hex(' '))
            return
        last_good = (hex(cid), off, h, d)
        off += d
    print("clean walk")
```

**The usual root causes, ranked.**

- **Stepped `headerSize` instead of `chunkSize`** into a container's first child (C1.1). Signature: the
  desync offset is *inside* the previous chunk's child region, and the "bad" id is actually a real child
  id read at the wrong place.
- **Off-by-twelve** — stepping `chunkSize + 12` (double-counting the inclusive header). Signature: every chunk overshoots by
  12; the desync is immediate and total.
- **An edit that grew a leaf without the ancestor fix-up** (C1.5). Signature: the walk is clean up to
  the edited subtree, then desyncs at the first sibling *after* the parent whose size is now short.
- **A file that is actually another format** — you skipped the magic test and a Bink or RCF is being
  read as Pure3D. Signature: desync at or near offset 12.

**Why this works.** The engine's loader runs the *same* walk (C1.8). So a file the retail game loads is,
by construction, a file your correct walker parses cleanly — which means a desync is always *your*
step, *your* edit, or *your* format confusion, never an inconsistency in a shipped file. That certainty
is what makes the diagnosis finite: there is exactly one first bad byte, and the method above finds it.

**What happens if you ignore it.** A desync that "mostly works" is the dangerous case: a tool that reads
90% of a file then quietly stops has silently dropped assets. Always assert that a full walk consumes
the file to `fileHeader.chunkSize` exactly; a walk that ends early is a walk that failed, even if it
didn't raise.
