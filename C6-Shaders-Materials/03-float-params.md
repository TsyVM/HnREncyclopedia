# C6.3 — Float Parameters (`0x00011004`)

**What it is.** The floating-point material parameters — the continuous values a shader's method uses, like
shininess and alpha thresholds. Fewer than the integer flags (C6.2), but they carry the *analog* tuning of a
surface.

**How it works (✅ verified).** Each `0x00011004` is a **FourCC tag + float32**. The verified vocabulary
(each ~11,000 uses):

| Tag | Value (example) | Governs (🟡) |
|---|---|---|
| `SHIN` | 10.0 | **shininess** (specular exponent) |
| `MSHP` | 0.5 | (material sharpness / specular power) |
| `ACTH` | 0.5 | **alpha threshold** (for the alpha test, pairs with `ATST`/`ACMP`, C6.2) |
| `CBVV` | — | the CBV-family float |

Verified: a shader's `SHIN` reads `10.0` (`0x41200000`), a plausible specular exponent; `ACTH` reads `0.5`,
a mid alpha cutoff. The **tags and float values are ✅**; the **meanings 🟡** from the mnemonics and typical
material math. `SHIN` (shininess) controls how tight and bright the specular highlight is — high for shiny
plastic/metal, low for matte; `ACTH` sets where the alpha test cuts (pixels below the threshold are
discarded — how cut-out foliage and fences render).

**Why separate float params from int flags.** Render *state* is discrete (a blend mode is one of a few
enums, C6.2); material *properties* are continuous (shininess is any value). Splitting them — integers for
state, floats for properties — matches how the hardware and the math work: the int flags configure the
pipeline, the floats feed the lighting equation. It also keeps each param chunk simple (tag + one typed
value), with the type baked into the chunk id (`0x00011004` = float).

**The lighting tie.** `SHIN`/`MSHP` feed the specular term of the lighting equation, and the colour params
(C6.4) feed its diffuse/ambient/specular/emissive terms. Together, a shader's floats and colours *are* its
lighting material: `AMBI` + `DIFF` + `SPEC`·(specular from `SHIN`) + `EMIS` is the classic fixed-function
lighting model. So C6.3 (floats) and C6.4 (colours) jointly define how a surface responds to light — the
floats shape the specular, the colours set the reflectance.

**What happens if you bend it.**

- *Crank `SHIN` very high* — the specular highlight becomes a tiny bright pinpoint (very shiny); very low and
  it spreads to a dull sheen. Tune it to the material.
- *Set `ACTH` wrong on an alpha-tested surface* — foliage/fences either disappear or show their full quad.
  Match the threshold to the texture's alpha (C6.2 `ATST`).
- *Read the float as an int (or vice versa)* — the chunk id tells you the type (`0x00011004` = float). Decode
  per id.
