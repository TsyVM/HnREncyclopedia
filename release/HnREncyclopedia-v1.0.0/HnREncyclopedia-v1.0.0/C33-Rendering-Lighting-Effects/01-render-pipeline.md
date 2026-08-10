# C33.1 — The Render Pipeline

**What it is.** The machinery that turns the scene graph (C10) and the UI (C21) into the pixels on screen
each frame — a pipeline of **render layers** sequenced by a manager. It's the "backend" you never see but
that draws everything you do.

**How it works (✅ verified).** Rendering is layered and centrally managed:

```
RenderManager        — owns the pipeline
RenderFlow           — sequences the render passes each frame
WorldRenderLayer     — draws the 3-D world (the scene-graph walk, C10.6)
FrontEndRenderLayer  — draws the UI/HUD on top (the Scrooby pass, C21.4)
Fader                — screen fades (context transitions, C30)
```

Each frame, `RenderFlow` runs the layers in order: **`WorldRenderLayer`** draws the 3-D world — it walks the
scene graph (C10.6), applies transforms and culling, and draws each drawable with its shader (C6) and texture
(C5), in sort order (C10.5). Then **`FrontEndRenderLayer`** composites the UI/HUD on top — the Scrooby pages
(C21.4), the HUD (C26.1), the map (C29). **`Fader`** applies screen fades for transitions between contexts
(C30) — the fade-to-black when you enter a loading screen. `RenderManager` owns the whole stack.

**Why a layer pipeline.** Separating the world and the UI into distinct render layers is what lets them be
drawn with different rules: the world uses 3-D projection, depth testing, and lighting (C33.2); the UI uses
2-D screen coordinates and no depth (it's always on top). Drawing them as ordered layers — world first, UI
second — guarantees the HUD is always over the world, and lets each layer manage its own state. It also makes
transitions clean: `Fader` is just another layer that draws a fading black quad over everything. This is the
standard "layered compositor" render architecture, and it mirrors the game's overall layered design (world
entities, UI on top, C30).

**The frame's render step.** Rendering is the last step of the gameplay frame loop (C30.5): after input, AI,
missions, physics, and streaming update the world, `RenderManager` draws it. So the render pipeline consumes
the results of every other system — the physics-moved objects (C26), the AI-driven characters (C25), the
mission HUD state (C26.1) — and turns them into the frame. It's the sink at the end of the loop.

**Direct3D 8.** SHAR renders on **Direct3D 8** on PC (the shipped `pddidx8r.dll` is the D3D8 renderer, C28).
This dates the pipeline: fixed-function transform and lighting (C33.2), no programmable shaders in the modern
sense — the "shaders" (C6) are material/state descriptions fed to the fixed-function pipeline, not GPU
programs. This is why the lighting is the classic light-type family (C33.2) and the materials are render-state
parameters (C6.2): it's a fixed-function GPU of 2003.

**What happens if you bend it.**

- *Rely on a `RenderManager`/render-layer member offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Expect programmable shaders* — it's fixed-function D3D8 (C6). The "shaders" are state, not GPU programs.
- *Assume UI draws with the world's rules* — the UI is a separate layer with 2-D rules on top. Different
  layer, different state.
