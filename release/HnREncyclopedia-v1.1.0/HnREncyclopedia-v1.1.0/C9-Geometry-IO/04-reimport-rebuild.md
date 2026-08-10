# C9.4 — Re-Importing & Rebuilding

**What it is.** The hard direction: taking edited geometry from a tool back into a Pure3D file the game loads.
It's a rebuild, governed by the size-tree discipline (C1.5), because changing geometry changes stream lengths
and every ancestor size.

**How it works.** Read the edited OBJ/glTF into the neutral model (C9.1), converting axes back to engine
space (C9.2), then rebuild the Pure3D geometry:

1. **Rebuild the streams.** Write new position (`0x00010005`), UV (`0x00010007`), colour (`0x00010008`), and
   index (`0x0001000A`) chunks from the neutral model, each count-prefixed (C7.3–C7.4). Convert the triangle
   list back to a strip if the group uses strips (C7.2/C7.4).
2. **Update the counts.** Set the primitive group's `vertexCount`/`indexCount` (C7.2) and the mesh-level
   counts (C7.1) to match the new geometry. These *must* agree with the stream lengths.
3. **Re-bind the shader.** Keep the shader name (C9.1) in the primitive group (C7.2) so the material still
   binds (C6.5).
4. **Run the ancestor size fix-up (C1.5).** Every changed chunk's `chunkSize` propagates up: stream → group →
   mesh → … → the file header. Use the tree-parse → edit → re-emit-bottom-up flow (C4.1) so the writer
   recomputes every size and none is left stale.

Step 4 is the whole difficulty. Because Pure3D sizes are inclusive and nested (C1.2), changing a vertex count
resizes a stream, which resizes its group, its mesh, and every ancestor. Hand-patching those sizes is where
imports break; re-emitting the tree bottom-up (C4.1) makes it impossible to leave a stale size.

**Why rebuild, not patch.** For a length-preserving edit (moving a vertex, recolouring — same counts) you
*could* patch bytes in place (C1.5). But any edit that changes vertex or triangle count changes lengths, and
then in-place patching means hand-maintaining the size tree — error-prone. Parsing to a tree, swapping the
geometry, and re-serializing bottom-up is the robust path: it handles both cases and can't desync. Reserve
in-place patching for strictly same-count tweaks.

**Skinned re-import.** Re-importing a skinned character (C8) adds a step: the skin data (`0x00017001`, C8.3)
maps vertices to joints, so if you changed the vertex count you must rebuild the weights to match — the same
per-vertex consistency as the streams (C7.3). glTF carries the weights (C9.3), so a glTF round-trip preserves
them; the re-import writes them back into the skin chunk. Editing a skinned mesh's *shape* without touching
its *vertex count* is far safer — it keeps the weights valid.

**What happens if you bend it.**

- *Change vertex count but not the counts/sizes* — the loader reads the wrong number of elements or desyncs
  (C7.2, C1.7). Update every count and run the fix-up.
- *Forget to convert axes back* — the re-imported mesh is mirrored/rotated (C9.2). Convert at the boundary.
- *Break skin-weight/vertex correspondence* — the character deforms into spikes (C8.3). Keep weights in step
  with vertices, or don't change the count.
