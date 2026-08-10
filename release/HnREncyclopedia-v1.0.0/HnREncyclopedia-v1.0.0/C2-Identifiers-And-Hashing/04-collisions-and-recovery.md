# C2.4 — Collisions & Name Recovery

**What it is.** The practical task created by C2.1: shipped assets reference each other, and the archives
address their members, by hash — so to work with names a human recognises you must **recover** them from
hashes. This page is the workflow, ordered by yield.

**The core asymmetry that makes it possible.** Hashing is one-way, but the game ships a huge crib sheet:
the **plain-text scripts keep every string**. Across 344 `.mfk`, 255 `.con`, and 9 `.cho` files there
are thousands of real paths and object names in the clear. Recovery is therefore mostly *dictionary
building*, not cryptanalysis.

**Step 1 — Mine the scripts for names (highest yield).** Extract every quoted path and identifier from
the text scripts:

```python
import re, glob
names = set()
for path in glob.glob('scripts/**/*.mfk', recursive=True) + glob.glob('scripts/**/*.con', recursive=True):
    text = open(path, 'r', errors='ignore').read()
    names |= set(re.findall(r'"([^"]+)"', text))     # quoted paths/names
    names |= set(re.findall(r'\b([A-Za-z_]\w{2,})\b', text))  # bare identifiers
```

This alone yields the level, mission, car, and prop names — the bulk of what you want.

**Step 2 — Hash the dictionary forward and match.** For each known name, compute `radical_hash(name)`
(C2.2) and index it. Now any unknown hash — an RCF key, a Pure3D asset reference — is a dictionary
lookup:

```python
from_hash = { radical_hash(n): n for n in names }        # forward index
def resolve(h): return from_hash.get(h, f"0x{h:08X}")     # name or hex fallback
```

Point this at the 125 keys of `scripts.rcf` (C3) and the entries that correspond to script paths you
mined will resolve to real names; the rest tell you exactly which names you are still missing.

**Step 3 — Brute force the short residue (lowest yield, last resort).** For hashes still unresolved,
enumerate short strings over the plausible alphabet (`a–z0–9_`, plus known prefixes like `art\` and
`m1`, `m2`) and hash them. Because asset names are short and follow visible conventions (`m1i`, `m1l`,
`m1sdi`…), a targeted search over those patterns recovers far more than a blind one. Keep the search
seeded from the naming patterns you already see in the scripts.

**Collisions — why you keep the string, not just the hash.** The Radical hash is 32-bit; over a large
open name set, two different names *can* map to one value. Inside the retail directories the keys happen
to be distinct (which is why a sorted array suffices — C3), but a *recovered dictionary* you build
yourself can contain collisions. The rule: your recovery table maps hash → **set of candidate names**,
and you disambiguate by context (which name makes sense for a car vs. a texture). Never discard the
source string in favour of its hash; the string is the only thing that survives a collision.

**Why recovery is worth it.** A resolved name turns a byte dump into a readable asset graph: instead of
"chunk references `0x1A2B3C4D`," you see "shader references texture `homer_body`." Every later chapter is
easier to write and to *use* when the references carry names, which is exactly why the scripts (which
keep their names) are documented early, in Chapters 14–17.

**What happens if you bend it.** Trusting a single brute-forced name without confirming it against a
known-good round-trip can seed your whole map with a plausible-but-wrong string. Always validate a
recovered name by re-hashing it and checking it reproduces the exact key, and prefer names mined from
scripts (ground truth) over names guessed by search.
