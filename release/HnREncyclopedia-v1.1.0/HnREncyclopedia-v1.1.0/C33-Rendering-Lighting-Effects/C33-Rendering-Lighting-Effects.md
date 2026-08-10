# Chapter 33 — Rendering, Lighting, Sky & Effects

> **Goal of this chapter:** decode the "backend" visual systems you see but rarely think about — the render
> pipeline that draws each frame, the lighting that lights the world, the sky (which is *art*, not code), and
> the particles, sprites, and effects that make the world sparkle, smoke, and explode.

Beneath the assets (Part II) and the scene graph (C10) is the machinery that turns them into pixels each
frame: the **render pipeline**, the **lighting** system, and the **effects** (particles, sprites,
billboards). This chapter decodes them from the verified RTTI set (with confirmed vtable addresses) — and
establishes an honest negative finding: **there is no sky/atmosphere code system; the sky is geometry and
textures.**

**Key finding (✅ verified):** rendering runs through `RenderManager`/`RenderFlow` and stacked **render
layers**; lighting is the `tLight` family (`tAmbientLight`, `tDirectionalLight`, `tPointLight`, `tSpotLight`,
`tLightGroup`); effects are a full **particle system** (`tParticleSystem`, `tBaseEmitter`, `tSpriteEmitter`,
`ParticleSystemDSG`) plus **billboards/sprites** (`tBillboardQuad`, `tSprite`). The **sky is art** — cloud
and sun *textures* (`l7_backcloud.bmp`, `cloud1_alpha.bmp`, `sun2.bmp`) on skydome geometry, with **no**
dedicated atmosphere class.

---

## Deep-dive pages

- [C33.1 — The Render Pipeline](01-render-pipeline.md): `RenderManager`, `RenderFlow`, and the render layers.
- [C33.2 — Lighting](02-lighting.md): the `tLight` family and light groups.
- [C33.3 — Sky & Atmosphere: It's Art](03-sky-atmosphere.md): the skydome, cloud textures, and the missing code system.
- [C33.4 — Particles & Emitters](04-particles.md): `tParticleSystem`, emitters, `ParticleSystemDSG`.
- [C33.5 — Sprites, Billboards & Effects](05-sprites-effects.md): `tBillboardQuad`, `tSprite`, `tEffectController`, `RumbleEffect`.

---

## 33.1 The render pipeline (✅ verified)

Each frame is drawn through a pipeline of **render layers**, managed centrally:

```
RenderManager        — owns the render pipeline
RenderFlow           — sequences the render passes
WorldRenderLayer     — the 3-D world (scene graph, C10)
FrontEndRenderLayer  — the UI/HUD on top (Scrooby, C21)
Fader                — screen fades (transitions between contexts, C30)
```

The world draws first (`WorldRenderLayer` — the scene-graph walk, C10.6), then the UI composites on top
(`FrontEndRenderLayer` — the Scrooby pass, C21.4), with `Fader` handling fades between game states (C30).
`RenderManager`/`RenderFlow` sequence it all. [C33.1](01-render-pipeline.md).

## 33.2 Lighting (✅ verified)

The world is lit by the `tLight` family — the standard fixed-function light types (SHAR renders on Direct3D
8, C28):

```
tLight (base)
  ├ tAmbientLight      — uniform fill light
  ├ tDirectionalLight  — the "sun" (parallel rays)
  ├ tPointLight        — a local omni light
  └ tSpotLight         — a cone light
tLightGroup            — a set of lights (per area)
tLightAnimationController — animates a light over time (C34)
```

Lights are grouped (`tLightGroup`, `Scenegraph::LightGroup`) per area and can be animated (a flickering light
via `tLightAnimationController`, driven by channels, C34). [C33.2](02-lighting.md).

## 33.3 Sky & atmosphere: it's art (✅ verified negative)

There is **no sky, cloud, fog, or atmosphere class** in the RTTI (a sweep finds zero). The sky is **art**:
a **skydome** mesh (C7) textured with sky/cloud/sun *textures* — verified in the texture index:
`l7_backcloud.bmp`, `l3_Cloudmove.bmp` (an animated, scrolling cloud layer), `cloud1_alpha.bmp`,
`cloud_smokealpha.bmp`, `sun2.bmp`, `bluestarglow.bmp`. Fog is a Direct3D render-state setting, not a class.
So "the atmosphere" is made by artists, not an engine subsystem. [C33.3](03-sky-atmosphere.md).

## 33.4 Particles & emitters (✅ verified)

Sparks, smoke, fire, and dust are a full **particle system**:

```
tParticleSystem / tParticleSystemFactory     — a particle effect and its template
tParticleArray / tParticlePool               — the live particles
tBaseEmitter / tSpriteEmitter                — spawn particles (sprite-based)
tSpriteParticle                              — one billboard particle
ParticleSystemDSG / InstParticleSystemLoader — particle systems in the scene graph (C10)
```

Particle textures are set from scripts (`SetParticleTexture`, C14.6). A particle system is a scene-graph
entity (`ParticleSystemDSG`) that emits `tSpriteParticle`s. [C33.4](04-particles.md).

## 33.5 Sprites, billboards & effects (✅ verified)

**Billboards** (camera-facing quads) and **sprites** render 2-D-in-3-D — coins, glows, particles:

```
tBillboardQuad / tBillboardQuadGroup / tBillboardQuadGroupAnimationController
tSprite / tSpriteLoader / FeSprite / Scrooby::Sprite
tEffectController / tOpticEffect / ConstantEffect     — effect drivers
RumbleEffect / WheelRumble                            — controller force-feedback (rumble!)
```

Billboards always face the camera (a glow, a coin); `RumbleEffect` even drives the controller's rumble motor
— an "effect" that isn't visual. [C33.5](05-sprites-effects.md).

---

## Key takeaways

- Rendering is a **layer pipeline** (`RenderManager`/`RenderFlow`): `WorldRenderLayer` (3-D) then
  `FrontEndRenderLayer` (UI), with `Fader` for transitions.
- Lighting is the **`tLight` family** (ambient/directional/point/spot) in **light groups**, optionally
  animated (C34).
- **The sky is art, not code** — a skydome mesh + cloud/sun textures (verified: `l7_backcloud`, `Cloudmove`,
  `sun2`); no atmosphere class. Fog is a D3D render state.
- **Effects** are a full particle system (`tParticleSystem`/emitters/`ParticleSystemDSG`) plus
  **billboards/sprites** (`tBillboardQuad`/`tSprite`), and even **rumble** (`RumbleEffect`).
- All classes ✅ verified with ✅ vtable addresses; member offsets ⏳.

**Next:** [Chapter 34 — Animation Channels & Controllers](../C34-Animation-Channels/C34-Animation-Channels.md).
