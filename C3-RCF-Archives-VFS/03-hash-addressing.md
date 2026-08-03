# C3.3 — Hash Addressing: Files Without Names

**What it is.** The defining choice of the RCF format: members are keyed by the **Radical hash of their
path**, and the path string itself is not stored. The directory is `{hash, offset, size}` and nothing
more (C3.2, ✅ verified).

**How it works.** At build time each member's path — `scripts\cars\ambul.con`, normalised to lower case
with backslashes — is run through the Radical hash (C2.2) to produce the 32-bit key. Members are sorted
by that key and written. At load time the engine does the same hash on the requested path and binary
-searches for it. The string exists only in the *build inputs* and in the *code/scripts that request
files*; it never reaches the shipped directory.

**Why it's built this way.** It is the logical extension of the whole "names as numbers" philosophy
(C2.1) to the archive layer: fixed-width keys, a contiguous sorted array, O(log n) lookup, and a smaller
file with no string heap. For a game that resolves asset requests constantly, hashing the path once and
comparing integers is materially cheaper than string matching, and it removes any dependency on string
encoding or case handling at lookup time — the hash already folded those in.

**What it means for you.** Two concrete consequences:

1. **Extraction by name requires the name.** You cannot list an RCF's contents as human paths from the
   archive alone — the paths aren't there. You can list the *hashes*, sizes, and offsets, and you can
   extract every member as an anonymous blob, but to name them you must supply or recover the paths
   (C2.4). The good news, again, is that the scripts are full of the real paths: hash every path you find
   in the `.mfk`/`.con` files and match them against the directory keys to name most members.
2. **The member's *own* content often re-identifies it.** Even anonymous, a member usually announces its
   type by its first bytes — a packed `.p3d` still starts `P3D\xff`, a packed sound still starts `RSD4`.
   So you can classify extracted blobs by magic (the [identifier](../Glossary/extensions.md#a-portable-identifier))
   even before you recover their names. In `scripts.rcf` the members begin with a small common tag,
   consistent with a compiled-script container.

**A worked recovery.** To confirm your hasher and name a member at once: take a script path you can read,
`scripts\missions\level01\m1l.mfk`, normalise and hash it, and search the 125 keys. A hit both names that
member and proves your implementation of C2.2 against ground truth. Do this for the handful of names you
know and you bootstrap a dictionary for the rest.

**What happens if you bend it.**

- *Request a path with the wrong normalisation* (case or slashes) and the hash misses even though the
  file is present. Normalise exactly as the engine does before hashing.
- *Assume you can rename a member by editing the directory* — the key is derived from the path, so a
  "rename" means recomputing the hash for the new path *and* ensuring every requester uses that new path.
  There is no name to edit, only a key to recompute.
- *Expect two members to share a key* — within a shipped archive the keys are distinct (sorted, unique).
  If you build an archive and two paths collide, one shadows the other; keep the source paths and check
  for collisions at pack time.
