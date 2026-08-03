# C12.5 — Ambient Gags & Population

**What it is.** The comedy and life baked into a level before any mission runs — the gags scattered across
Springfield, the ambient drivers, and the vehicle roster. This is what makes a level feel like a place, not
just a stage.

**How it works (✅ verified).** `level.mfk` for level 01 contains **39 gags** — full `GagBegin…GagEnd` blocks
(the gag system of C14.4) — plus `SuppressDriver` calls (25), `AddVehicleSelectInfo` (4), and
`GagSetAnimCollision` (3). Each gag is a self-contained interactive joke placed in the world: a trigger, a
sound, an animation cycle, a coin reward, positioned at a spot in the level. `SuppressDriver` removes drivers
from certain ambient cars (parked or scripted vehicles). The gags run whether or not you're on a mission —
they are the level's ambient texture.

**Why bake ambient content into the level script.** The gags and ambient population are properties of the
*place*, not of any mission, so they live in the *level* script rather than a mission script (C16). This
means the moment a level loads, its jokes and life are active — drive around Level 1 and the 39 gags are
there to find regardless of story progress. It also means the ambient comedy is authored once per level, in
one file, rather than repeated in every mission set in that level. This mirrors the general SHAR split:
place-level content in `level.mfk`, mission-level content in `m{N}i.mfk`.

**How this ties to the world.** Each gag references a **locator** (C8.4) for its position, a **sound** (C19)
for its audio, and an **animation** (C8.2) for its motion — so the level's gags are the meeting point of the
locator, audio, and animation systems, wired by the gag verbs (C14.4). The 39 gags of Level 1 are 39 such
wirings, each turning a spot in Springfield into an interactive moment.

**Reading a level's character.** The gag and population content is what gives each level its personality —
Level 1's suburban jokes differ from downtown's. Dumping the `level.mfk` gag blocks (they're plain text) is
the fastest way to inventory what a level *does* ambiently, and it's the layer a modder edits to add new
jokes or change the feel of a place without touching missions.

**What happens if you bend it.**

- *Add a gag referencing a missing locator/sound/animation* — it fails silently (C14.4). Ensure all three
  referenced assets are loaded.
- *Remove `SuppressDriver` from a car meant to be empty* — a driver appears where there shouldn't be one.
  Keep suppression on scripted/parked vehicles.
- *Over-populate a level with gags* — each is live work; too many can crowd the level and the budget. Add
  ambient content in proportion to the place.
