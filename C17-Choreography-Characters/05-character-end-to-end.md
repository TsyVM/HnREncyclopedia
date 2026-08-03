# C17.5 — A Character End-to-End

**What it is.** The whole character, assembled — every layer from the model on disk to the live, animated,
AI-driven, choreographed person on screen. This page ties together C7, C8, C17, and C25 into one picture, the
character counterpart to the "a level end-to-end" synthesis (C12.6).

**The full stack (✅ verified layers).** A character is built from, bottom to top:

1. **Model** (C7) — the body geometry: meshes, textured (C5) and shaded (C6). On disk as the character's
   `.p3d` (`art/chars/*.p3d`).
2. **Skeleton** (C8.1) — the joint hierarchy inside the `.p3d`, the bones the body deforms with.
3. **Skin** (C8.3, `0x00017002`) — binds the mesh vertices to the skeleton so the body deforms as joints
   move.
4. **`.cho` rig** (C8.1) — the choreography rig: joint roles, IK legs, balance — the operating instructions
   for the skeleton. Loaded into a `choreo::Rig`/`RigLeg` (C17.1).
5. **Animation states → clips** (C8.2) — the `.cho` map from behaviour states to animation clips, played from
   `choreo::Bank`s (C17.2).
6. **`choreo::` engine** (C17.1–C17.3) — poses the `choreo::Puppet` each frame: selects clips, blends them,
   runs transitions, partitions the body, and solves foot IK.
7. **`CharacterAi`** (C25.2) — the state machine (`Loco`/`InCar`/`InSim`/…) deciding *what* the character
   does, which requests animation states (5) from the engine (6).
8. **Controller** (C25.3) — who drives it: the player (`CameraRelativeCharacterController`) or AI.
9. **`Character`** (C25.1) — the physical scene entity (DSG/physics, C23.2) all of the above hangs on — drawn
   (C10), solid (C11), simulated (C26).

**How a single motion flows through the stack.** When the player walks: the **controller** (8) feeds input to
the **`CharacterAi`** (7), which is in the `Loco` state and requests a walk **animation state** (5); the
**`choreo::` engine** (6) selects the walk clip from a **bank** (2 via C17.2), blends it with any upper-body
action (**partition**, C17.3), solves **foot IK** (C17.3) against the ground, and poses the **`choreo::Rig`**
(4); the **skin** (3) deforms the **mesh** (1) to that pose; and the **`Character`** entity (9) is drawn
(C10) at its physics-simulated (C26) position. Nine layers, one step of walking — each layer a chapter of
this book.

**Why so many layers.** Each layer is one concern, cleanly separated: geometry (what it looks like), skeleton
(its bones), skin (how bones deform it), rig (how to drive the bones), states (what motions exist), engine
(how to play/blend them), AI (what to do), controller (who decides), entity (where it is and that it's
solid). This separation is why SHAR characters are so flexible — swap the mesh (reskin), swap the `.cho`
(re-rig), add a costume (new state set, C8.2), change the AI, and the rest keeps working. It's the same
layered, reference-based design as the whole engine, applied to the most complex asset in the game.

**The whole-book view.** A character touches nearly every chapter: textures (C5), shaders (C6), meshes (C7),
skeletons/skin/locators (C8), the scene graph (C10), collision (C11), choreography (C17), the runtime
`Character`/AI (C25), physics (C26), sound (C19), and missions (they're who you `talkto`, C16). To assemble a
character is to use the whole engine — which is why this chapter, closing the character arc, is also a
recapitulation of the book.

**What happens if you bend it.**

- *Edit one layer and forget its neighbours* — a new mesh (1) may need new skin weights (3) if the vertex
  count changed (C8.3); a new `.cho` (4) needs matching skeleton joint names (2). Trace the stack.
- *Rely on a character-layer member offset* — classes ✅ across the stack, offsets ⏳. Diff (C4.3).
- *Assume the layers are one object* — they're separable by design. Edit the layer that owns the concern you
  want to change.

**Next:** [Chapter 18 — RSD Sound Format](../C18-RSD-Sound/C18-RSD-Sound.md).
