# C11.1 — The Collision Object (`0x00121000`)

**What it is.** The root of one thing's collision: a named container that holds the volume tree and a
bounding box. It is the collision counterpart to a Mesh (C7) — the same object has a mesh you *see* and a
collision object you *touch*, matched by name.

**How it works (✅ verified).** The `0x00121000` own data, decoded from `art/b00 - Copy.p3d`:

```
00 00 00 00                       (index / flags)
10  "BQG_flareShape\0\0"           pstr, length 16 (null-padded, C6): the object name
42 51 47 …                         "BQG" tag + float extents
```

The name is the hook: `BQG_flareShape` pairs with the drawable `…flareShape` (C7), so the engine knows
which collision belongs to which visible object. The `BQG` tag and following floats are the object-level
bounds (🟡 — decoded as a tag + floats). Its two children are:

- **`0x00121002`** — the bounding volume container (the tree of C11.2), often large.
- **`0x00121004`** — a bbox/count leaf: verified `01, 0x864, 0x890, 0x864, 0x864` — counts and extents that
  let the broad-phase size the object before descending.

**Why it's built this way.** Separating collision from the mesh means the two can differ: collision is
usually *simpler* than the visible geometry (a crate is a box to touch but a detailed model to look at),
which is both faster to test and more forgiving to play against. Naming both halves the same lets the level
data reference one name and get both. Keeping a top-level bbox on the object is the first rejection test —
if the player isn't near the object's box, no volume inside it is tested at all.

**What happens if you bend it.**

- *Rename the collision but not the mesh (or vice versa)* — the engine can't pair them and the object
  becomes visible-but-non-solid, or solid-but-invisible. Rename both together.
- *Shrink the top-level bbox below the volumes it contains* — the broad-phase rejects the object before
  testing volumes that actually stick out, and the player clips through. Keep the object bbox enclosing all
  its volumes.
- *Assume collision matches the mesh triangle-for-triangle* — it usually doesn't; collision is its own,
  simpler geometry. Read the volume tree (C11.2), not the mesh, to know what's solid.
