# C33.2 — Lighting

**What it is.** How the world is lit — the `tLight` family of light types and the groups that organise them.
It's the fixed-function lighting of a Direct3D 8 engine (C33.1): a handful of light types combined per area.

**How it works (✅ verified).** The verified light hierarchy:

```
tLight (base)
  ├ tAmbientLight      — uniform ambient fill (the base illumination everywhere)
  ├ tDirectionalLight  — parallel rays (the "sun" — one direction, no falloff)
  ├ tPointLight        — an omni light at a position (falls off with distance)
  └ tSpotLight         — a cone light (position + direction + angle)
tLightGroup / Scenegraph::LightGroup   — a set of lights (per area/object)
tLightAnimationController              — animates a light's properties over time (C34)
tLightLoader / tLightGroupLoader       — load lights from Pure3D chunks
```

These are the four classic fixed-function light types. A scene is lit by combining them: an `tAmbientLight`
for the base fill, a `tDirectionalLight` for the sun, and `tPointLight`/`tSpotLight`s for local sources (a
lamp, a fire). Lights are organised into **groups** (`tLightGroup`) per area, so only the relevant lights
affect a given region — the lighting equivalent of the streaming zones (C12.3). The material's response to
these lights is the shader's `DIFF`/`AMBI`/`SPEC` colours and `SHIN` (C6.3–C6.4) — the lights provide the
illumination, the materials define the reflectance.

**Why grouped, fixed-function lights.** On 2003 hardware, lighting is computed per-vertex by the fixed-
function pipeline (C33.1), and the GPU handles a limited number of active lights at once. Grouping lights by
area (`tLightGroup`) keeps the active set small — only the lights near the object being drawn are enabled —
which is both a performance necessity and a correctness one (you don't want a lamp in another zone lighting
you). This is the same "only what's near matters" locality as collision broad-phase (C11.2) and streaming
(C12.3): the world is divided, and only the local subset is active. The light types themselves (ambient/
directional/point/spot) are the D3D8 standard, so SHAR uses them directly.

**Animated lights.** `tLightAnimationController` animates a light over time — a flickering fire, a pulsing
sign, a light that dims. It's an animation *controller* (C34) driving the light's properties (colour,
intensity) through the channel system (C34). This is how the world has *dynamic* lighting despite fixed-
function rendering: the light values change per frame via channels, even though the lighting *model* is
static. So a flickering light is a `tPointLight` whose colour channel (C34) is animated by a
`tLightAnimationController`.

**The tie to materials and shadows.** Lighting is one half of a surface's look; the material (C6) is the
other. A surface's final colour is its material's reflectance (C6.4) times the lights hitting it (here), plus
its emissive (C6.4) and specular (C6.3). Shadows are separate and cheap — the blob shadows under cars
(`SetShadowAdjustments`, C15.6) are projected quads, not shadow-mapped, fitting the fixed-function era. So
"lighting and shadows" in SHAR is: fixed-function vertex lighting from the `tLight` family, plus blob shadows
as art.

**What happens if you bend it.**

- *Rely on a `tLight` member offset* — classes/vtables ✅, offsets ⏳. Diff (C4.3).
- *Add many lights to one area* — the fixed-function pipeline has a limited active-light budget; grouping
  (`tLightGroup`) exists to respect it. Keep the local set small.
- *Expect real-time shadows from lights* — shadows are separate blob quads (C15.6), not light-cast. Different
  system.
