# C6.4 — Colour Parameters (`0x00011005`)

**What it is.** The colour material parameters — the RGBA values that set how a surface reflects each
component of light. These four (`DIFF`, `SPEC`, `AMBI`, `EMIS`) are the heart of the lighting material.

**How it works (✅ verified).** Each `0x00011005` is a **FourCC tag + RGBA byte quad**. The verified
vocabulary (each ~11,000 uses):

| Tag | Value | Is |
|---|---|---|
| `DIFF` | `FF FF FF FF` | **diffuse** colour (base surface colour under direct light) |
| `SPEC` | `FF 00 00 00` | **specular** colour (the highlight colour) |
| `AMBI` | `FF FF FF FF` | **ambient** colour (colour under ambient light) |
| `EMIS` | `FF 00 00 00` | **emissive** colour (self-illumination, unlit glow) |
| `CBVC` | — | the CBV-family colour |
| `COLB` / `TRNB` / `ENVB` | — | (colour/translucency/environment-blend, on reflective shaders) |

Verified colours read as `0xAARRGGBB`-style byte quads: `DIFF = FF FF FF FF` (opaque white — the texture
supplies the colour, the material doesn't tint it), `SPEC = FF 00 00 00` (opaque black — no specular
contribution for this matte shader), `EMIS = FF 00 00 00` (black — not self-illuminating). The **tags and
RGBA values are ✅**; the roles 🟡 from the mnemonics and the standard lighting model.

**The lighting equation.** These four colours are the terms of fixed-function lighting:

```
surface = EMIS  +  AMBI·ambientLight  +  DIFF·(texture)·diffuseLight  +  SPEC·specular(SHIN)
```

`EMIS` glows regardless of light (neon, screens); `AMBI` sets the shadowed-side colour; `DIFF` is the main
lit colour (usually white so the texture shows through); `SPEC` + `SHIN` (C6.3) make the highlight. A shader
with white `DIFF`/`AMBI` and black `SPEC`/`EMIS` is a plain textured matte surface — the common case. Change
these and you change how the surface responds to light without touching its texture.

**Why white diffuse is the default.** `DIFF = white` means "don't tint the texture" — the texture (C5)
provides the colour, and the material passes it through. This is why most shaders have white `DIFF`: the art
is in the texture, and the shader just lights it. A coloured `DIFF` *tints* the texture (a red `DIFF` makes
everything reddish) — used deliberately for effects, not as the norm. Same for `AMBI`. `SPEC`/`EMIS` are
usually black (off) and turned on only for shiny or glowing surfaces.

**What happens if you bend it.**

- *Set `DIFF` to a colour on a normal surface* — it tints the texture, often unintentionally. Keep `DIFF`
  white unless tinting is the goal.
- *Turn on `EMIS`* — the surface glows at full brightness regardless of lighting (looks flat/overbright).
  Use it only for genuinely self-lit surfaces.
- *Mismatch RGBA byte order* — colours come out wrong (channels swapped). Decode as the verified byte quad.
