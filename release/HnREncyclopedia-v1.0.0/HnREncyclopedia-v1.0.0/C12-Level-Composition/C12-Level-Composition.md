# Chapter 12 — Level Composition

> **Goal of this chapter:** understand how a whole playable level is assembled — terrain, streaming zones
> and road blocks, missions, teleport destinations, and ambient gags — from the files and the `level.mfk`
> that ties them together. After this chapter you can read how Springfield is built and streamed.

A SHAR level is not one file; it is a **composition**. The world is split into terrain, streaming **zone**
and **road** blocks, and a `level.mfk` that lists the missions, the fast-travel destinations, and the gags.
This chapter reads that composition from the retail data — the seven terrain files, the `b**.p3d` block set,
and the verified `scripts/missions/level01/level.mfk`.

**Key finding (✅ verified):** the world **streams by zones and roads**. `level.mfk`'s `AddTeleportDest`
entries name each Springfield location, its coordinates, *and the exact `.p3d` blocks to load there* — e.g.
`"Kwik E Mart", 209, 3.6, -285, "l1z2.p3d;l1r1.p3d;l1r2.p3d;"`. The naming is systematic:
`l{level}z{zone}.p3d` for zones, `l{level}r{road}.p3d` for roads.

---

## Deep-dive pages

- [C12.1 — The Seven Levels & Terrain](01-levels-terrain.md): the level roster, `L*_TERRA.p3d`, and `h2h`.
- [C12.2 — World Blocks & LODs (`b**.p3d`)](02-world-blocks.md): the block set and its detail variants.
- [C12.3 — Zones, Roads & Streaming](03-zones-streaming.md): the `l{level}z*`/`l{level}r*` residency system.
- [C12.4 — The `level.mfk`: Missions & Teleports](04-level-mfk.md): assembling a level's content.
- [C12.5 — Ambient Gags & Population](05-gags-population.md): the level's baked-in comedy and life.
- [C12.6 — Assembling a Level End-to-End](06-assembling.md): every piece, in load order.

---

## 12.1 The seven levels & terrain (✅ verified)

SHAR ships **seven story levels**, each with a terrain file — `L1_TERRA.p3d` … `L7_TERRA.p3d` (verified;
levels 2,3,5,6 lower-cased as `l2_TERRA.p3d` etc.) — plus a separate **`h2h`** (head-to-head/multiplayer)
tree and `level08`/`level09` mission dirs. Levels 1, 4, and 7 are the three "acts" set in the Simpsons'
neighbourhood, downtown, and the nuclear/rural edge; each level is a self-contained slice of Springfield.
[C12.1](01-levels-terrain.md).

## 12.2 World blocks & LODs (✅ verified)

The world geometry is split into **blocks** — `b00.p3d`, `b01.p3d`, … (11 base blocks) — each paired with a
`b0Ndata.p3d` companion, and some with **level-of-detail variants** (`b02l.p3d`, `b02m.p3d`, `b02s.p3d`,
`b02st.p3d` — large/medium/small/street). The block split is what makes streaming possible: the game loads
only the blocks near the player. [C12.2](02-world-blocks.md).

## 12.3 Zones, roads & streaming (✅ verified)

The finest-grained streaming unit is the **zone** (`l{level}z{n}.p3d`) and **road** (`l{level}r{n}.p3d`). Each
location in the world declares which zones and roads must be resident there. Verified from `level.mfk`:

```
AddTeleportDest("Simpsons' House", 220, 3.5, -172, "l1z1.p3d;l1r1.p3d;l1r7.p3d;");
AddTeleportDest("Kwik E Mart",     209, 3.6, -285, "l1z2.p3d;l1r1.p3d;l1r2.p3d;");
```

Fast-travelling to the Kwik-E-Mart loads zone `l1z2` and roads `l1r1`,`l1r2`. As you drive, the game streams
these in and out by proximity. [C12.3](03-zones-streaming.md).

## 12.4 The `level.mfk` (✅ verified)

The `level.mfk` assembles the level's *content*: its **missions** (`AddMission("m0")`…`AddMission("m7")`),
its **bonus missions** (`AddBonusMission("sr1"/"gr1"/"bm1")` — street races and bonus), its **teleport
destinations** (12 named Springfield locations), its **selectable vehicles** (`AddVehicleSelectInfo`), and
its **gags**. It is the level's table of contents. [C12.4](04-level-mfk.md).

## 12.5 Gags & population (✅ verified)

`level.mfk` also bakes in the level's ambient life: **39 gags** (the `GagBegin…GagEnd` blocks of C14.4),
`SuppressDriver` calls, and vehicle-select info. This is the comedy and traffic that make a level feel alive
before any mission starts. [C12.5](05-gags-population.md).

## 12.6 Assembling a level

Terrain + blocks + streamed zones/roads + `level.mfk` content (missions, teleports, gags) + the referenced
characters, cars, and props = a playable level. [C12.6](06-assembling.md) walks the whole assembly in load
order.

---

## Key takeaways

- A level is a **composition**, not a file: terrain (`L*_TERRA.p3d`), blocks (`b**.p3d` + LOD variants),
  streamed zones/roads, and a `level.mfk`.
- The world **streams by zone and road**: `AddTeleportDest` names each location's required
  `l{level}z*`/`l{level}r*` blocks (✅ verified).
- `level.mfk` assembles content: 8 missions + bonus missions, 12 teleport destinations, vehicle-select, and
  ~39 ambient gags per level.
- Seven story levels + an `h2h` multiplayer tree.

**Next:** [Chapter 13 — Paths, Fences & Road Data](../C13-Paths-Fences/C13-Paths-Fences.md) (already written).
