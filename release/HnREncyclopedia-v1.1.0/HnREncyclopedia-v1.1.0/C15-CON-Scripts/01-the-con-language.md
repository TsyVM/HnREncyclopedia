# C15.1 — The CON Language

**What it is.** The grammar of a `.con` file, in full. It is the smallest language in the game: a
sequence of setter calls, one per statement, executed against the vehicle being constructed.

**How it works.** Three token classes and one rule:

- **Comments** — `//` to end of line. The first comment of a car file is conventionally its human name and
  role: `// Ambulance (Traffic AI)`, `// Otto School Bus (cooool dude!)` (✅ observed across the tree).
- **Setter calls** — `Name(arg, arg, …);`. The name is one of the ~30 verified commands (C15 hub table);
  the arguments are almost always floats, occasionally an integer flag (`SetCharactersVisible(1)`), a
  vector spread as several floats (`SetShadowAdjustments` takes 8), or a string (`SetDriver("homer")`).
- **Whitespace** — free. Blank lines group related settings by convention; they carry no meaning.

The one rule: **statements run in order, each mutating the vehicle under construction.** There is no
control flow — extraction across all 255 files finds nothing but `Set…` calls and comments (the only
capitalised non-`Set` tokens are words *inside* comments). So a `.con` is best read as a property sheet
that happens to be written as function calls.

**Why it's built this way.** A flat setter list is trivial for the engine to parse (a tokenizer and a
name→function table) and trivial for a designer to author and tweak — which is exactly what tuning 90
vehicles demands. It also means the file has no structural invariants to maintain: unlike a Pure3D file
(C1.5) or an RCF (C3.4), you can add, remove, or reorder lines freely and nothing else needs fixing.

**The execution model, concretely.** When the game loads a car (via `LoadDisposableCar` or the player-car
path, Chapter 14), it creates a vehicle object with **default** handling, then runs the `.con`, and each
`Set…` overwrites one default. A value you don't set keeps its default — which is why some commands appear
in only 55 or 33 of the 90 cars (C15 hub): those cars accept the default for the rest. This is the same
"default then override" model as many config formats, and it means a minimal `.con` is legal.

**Argument types you will meet.**

- *Scalar float* — the overwhelming majority: `SetMass(2500.0)`, `SetTireGrip(2.5)`.
- *Integer flag* — `SetCharactersVisible(1)`, `SetHasDoors(0)`; 0/1 booleans.
- *Multi-float* — `SetShadowAdjustments(-0.1, -0.3, -0.1, 0.5, 0.0, 0.5, 0.0, -0.5)` (a shadow shape),
  `SetCMOffsetX/Y/Z` as three separate calls forming a vector.
- *String* — `SetDriver("…")` names a character (🟡 — string form observed; the exact resolution is C24).

**What happens if you bend it.**

- *Malformed call* (missing `;`, wrong arg count) — the parser may skip the line or the car may load with
  a default in that slot. Keep the call shape exact; match the arg count the retail files use for that
  command.
- *Reorder a dependent pair* — most settings are independent, but where two interact (the slip pair in
  C15.3), keep them together and in the retail order to avoid surprises. Order rarely matters, but when it
  does it is within a related group.
- *Add an unknown `Set…`* — an unrecognised name is ignored by the engine (no handler), so a typo is a
  silent no-op, not an error. Verify the name against the C15 hub table.
