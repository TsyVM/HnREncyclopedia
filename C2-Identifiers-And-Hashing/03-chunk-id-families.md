# C2.3 — Chunk-ID Families

**What it is.** The observation that Pure3D chunk ids are *organised*: the high bits sort them into
subsystem families, so the top half of an id tells you which chapter to open before you decode anything.
This is read directly off the verified census, so the families are ✅; the family *names* are 🟡.

**How it works.** Grouping the 179 observed ids by their high bytes yields a small number of clusters,
and every cluster maps cleanly to one subsystem:

| Family prefix | Subsystem | Representative ids (occurrences) | Chapter |
|---|---|---|---|
| `0x0001xxxx` | Shaders / textures / meshes | `0x00011003` (224,971), `0x00010000` shader (14,825), `0x00019000` texture (10,312) | C5–C7 |
| `0x0012xxxx` | Collision & intersect | `0x00121110` (147,655), `0x00121100` (67,434), `0x00121001` (46,316) | C11 |
| `0x03F0xxxx` | Scene graph | `0x03F00007` (10,311), `0x03F00003` (8,755), `0x03F00005` drawable | C10 |
| `0x0300xxxx` | Paths & fences | `0x03000009` (6,544), `0x03000005`, `0x0300000B` | C13 |
| `0x0701xxxx` | Locators / frames | `0x07010007` (48,968), `0x07010001` (15,577) | C8 |
| `0x0000xxxx` | Animation & controllers | `0x00004500` family, `0x00002200` | C8 |

The occurrence counts are exact and reproducible (they come straight from the parser over all 1,941
files). They also *rank the game by mass*: the single most common chunk in the entire game is
`0x00011003` (a **shader integer parameter** — a FourCC tag plus an int; decoded and verified in C6,
224,971 instances), and the second is `0x00121110` (a collision vector list, 147,655) — telling you,
before any art is opened, that this is a world of heavily-parameterised materials over dense collision.
(Note: this `0x0001**1**xxx` family is the **shader** family; the geometry lives in the neighbouring
`0x0001**0**xxx` family — `0x00010000` Mesh, `0x00010005` positions, `0x0001000A` indices — a
distinction the byte-level decode in C6–C7 makes exact, and a good example of why names carry
confidence markers.)

**Why it's built this way.** A structured id space lets the loader's dispatch table be compact and lets
whole subsystems be reasoned about together. It also means a tool can make a safe *coarse* decision — "is
this a collision chunk?" — from a mask (`(id & 0xFFFF0000) == 0x00120000`) without a full table, which is
handy when triaging an unknown file.

**How to use it.** When [the universal dumper](../C1-Pure3D-Container-Model/06-universal-opener.md) prints
a tree, glance at the dominant prefix:

- Mostly `0x0001xxxx` → an art asset (texture atlas, model). Open C5–C7.
- Mostly `0x0012xxxx` → collision data. Open C11.
- Mostly `0x03F0xxxx` → a scene graph assembling other drawables. Open C10.
- A spread with `0x0300xxxx` and `0x0701xxxx` → a level/world file with paths and locators. Open C10–C13.

**What happens if you bend it.** The families are a *guide*, not a law — role (container/leaf) is still
decided per instance by the size comparison (C1.2), and a few ids appear across contexts. Use the family
to pick a starting chapter, then confirm by decoding the actual chunk. Never assume a family prefix
implies a fixed payload layout; the payload is defined per id, in its chapter.
