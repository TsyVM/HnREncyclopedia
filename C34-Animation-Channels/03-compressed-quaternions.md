# C34.3 — Compressed Quaternions

**What it is.** Why rotation — and only rotation — gets a second, *compressed* channel type
(`tCompressedQuaternionChannel`). It's a targeted optimisation for the single largest category of animation
data in the game: skeletal joint rotations.

**How it works (✅ verified).** There are two rotation channels: `tQuaternionChannel` (full precision, 4
floats = 16 bytes per keyframe) and `tCompressedQuaternionChannel` (packed into far fewer bytes). The
compressed form exploits the mathematics of unit quaternions: a rotation quaternion is always **unit length**
(`x²+y²+z²+w²=1`), so one component is redundant — you can store three and reconstruct the fourth. Combined
with quantising each component to fewer bits (rotations don't need full float precision to look smooth), a
compressed quaternion fits in a fraction of the 16 bytes, at a small, usually imperceptible, precision cost.

**Why rotation specifically.** Do the arithmetic: a character has dozens of joints (C8.1), each joint's
rotation is a quaternion channel, and each channel has many keyframes across an animation — and the game has
hundreds of animations (C8.2) across dozens of characters. Rotation keyframes are, by a wide margin, the
**bulk of all animation data**. Position and scale animate less (a character's joints rotate; they don't
usually translate or scale independently), and colours/floats/events are comparatively tiny. So compressing
*rotation* compresses the thing that dominates — a targeted optimisation with the biggest payoff. Positions
and colours don't get a compressed channel because they're not the bottleneck; rotation is, so it gets the
special treatment.

**The precision trade.** Compression loses a little precision — a compressed rotation is very slightly off
from the exact one. For skeletal animation this is invisible: a joint rotated 0.1° off from the authored
value looks identical in motion, and the eye can't detect it across a fast animation. The trade — a large
size saving for imperceptible precision loss — is exactly right for the use case. Where precision *does*
matter (a precise camera move, perhaps), the full `tQuaternionChannel` is available. Having both lets each
use pick: compressed for the bulk skeletal data, full for the rare precision-critical rotation.

**Why this matters for the format.** When you decode a character's animation data (C8), you'll meet *both*
channel types, and you must decode the compressed one correctly (unpack three components, reconstruct the
fourth from the unit-length constraint, dequantise) — reading it as a full quaternion gives garbage. This is
the kind of format detail (like the P3DZ compression, C1.9) where knowing the *reason* (rotation is the
bulk, so it's compressed) tells you *what to expect* (most joint channels are the compressed type). The
compression is a property of the animation data, and decoding animations means handling it.

**What happens if you bend it.**

- *Decode a compressed quaternion channel as a full one* — you read packed bytes as floats, producing garbage
  rotations. Detect the type and unpack accordingly.
- *Re-compress with the wrong quantisation* — the game's decoder expects its exact packing (the precise bit
  layout is ⏳ in this data set; the *concept* is verified). Match the format.
- *Use compressed rotation where precision is critical* — a jittery precise camera. Use the full channel where
  precision matters.
