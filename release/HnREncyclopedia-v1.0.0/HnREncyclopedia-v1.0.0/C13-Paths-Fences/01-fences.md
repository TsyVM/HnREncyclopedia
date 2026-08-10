# C13.1 — Fences: Barrier Segments (`0x03000000`)

**What it is.** The invisible walls that keep vehicles on the road and out of the scenery. A fence is a
single line-segment barrier; chained together, fences form the continuous edges of the drivable world.

**How it works (✅ verified).** A `0x03000000` Fence is 36 bytes — nine floats — decoded from
`art/b01 - Copy.p3d`:

```
start  = (-29.83, 0.0, -29.35)
end    = (-29.92, 0.0,  34.73)
normal = (-1.0,   0.0,   … )
```

Two points on the ground plane define the wall's extent; the normal says which side is "inside." A car that
tries to cross the segment from the inside is pushed back. A level block holds **49** such segments (verified),
and they chain end-to-end into the barrier running along each street. The `y = 0.0` in both points shows
fences are essentially 2-D (ground-plane) barriers extruded vertically — you can't drive *through* them, but
they don't need a height because cars are on the ground.

**Why line-segment fences instead of mesh collision.** The visible world already has collision (C11), but
using it to contain cars would be both expensive (narrow-phase against detailed geometry every frame for
every car) and *wrong* — you want a car nudged smoothly back onto the road, not to crash into an invisible
wall shaped like a hedge. A simple line segment with a normal gives a cheap, smooth containment test: which
side of the line is the car on, and push it toward the inside. This is the classic driving-game "invisible
wall," and storing it as a handful of floats per segment is why a level can afford thousands of them.

**Reading a level's fences.** Walk for `0x03000000`, collect the segment endpoints, and you can plot the
drivable boundary of a level as a 2-D map — a genuinely useful debugging view (overlay it on the terrain,
C12). Gaps in the fence chain are where a car *can* leave the road (shortcuts, or bugs); a continuous chain
is a sealed street.

**What happens if you bend it.**

- *Flip a fence's normal* — the "inside" and "outside" swap, and the fence pushes cars *off* the road
  instead of onto it. Keep normals pointing into the drivable area.
- *Leave a gap in the chain* — cars escape the road there. Intentional for a shortcut; a bug otherwise. Check
  continuity when editing.
- *Give a fence a height expecting a 3-D wall* — fences are ground-plane segments; for true 3-D blocking use
  collision (C11). Don't conflate the two systems.
