# C2.2 — The Radical String Hash

**What it is.** The 32-bit string hash Radical uses for asset-name references and RCF directory keys —
the function `radLoadObject` effectively keys on. This page gives a portable implementation and states
plainly what is proven and what is reasoned.

**Confidence up front.** That RCF keys and Pure3D name references *are* 32-bit hashes is ✅ **Verified**
(the RCF directory is `{hash, offset, size}` with no strings — C3 — and Pure3D references are `uint32`).
The *exact algorithm and string normalisation* below is 🟡 **Reasoned**: it matches the DonutsSDK
`hashing` module and is consistent with the observed RCF keys, but because the shipped directories store
only hashes (no source paths), it is not proven byte-for-byte against a shipped name list in this data
set. Treat it as the best-supported reconstruction, and always confirm a specific key by round-tripping a
name you *do* know from the scripts.

**Normalisation (part of the hash).** Before hashing a path, the engine works on a canonical form:
lower-cased, with path separators normalised (Windows `\`). Two strings that differ only in case or slash
direction must hash the same, or the archive lookups the game itself performs would fail — so
normalisation is not optional decoration, it is part of the key.

**The algorithm (🟡 reasoned).** A per-character multiply-accumulate over the normalised bytes — the
classic Radical form:

```python
def radical_hash(name: str) -> int:
    h = 0
    for ch in name.lower().replace('/', '\\'):
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF     # 32-bit multiply-add
    return h
```

The multiplier and the exact seed are the parts to pin against a known key; the *shape* — accumulate,
multiply by a small constant, add the byte, keep 32 bits — is the reliable structure. The DonutsSDK
ships this as a `constexpr` so a mod can compute keys at compile time; this Python mirror is for tooling
and verification.

**How to confirm it on your own copy.** The scripts give you ground truth for free. Take a path you can
read in an `.mfk` — say the compiled-script name that `scripts.rcf` must contain — normalise it, hash it,
and check the result against the 125 keys in the directory (C3). When your implementation reproduces the
real keys for names you know, you can trust it for names you are trying to recover.

**Why a small odd multiplier.** A multiply-add with an odd constant (31 is the textbook choice) spreads
input bits across the full 32-bit range and avoids the clustering a pure sum or shift would give for the
short, similar strings asset names tend to be (`m1i`, `m1l`, `m2i`…). Good spread is what keeps the
directory's hash keys collision-free enough to be a plain sorted array.

**What happens if you bend it.**

- *Skip normalisation* (hash `"Art\Cars\Ambul.CON"` verbatim) and you get a different number than the
  engine stored; the lookup misses. Lower-case and slash-normalise first, every time.
- *Use the wrong multiplier/seed* and every key is wrong; the give-away is that *no* known name
  round-trips. Fix it against one known key and they all fall into line.
- *Assume no collisions* on an open name set and you may map two different names to one key. Within the
  retail directories the keys are distinct (a sorted array works), but for recovered dictionaries always
  keep the source string, not just the hash — see [C2.4](04-collisions-and-recovery.md).
