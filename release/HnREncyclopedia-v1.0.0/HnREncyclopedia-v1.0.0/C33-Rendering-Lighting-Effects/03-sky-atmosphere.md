# C33.3 — Sky & Atmosphere: It's Art

**What it is.** An honest negative finding, and an instructive one: SHAR has **no sky, cloud, fog, or
atmosphere code system**. The sky you see is **art** — a skydome mesh with sky/cloud/sun textures. This page
documents the *absence* of a system as carefully as the presence of one, because knowing what *isn't* there
is as useful as knowing what is.

**The evidence (✅ verified negative).** A sweep of all 1,207 RTTI classes for `Sky`, `Cloud`, `Fog`,
`Atmosphere`, `Weather`, `Sun`, `Star`, `Horizon` finds **zero** real matches (the only hits are false
positives — `CGuiScreenPauseSunday`, a menu pun, and `CarStartLocator`). There is no atmosphere subsystem.
Meanwhile, the **texture index** (Legend) is full of sky art:

```
l7_backcloud.bmp    — level 7's background clouds
l3_Cloudmove.bmp    — an animated (scrolling) cloud layer for level 3
cloud1_alpha.bmp / cloud_smokealpha.bmp   — cloud sprites with alpha
sun2.bmp            — the sun
bluestarglow.bmp    — star glow (night skies)
burninterior_sky.bmp — an interior's sky backdrop
```

So the sky is **geometry + textures**, not code: a **skydome** (a large inverted dome mesh, C7) surrounding
the world, textured with a sky gradient and cloud layers, drawn behind everything (first, at max distance).
The `l3_Cloudmove` name reveals clouds are animated by **texture scrolling** (a texture-animation channel,
C34, sliding the cloud texture across the dome) — a cheap, classic sky effect.

**Why the sky is art, not a system.** A code-driven atmosphere (dynamic sky, volumetric clouds, weather) is
expensive and unnecessary for SHAR: the game has a fixed, cartoon Springfield sky per level, and a painted
skydome delivers it perfectly at almost no cost. Making the sky *art* means artists control exactly how each
level's sky looks (level 7's clouds differ from level 3's), it costs one dome mesh and a few textures, and it
needs no runtime system. This is the right engineering call for a stylised game with static skies — spend the
complexity budget on the driving, missions, and characters (which *do* have deep systems), and paint the sky.
It's a lesson in scope: not everything needs to be a system.

**Fog and distance.** Fog — the fade-to-haze at distance — is a **Direct3D 8 render state** (C33.1), a
per-frame setting the pipeline applies, not a class. It's used to hide the world's draw distance (the point
where streaming, C12.3, hasn't loaded yet) behind a haze. So "atmosphere" in SHAR is two art/state things:
the painted skydome (geometry + texture) and D3D fog (a render state) — neither a code subsystem.

**The modding consequence.** Because the sky is art, modding it is *art editing*, not code: replace the
skydome texture (C5.5) to change the sky's look, edit the cloud textures, or swap the skydome mesh (C7). You
can't "change the weather system" because there isn't one — but you can repaint the sky freely, which is
exactly the kind of edit the loose-file art pipeline (C28.2) makes easy. Want a night sky? Retexture the dome
with `bluestarglow`-style art.

**What happens if you bend it.**

- *Look for a sky/weather system to mod* — there isn't one. Edit the skydome texture/geometry (C5/C7).
- *Assume clouds are simulated* — they're a scrolling texture (`Cloudmove`, C34 texture animation). Edit the
  texture or its scroll.
- *Expect dynamic time-of-day* — the sky is a fixed painted dome per level. Different domes/textures per
  level give different skies, but there's no runtime day/night cycle.
