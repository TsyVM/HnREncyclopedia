# Chapter 43 — Time of Day, Lighting & Shadows

> **Goal of this chapter:** answer "what makes Level 1 daytime, Level 3 a sunset, and Level 7
> night — and how do you change it?" The short answer surprises people: **time of day is not a
> runtime setting; it is baked into each level's art.** This chapter proves that, names the few
> dynamic lighting levers that do exist, and shows how to manipulate the look.

Springfield's mood — bright noon, orange dusk, blue night — is one of the most atmospheric parts
of the game. It is also one of the most *misunderstood* to mod, because players look for a
"set time of day" switch that doesn't exist.

**Key finding (✅ verified):** there is **no time-of-day command and no time-of-day variable**.
An exhaustive search of the level scripts and `Simpsons.exe` finds **no** `SetTimeOfDay`,
`SetFog`, `SetSky`, or `SetAmbientLight` — none. The day/sunset/night look is **authored into
each level's art**: the world geometry's **baked vertex lighting**, the **sky dome texture**
(the sky is *art*, not code — C33.3), and the level's fog/horizon colours. Dynamic objects (cars,
characters) are lit by a global light asset, **`camlight.p3d`** (🟡 the camera-relative "sun").
The only lighting *commands* are shadow tweaks — **`SetShadowAdjustments`** (per **vehicle**, in
`.con` files — it tunes a car's blob shadow, **not** the time of day) and `SetStatepropShadow`
(prop shadows). So to change a level's time of day you **edit its art**, not a value.

---

## Deep-dive pages

- [C43.1 — What Sets the Time of Day](01-what-sets-it.md): the proof that it's baked art, per level, with no runtime switch.
- [C43.2 — The Sky Dome](02-sky-dome.md): the sky as a textured dome (art), and how it carries the time-of-day colour.
- [C43.3 — Baked Vertex Lighting](03-baked-vertex-lighting.md): how the static world carries its own light in vertex colours.
- [C43.4 — `camlight.p3d`: the Global Light](04-camlight.md): the light that keeps dynamic objects consistent.
- [C43.5 — Shadows (`SetShadowAdjustments`)](05-shadows.md): the per-vehicle/prop shadow levers — distinct from time of day.
- [C43.6 — Manipulating the Look](06-manipulating.md): making a level darker/warmer/night via art mods.

---

## 43.1 What sets it (✅ verified by absence + art)

No script command and no exe string sets time of day. The look is per-level **art**: each
level's world P3D ships its own baked lighting, sky, and fog. Load Level 7's art and you get
night because Level 7's *assets* are night — not because a clock was set. [C43.1](01-what-sets-it.md).

## 43.2 The sky dome (✅ verified art)

The sky is a **textured dome/backdrop** — pure art (C33.3), not a simulated atmosphere. Its
texture is where "sunset orange" or "night blue" actually lives. [C43.2](02-sky-dome.md).

## 43.3 Baked vertex lighting (✅ verified mechanism)

The static world's lighting is **baked into vertex colours** (Pure3D mesh colour streams, C7):
the level was lit offline and the result stored per vertex, so no runtime lights are needed for
the world. This is why a level's time of day is fixed — it's in the geometry. [C43.3](03-baked-vertex-lighting.md).

## 43.4 The global light — `camlight.p3d` (🟡 reasoned)

`camlight.p3d` is a global light asset the engine loads directly (not referenced by any script).
It behaves as the camera-relative directional "sun" that lights **dynamic** objects (cars,
characters, props) consistently, so they don't look flat against the baked world. [C43.4](04-camlight.md).

## 43.5 Shadows — not time of day (✅ verified)

`SetShadowAdjustments( 8 floats )` appears in **`.con` vehicle files** (e.g. `IStruck.con`,
mission cars) — it tunes that **vehicle's** shadow, and its values vary per car/mission, *not*
per time of day. `SetStatepropShadow` handles prop shadows. Don't mistake these for a lighting
clock. [C43.5](05-shadows.md).

## 43.6 Manipulating the look (✅ practical)

Because it's art, you change time of day by editing art: retint the world's vertex colours, swap
the sky dome texture, adjust `camlight`. A "night Level 1" is an **art mod**, not a value tweak.
[C43.6](06-manipulating.md).

---

## What this chapter established

- **Time of day is baked art, per level** — there is no runtime time-of-day switch, fog, or sky
  command (verified by exhaustive absence).
- The look lives in three art places: the **sky dome texture**, the world's **baked vertex
  lighting**, and the global **`camlight`** for dynamic objects.
- The only lighting *commands* are **shadow** tweaks (`SetShadowAdjustments` per vehicle,
  `SetStatepropShadow`) — unrelated to time of day.
- To change it, you **mod the art**, not a value.

**Cross-references:** C33 (rendering, lighting, the `tLight` family, sky-is-art), C7 (mesh colour
streams — where baked light lives), C5 (sky/texture art), C12 (level composition — which art a
level loads), C35 (vehicle shadows via `.con`), C15 (CON scripts).
