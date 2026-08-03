# C6.2 — Integer Parameters (`0x00011003`)

**What it is.** The largest parameter family — the integer render-state flags that configure a shader's
method. `0x00011003` is the single most common chunk in the whole game (224,971 instances, C2.3), because
every shader carries a dozen-plus of them.

**How it works (✅ verified).** Each `0x00011003` is a **FourCC tag + int32**. The verified tag vocabulary,
extracted and counted across the corpus (each appears ~11,000 times — once per shader):

| Tag | Governs (🟡 from mnemonic) |
|---|---|
| `SHMD` | shade mode |
| `FIMD` | fill mode (solid/wireframe) |
| `BLMD` | blend mode (opaque/alpha/additive) |
| `UVMD` | UV / texture-address mode (wrap/clamp) |
| `ACMP` | alpha-compare function |
| `ATST` | alpha test (on/off) |
| `2SID` | two-sided (backface culling on/off) |
| `MMIN` / `MMAX` / `MMEX` | mip min / max / … levels |
| `PLMD` | (polygon/light mode) |
| `CBVM` / `MCBV` / `CBVA` / `CBVB` / `CBVP` | the "CBV" family (colour-buffer/vertex control) |

The **tags and their int values are ✅ verified** (read from bytes); the **meanings are 🟡** (inferred from
the four-character mnemonics and standard render state). `2SID=0` means one-sided; `BLMD=2` selects a blend
mode; `ACMP=4` an alpha-compare function. These are the classic fixed-function render states of a D3D8-era
engine (SHAR renders on Direct3D 8, C28), exposed as tagged integers.

**Why so many integer flags.** A fixed-function GPU (2003 hardware) is configured by *state* — blend mode,
alpha test, cull mode, texture addressing, mip range — and each of these is an integer setting. A shader that
must fully specify how its surface draws needs to set all of them, so ~16 integer params per shader is simply
the render-state surface of the hardware. Multiply by ~11,000 shaders and you get the 224,971 instances that
make `0x00011003` the most common chunk in the game — a direct measure of how much of SHAR is *material
configuration*.

**Why FourCC-tagged.** The tag model (C6, C11.3) lets a shader carry exactly the params its method needs, in
any order, and lets a reader decode by tag rather than a fixed struct. A `simple` shader sets the common
states; a fancier method adds its own tags. Unknown tags are ignored (like unknown chunks, C1.8), so the
format is extensible. This is why the same `0x00011003` chunk id serves every integer flag — the tag
disambiguates.

**What happens if you bend it.**

- *Change `2SID` / `BLMD` / `ACMP` carelessly* — you alter culling, blending, or alpha behaviour and the
  surface renders wrong (invisible backfaces, wrong transparency). Understand the state before flipping it.
- *Read a param by position instead of tag* — params can be in any order; read by FourCC (C6).
- *Add an unknown tag* — it's ignored (a no-op). Use verified tags.
