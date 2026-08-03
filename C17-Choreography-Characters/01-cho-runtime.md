# C17.1 — The `.cho` Runtime: Rig & Puppet

**What it is.** The runtime objects the `.cho` rig files (C8.1) become when loaded — the `choreo::Rig` and
its legs, and the `choreo::Puppet` that is a character under choreographic control. This is where the text
rig you decoded in C8 turns into live, drivable animation state.

**How it works (✅ verified).** The `.cho` file is read by a `choreo::` file reader and built into rig
objects. Verified classes from `shar_dumps.csv`:

```
choreo::ScriptReader : tRefCounted, radLoadObject      — parses the .cho script
choreo::StringFileReader : choreo::FileReader          — reads the text
ChoreoFileHandler                                       — the chunk handler that loads choreography
choreo::Rig : tEntity, tRefCounted                     — the runtime skeleton rig (the .cho `rig` block, C8.1)
choreo::RigLeg : tEntity, tRefCounted                  — one leg's IK chain (the .cho `leg` blocks, C8.1)
choreo::Puppet : tEntity, tRefCounted                  — a character driven by choreography
```

The mapping to the `.cho` data (C8.1) is direct: the `.cho` `rig "apu" { … }` block becomes a
`choreo::Rig`; each `leg "left" { … }` becomes a `choreo::RigLeg` with its thigh/knee/ankle IK chain; and the
character being animated is a `choreo::Puppet`. `choreo::ScriptReader` is what *reads* the `.cho` text at
load — the runtime counterpart to the file you decoded in C8.

**Why "puppet."** A `Puppet` is exactly the metaphor: a character whose motion is *driven* from outside —
by animation clips, by AI, by a cutscene — rather than moving on its own. The choreography engine (C17.2)
"pulls the strings" of the puppet's rig each frame, posing its joints. Separating the **puppet** (the driven
character) from the **rig** (its skeleton/IK definition) from the **drivers** (what's currently moving it,
C17.2) is the clean separation that lets one character be driven by walking one moment and a scripted
cutscene the next — you swap the driver, keep the puppet and rig.

**The rig/skeleton relationship.** The `choreo::Rig` is the *choreography* rig — the roles, IK chains, and
balance parameters from the `.cho` (C8.1) — layered over the raw *skeleton* in the character's `.p3d` (the
joints, C8.1). The skeleton is the bones; the rig is how choreography drives them (which joints are the
motion/balance/AI roots, how the legs solve IK). This is why a character needs *both* a skeleton (in the
`.p3d`) and a `.cho` rig: the skeleton is the anatomy, the rig is the operating instructions.

**What happens if you bend it.**

- *Edit the `.cho` rig without matching the skeleton* — the rig references joints by name (C8.1); a mismatch
  breaks IK or posing. Keep `.cho` joint names in sync with the `.p3d` skeleton.
- *Rely on a `choreo::` member offset* — the classes are ✅ (46 of them), offsets ⏳. Diff (C4.3).
- *Assume a puppet moves itself* — it's driven (C17.2). To change how it moves, change its driver, not the
  puppet.
