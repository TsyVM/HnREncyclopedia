# C10.2 — Branches & Nodes (`0x03F00002`)

**What it is.** The interior of the scene-graph tree: branch nodes that group children, letting the graph
fan out from its root into the many placements a level needs.

**How it works.** A branch (`0x03F00002`) is a container whose children are further nodes — more branches,
transforms (C10.3), and drawables (C10.4). The tree shape mirrors the world's logical grouping: a building
node contains its wall nodes, each wall node contains its window drawables, and so on. Walking is the
universal recursion (C1.3): descend every container, and the ids tell you what each node does (branch vs.
transform vs. drawable).

**Why a tree of branches.** Grouping is what makes transforms and culling efficient. A transform on a parent
branch applies to its whole subtree — move the building node and every wall moves with it — so shared motion
costs one matrix, not one per part. Culling works the same way: if a branch's bounds are off-screen, the
whole subtree is skipped in one test (the broad-phase idea, shared with collision, C11.2). The branch
structure is therefore not decoration; it is what lets a large world draw and update cheaply.

**Reading structure from the tree.** The *shape* of the branch tree tells you how a level is organised
before you decode a single transform: a wide, shallow tree is a flat scattering of props; a deep tree is a
nested, articulated object (a vehicle, a machine). The C4.2 dump, showing indentation, makes this visible at
a glance.

**What happens if you bend it.**

- *Re-parent a node to the wrong branch* — it inherits the wrong transform and jumps to the wrong place.
  Parenting is spatial; keep nodes under the branch whose transform they should follow.
- *Flatten the tree* — you lose grouped transforms and grouped culling, making the graph slower to update
  and draw. Preserve meaningful grouping.
- *Create a cycle* (a node that is its own ancestor) — the walk never terminates. Scene graphs are trees;
  keep them acyclic (and cap recursion depth defensively, C1.3).
