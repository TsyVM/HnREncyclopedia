# C10.1 — The Scenegraph & its Root (`0x03F00000` / `0x03F00001`)

**What it is.** The top of the world hierarchy: a named Scenegraph chunk and the Root/Branch that begins its
node tree. Everything a level draws hangs beneath here.

**How it works (✅ verified).** Decoded from `art/b00 - Copy.p3d`:

```
0x03F00000 Scenegraph   name="t2_bonus164Shape_001"   (own: pstr name + fields)
0x03F00001 Root/Branch  name="t2_bonus116Shape"       (own: pstr name + fields)
```

Both are **named**, both are containers (their `headerSize < chunkSize`, C1.2), and both are ordinary
Pure3D chunks — you walk into them with the same recursive walker as any other subtree (C1.3). The
Scenegraph names the whole graph; the Root begins the tree of transform and drawable nodes beneath it. The
`…Shape` / `…Shape_001` names are Maya export names (C7.1), so a node traces back to a source object.

**Why a named graph.** Naming the graph and its root lets the level (C12) and scripts (C14) reference a
whole sub-tree by name — "place the graph `t2_bonus164Shape_001` here" — rather than by offset. It also
makes the tree self-documenting: a dump of a level's scene graph reads as a list of recognisable object
names, which is how you orient yourself in an unfamiliar `.p3d` (the C4.2 dump-first workflow).

**Relationship to the mesh.** A scene-graph node named `…Shape` is not the mesh itself — it is the *placement*
of a drawable that *is* the mesh (C10.4). The same mesh can appear under many nodes; the graph is the "where
and how many," the mesh chunk is the "what." Keeping them separate is what lets one crate model become fifty
crates in a level with fifty lightweight transform nodes and one heavy mesh.

**What happens if you bend it.**

- *Rename a node but not its script references* — a level or mission that places the graph by name (C14) no
  longer finds it. Rename both ends.
- *Treat the node as owning the geometry* — it references it (C10.4); editing the node's transform moves the
  instance, editing the mesh changes every instance. Know which you're editing.
- *Break the container/leaf sizes when editing* — the graph is a chunk subtree; the C1.5 size discipline
  applies. Re-emit with the size-computing writer.
