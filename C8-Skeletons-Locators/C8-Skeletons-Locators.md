# Chapter 8 — Skeletons, Skinning & Locators

> **Goal of this chapter:** decode how characters are rigged and animated, how skinned meshes bind to
> skeletons, and how the locators baked into geometry give gameplay its attachment points. After this
> chapter you can read a character's rig, its animation states, and the markers scripts hang behaviour on.

Characters are the most articulated assets in the game, and SHAR splits their definition across two forms:
**binary Pure3D** (`0x00017002` Skin, joints, and the `0x00015800`/`0x07010001` locator/frame families) and
**plain-text `.cho`** rig files (`art/chars/*.cho`) that declare the skeleton and map animation states to
clips. Both were decoded directly — the `.cho` structure from `apu.cho`, the binary chunks from real
character and level `.p3d` files.

**Key finding (✅ verified):** the `.cho` file is a character's brain — a **skeleton rig** (joints, IK legs
and arms) plus an **animation-state graph** that maps named states (including per-costume variants like
`a_army_idle0`) to actual animation clips. There are **8** shipped `.cho` files: `apu`, `bart`, `homer`,
`lisa`, `marge`, `ndr`, `npd`, `nps`.

---

## Deep-dive pages

- [C8.1 — The `.cho` Rig: Skeleton, Legs & IK](01-cho-rig.md): the text skeleton definition and inverse kinematics.
- [C8.2 — Animation States & Clips](02-animation-states.md): the state→clip map and per-costume variants.
- [C8.3 — Skinning (`0x00017002`/`0x00017001`)](03-skinning.md): binding a mesh to a skeleton.
- [C8.4 — Locators (`0x00015800`/`0x00015801`/`0x00015806`)](04-locators.md): named attachment points in the world.
- [C8.5 — Frames & the Locator Hierarchy (`0x07010001`)](05-frames.md): the frame tree scripts and cameras attach to.

---

## 8.1 The `.cho` rig (✅ verified)

A `.cho` opens with a **rig** block that names a skeleton and defines the limbs with full inverse-kinematics
data, decoded from `apu.cho`:

```
rig "apu" {
    skeleton "apu";
    jointIndex_AIRoot 0;  joint_MotionRoot "Motion_Root";  joint_BalanceRoot "Balance_Root";
    leg "left"  { joint_Thigh "Hip_L"; joint_Knee "Knee_L"; joint_Ankle "Ankle_L"; footPlantChannelIndex 1; }
    leg "right" { … }
}
```

Named joints, foot-plant channels, balance roots — this is a real IK rig, authored in text. [C8.1](01-cho-rig.md).

## 8.2 Animation states (✅ verified)

After the rig, the `.cho` maps **animation states to clips**, including **per-costume** variants:

```
rig "apu";
animation "apu_idle0"      { animation "apu_idle_yoga"; }
animation "a_army_idle0"   { animation "apu_idle_army"; }
animation "a_besharp_idle0"{ animation "apu_idle_be_sharp"; }
```

`apu_idle0` is the *state* the game requests; `apu_idle_yoga` is the *clip* it plays. The `a_army_*`,
`a_american_*`, `a_besharp_*` prefixes are **costume-specific** idle sets — Apu in his army costume idles
differently. This state→clip indirection is the character animation system. [C8.2](02-animation-states.md).

## 8.3 Skinning (✅ verified)

In the binary, `0x00017002` is the **Skin**: it binds a mesh to a skeleton so the mesh deforms with the
joints. Verified: a `0x00017002` in `apu_electrocuted.p3d` names a shape (`homercute1Shape`) and a shader
(`apucuted_m`) and contains `0x00017001` skin data (48 skin/data pairs in one level block). [C8.3](03-skinning.md).

## 8.4 Locators (✅ verified)

`0x00015800` is a **Locator group** (named, e.g. `smokecolumnShape`, with float params) holding
`0x00015801`/`0x00015806` **locators** — named, positioned markers. Locators are the anchors gameplay uses:
spawn points, trigger centres, effect emitters, camera nodes. Scripts reference them by name (C14.5).
[C8.4](04-locators.md).

## 8.5 Frames (✅ verified)

`0x07010001` is a **Frame** node that nests child frames (verified: one frame with 36 child frames) — a
transform hierarchy, distinct from the scene graph, that cameras, effects, and attachments hang on
(`0x07010007` frame data is 48,968 instances game-wide). [C8.5](05-frames.md).

---

## Key takeaways

- A character = **binary rig/skin/locators** (`.p3d`) + a **text `.cho`** (skeleton rig + animation-state
  graph). 8 shipped `.cho` files.
- The `.cho` rig defines named joints and **IK legs/arms**; the state section maps **states → clips**,
  with **per-costume** variants (`a_army_idle0` → `apu_idle_army`).
- `0x00017002` **Skin** binds a mesh to the skeleton (mesh name + shader name + `0x00017001` data).
- **Locators** (`0x00015800`+) are named attachment points scripts and gameplay reference (C14.5).
- **Frames** (`0x07010001`) are a transform hierarchy for cameras/effects/attachments.

**Next:** [Chapter 9 — Geometry Import/Export](../C9-Geometry-IO/C9-Geometry-IO.md) or [Chapter 10 — The Scenegraph](../C10-Scenegraph/C10-Scenegraph.md).
