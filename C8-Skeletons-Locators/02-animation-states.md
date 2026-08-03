# C8.2 — Animation States & Clips

**What it is.** The section of a `.cho` that maps **animation states** — the names the game asks for — to
**clips** — the actual animations that play. It is the character's behaviour vocabulary, including
per-costume variants.

**How it works (✅ verified).** After the rig, `apu.cho` lists state→clip mappings:

```
rig "apu";
animation "apu_idle0"       { animation "apu_idle_yoga"; }
animation "apu_idle1"       { animation "apu_idle_pants"; }
animation "apu_idle2"       { animation "apu_idle_backspin"; }
animation "a_american_idle0"{ animation "apu_idle_riding_horse"; }
animation "a_army_idle0"    { animation "apu_idle_army"; }
animation "a_besharp_idle0" { animation "apu_idle_be_sharp"; }
```

The **outer** name is the state the engine requests (`apu_idle0`); the **inner** name is the clip it plays
(`apu_idle_yoga`). The system asks for a *role* ("play idle variant 0") and the `.cho` decides *which
animation* fulfils it. The `a_american_*`, `a_army_*`, `a_besharp_*` prefixes are **costume sets**: when Apu
wears his army costume, `a_army_idle0` routes to `apu_idle_army` instead of the default — so the same "idle"
request produces costume-appropriate behaviour.

**Why the indirection.** Decoupling states from clips is what makes characters reusable and costumes cheap.
Gameplay code says "idle" without knowing which of a dozen idles will play; the `.cho` maps that to a clip,
and can pick a costume-specific one. Add a costume and you add a state set, not new gameplay code. It is the
same "request a role, resolve to an asset" pattern as the shader→texture binding (C6) and the scene-graph
drawable reference (C10.4) — indirection through a name table, applied to animation.

**The clips themselves.** The named clips (`apu_idle_yoga`, `apu_idle_army`) are the actual keyframed
animations, stored in the character's `.p3d` (the animation-group chunks, `0x00004500` family) and played
on the skeleton (C8.1). The `.cho` never contains the animation data — only the mapping — which keeps the
behaviour graph small and readable.

**What happens if you bend it.**

- *Map a state to a clip that doesn't exist* — the request resolves to nothing and the character freezes in
  that state. Ensure the named clip is present in the `.p3d`.
- *Omit a costume's state set* — that costume falls back to (or lacks) default states and idles wrong. Give
  each costume its full set.
- *Reuse a state name for two clips* — the later wins; the earlier is dead. Keep state names unique within a
  character.
