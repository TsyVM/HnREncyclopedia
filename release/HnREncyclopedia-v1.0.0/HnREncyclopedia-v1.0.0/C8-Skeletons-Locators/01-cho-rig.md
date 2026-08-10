# C8.1 — The `.cho` Rig: Skeleton, Legs & IK

**What it is.** The rig block at the top of a `.cho` file: a text declaration of a character's skeleton and
its inverse-kinematics limbs. It tells the animation system what joints exist and how the legs and arms
solve for foot- and hand-placement.

**How it works (✅ verified).** Decoded from `art/chars/apu.cho`:

```
rig "apu" {
    skeleton "apu";                       // the skeleton asset (in the .p3d)
    jointIndex_AIRoot        0;
    jointIndex_OrientationRoot 0;
    joint_MotionRoot   "Motion_Root";
    joint_BalanceRoot  "Balance_Root";
    joint_CharacterRoot "Character_Root";
    maxBalanceRootCompress 0.25;
    leg "left" {
        jointIndex_FootPlant 1;  footPlantChannelIndex 1;
        joint_Thigh "Hip_L";  joint_Knee "Knee_L";  joint_Ankle "Ankle_L";
        joint_FKMin "Hip_L";  joint_FKMax "Ball_L";
    }
    leg "right" { … }
}
```

Every joint is **named** (`Hip_L`, `Knee_L`, `Ankle_L`) and mapped to a role. The **roots** (Motion,
Balance, Character, AI, Orientation) are the anchors different systems use: the AI moves the AI root, the
animation moves the motion root, physics balances around the balance root. The **legs** carry full IK
chains (thigh→knee→ankle) plus foot-plant channels so feet lock to the ground instead of sliding.

**Why a text rig.** Rigging is authored and iterated by animators, and a text format lets them tune joint
mappings, IK chains, and balance parameters without a binary tool — the same reason handling lives in text
`.con` (C15) and missions in text `.mfk` (C14). Naming joints (rather than indexing them) makes the rig
readable and robust to skeleton edits: add a joint and the named references still resolve. The multiple
roots are what let AI navigation, animation playback, and physics balance act on one character without
fighting — each drives its own root.

**Why IK matters here.** SHAR characters walk on uneven ground (kerbs, stairs, slopes). Forward kinematics
alone would float or sink feet; the leg IK chains plus foot-plant channels solve ankle position so feet
meet the surface. That the rig bakes this in — per leg, with explicit thigh/knee/ankle joints — is why the
cartoon characters move believably despite exaggerated proportions.

**What happens if you bend it.**

- *Rename a joint in the skeleton but not the rig* — the `joint_…` reference no longer resolves and that
  limb's IK breaks. Keep names in sync between the `.p3d` skeleton and the `.cho` rig.
- *Remove a root* — the system that drives it (AI, animation, physics) loses its anchor. Keep all roots.
- *Break an IK chain* (wrong thigh/knee/ankle) — feet slide or hyperextend. Preserve the anatomical order of
  the chain.
