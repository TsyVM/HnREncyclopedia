# C8.4 — Locators (`0x00015800` / `0x00015801` / `0x00015806`)

**What it is.** Named, positioned markers baked into geometry that gameplay hangs behaviour on. A locator is
not drawn — it is a labelled point (or point + data) in the world that scripts, effects, cameras, and AI
reference by name.

**How it works (✅ verified).** `0x00015800` is a **Locator group**, itself named, holding individual
locators. Decoded from `art/b01 - Copy.p3d`:

```
0x00015800 Locator group  name="smokecolumnShape"   (own: name + float params, e.g. 30.0)
  0x00015806 ×2   locator entries
  0x0001580b ×1   locator data
0x00015801       locator
```

Each locator carries a position and a type/role. The group name (`smokecolumnShape`) tells you what it's for
— here, where a smoke-column effect emits. Across the game these are the anchors for: **spawn points** (where
NPCs and cars appear), **trigger centres** (where entering fires a mission event), **effect emitters** (smoke,
sparkle), **camera nodes**, and **teleport destinations**. Scripts reference them by name via
`AddSpawnPointByLocatorScript` and the waypoint commands (C14.5).

**Why bake locators into geometry.** A spawn point or an effect emitter is fundamentally a *place*, and the
natural place to author a place is in the same tool that built the level geometry. Baking locators into the
`.p3d` means the artist who models a street corner also drops the spawn point there, and the position stays
correct if the geometry moves. Naming them lets the *script* layer (C14) — authored separately — bind
behaviour to those places without knowing their coordinates: "spawn at `smokecolumnShape`," not "spawn at
(x,y,z)." This separation of *where* (baked locators) from *what happens there* (scripts) is the same
data/logic split as the rest of the engine.

**Reading and using them.** To find every attachment point in a level, walk for `0x00015800` groups and
collect their locators and names — the result is a map of every scriptable place. To add one (a new spawn
point), add a locator with a name your script references. Because they're named, the binding is by string,
so a new locator + a new `AddSpawnPointByLocatorScript` line (C14.5) is a complete addition.

**What happens if you bend it.**

- *Reference a locator name that isn't in the loaded geometry* — the spawn/trigger silently fails (C14.5).
  Ensure the named locator exists in a loaded `.p3d`.
- *Move geometry but not its locators* — spawn points and emitters end up in the wrong place. Locators are
  baked with the geometry; move them together.
- *Assume a locator is drawn* — it isn't; it's an invisible marker. To see one, dump the tree (C4.2) and
  read its name and position.
