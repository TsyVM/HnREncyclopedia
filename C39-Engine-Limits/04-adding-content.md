# C39.4 — Adding Content that Loads & Renders

> Raising a cap makes *room*; it doesn't put anything in the room. To actually add an object, vehicle, or ped
> you run a five-step pipeline — author, package, reference, load, render — and a break at any step means your
> content is invisible even though the limit was raised. This page is that pipeline.

## The five steps

```
author ──► package (RCF/P3D) ──► reference (MFK) ──► load (GameFlow) ──► render (scenegraph)
  C5/C7        C1/C2                 C14               C30                 C10/C33
```

Miss any one and the symptom differs: no package → not found; no reference → never spawned; no load → spawned
but no asset; no scenegraph entry → loaded but not drawn. Diagnosing "my thing isn't showing up" is really
asking *which step broke*.

## 1. Author the asset (C5/C7)

Make the mesh/texture/skeleton as Pure3D chunks — a model (`Mesh`/`Shader`/`Texture`, C7/C5), and for a
character a skeleton + animations (C8/C34). New content is new `.p3d` chunks; match the chunk families the game
already uses for that content type (a car looks like the other cars' chunk sets).

## 2. Package it (C1/C2)

Put the `.p3d` into the level/asset load path — either a loose `.p3d` the game reads (C3.6 shadowing) or inside
an RCF archive (C2). The loader finds assets by name/hash, so your file must sit where the level expects that
name.

## 3. Reference it from the level (C14)

An asset nobody asks for is never spawned. Add the spawn to the level's MFK (C14): `AddObject` / `AddCharacter`
/ the vehicle-placement calls that name your model and place it. **This is also where you meet the caps** — the
per-model max and `SetMaxTraffic`/`maxPropCount` (C39.2). Raise those alongside adding the reference.

## 4. Make it load (C30)

The **GameFlow** `LoadingContext` (C30) streams the level's assets between loading screens. Your asset loads if
it's in the level's load set (step 2) and referenced (step 3). Large additions extend load time and press the
static heap (C39.3) — a new model is new resident memory. If the loader can't fit it, you're back to the heap
ceiling.

## 5. Make it render (C10/C33)

Loaded ≠ drawn. A visible object must be attached into the **scenegraph** (C10) so the render walk reaches it,
with a drawable (mesh + shader) and a world transform. The renderer (C33) draws what the scenegraph presents;
an object that loads but never joins the graph is memory with no pixels. For characters, it must also be
registered with the animation/AI systems to move.

## Worked shape — adding a drivable car

1. Author the car's `.p3d` (body mesh, wheels, shaders, textures) like an existing car (C7/C5).
2. Package it where the level loads cars from (C2).
3. In the level MFK, place it and, if it's traffic, raise `SetMaxTraffic` / the per-model cap (C39.2).
4. Confirm it streams in under the GameFlow loader (C30) without tripping the static heap (C39.3).
5. Confirm it enters the scenegraph and draws; confirm collision/physics attach (C10/C11/C35).
6. Measure with SAHRDiag (C28.7) — your new car should appear as a live `Vehicle`/model instance.

## Why "raise the limit" is only step 3

The whole point of this page: the limit (C39.1–C39.3) is one line in a five-line pipeline. People raise
`SetMaxTraffic`, see no change, and conclude it "doesn't work" — when in fact steps 1–2 or 4–5 were missing.
Always walk all five.

## Cross-references

- **C1/C2** — Pure3D and RCF packaging.
- **C5/C7/C8** — authoring textures, meshes, skeletons.
- **C10/C11/C33** — scenegraph, collision, rendering.
- **C14 — MFK** — the level references and caps.
- **C30 — GameFlow** — the loader that streams it in.
