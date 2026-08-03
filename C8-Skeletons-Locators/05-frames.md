# C8.5 — Frames & the Locator Hierarchy (`0x07010001`)

**What it is.** A transform hierarchy separate from the scene graph: a tree of **frames** that cameras,
effects, attachments, and moving parts hang on. Where the scene graph (C10) arranges *drawables*, frames
arrange *reference points* that things attach to.

**How it works (✅ verified).** `0x07010001` is a **Frame** node that nests child frames. Decoded from
`art/b00 - Copy.p3d`: one frame node contains **36 child frames** plus a `0x07010006` data chunk — a genuine
hierarchy. The associated `0x07010007` frame-data leaf is one of the most common chunks in the game (**48,968
instances**), which tells you frames are everywhere: nearly every attachable point in every asset is a frame.

Each frame is a named transform — a coordinate space you can attach something to. A weapon attaches to a
hand frame; a camera tracks a target frame; an effect emits from an effect frame; a car's wheels are frames
its wheel meshes follow. The frame tree composes transforms exactly like the scene graph (C10.3): a child
frame's world position is its local transform composed with its parents'.

**Why frames are separate from the scene graph.** The scene graph exists to *draw* the world; frames exist to
*attach* to it. Keeping them separate means you can have an attachment point (a frame) that isn't itself a
drawable, and you can move an attached thing by moving its frame without touching the render tree. It also
matches how the animation system thinks: the skeleton (C8.1) is a frame hierarchy (joints are frames), so
animating joints and attaching props to them use one mechanism. Frames are, in effect, the engine's general
"named coordinate space" primitive, of which skeleton joints and attachment points are special cases.

**The relationship to locators.** A locator (C8.4) is a *place*; a frame is a *coordinate space*. They
overlap — both are named reference points — but a frame can have children and carries a full transform,
while a locator is typically a leaf marker. In practice: locators mark *gameplay* places (spawn, trigger),
frames provide *attachment/animation* spaces (joints, camera targets, wheel mounts). Both are how non-drawn
structure is baked into assets for other systems to reference by name.

**At runtime.** Frames become the transform nodes the animation and attachment systems drive. A camera
following a character reads the character's target frame each frame; a wheel mesh reads its wheel frame. The
runtime classes are part of the Pure3D/DSG object model (names ✅ from RTTI where present, offsets ⏳). The
sheer count of frame data (48,968) reflects that almost everything animated or attached in the game resolves
through a frame.

**What happens if you bend it.**

- *Attach to a frame that isn't in the loaded asset* — the attachment has no space to sit in and appears at
  the origin or not at all. Ensure the frame exists.
- *Confuse a frame with a scene-graph node* — editing a frame moves attachments, not drawables (and vice
  versa). Know which hierarchy you're in.
- *Break the frame tree's transforms* — attachments and cameras jump. Frames compose like scene-graph
  transforms (C10.3); keep the chain intact.

**Next:** [Chapter 13 — Paths, Fences & Road Data](../C13-Paths-Fences/C13-Paths-Fences.md).
