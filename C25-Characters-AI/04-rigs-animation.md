# C25.4 — Rigs, Animation & Choreography

**What it is.** How the character *data* decoded in C8 — the `.cho` rig, the animation-state graph, the
skinned mesh — drives a *live* character each frame, and where the `choreo::` classes stage scripted
performances. This is the runtime of C8 and the lead-in to C17.

**How it works (✅ data → runtime).** A live `Character` (C25.1) animates through the pipeline C8 laid out,
now in motion:

1. The **`CharacterAi` state** (C25.2) decides what the character is doing — say, `Loco` (walking).
2. The state requests an **animation state** by name (C8.2) — e.g. an idle or walk state.
3. The `.cho` **state→clip map** (C8.2) resolves it to a clip, picking the costume-appropriate variant.
4. The clip poses the **skeleton** (C8.1); the **IK legs** solve foot placement on the ground.
5. The **skin** (C8.3) deforms the mesh (C7) to the posed skeleton.
6. The scene graph (C10) draws the result.

So the `.cho` file you decoded statically is the *configuration* this runtime loop reads: the rig defines the
joints and IK, the state map defines which clip plays for which behaviour. Change the `.cho` (C8) and you
change the live character's motion.

**Choreography (`choreo::`, ✅ 46 classes).** Beyond ambient animation, the `choreo::` namespace (C23.3)
stages *scripted* character performances — the cutscene and mission set-pieces where characters walk marked
routes, turn to face each other, and act out dialogue. This is the runtime of the choreography system
(Chapter 17) and it's driven by the mission scripts' camera/dialogue verbs (C14.6): `SetConversationCam`,
`SetDialogueInfo`, and the waypoint commands (C14.5) feed the `choreo::` classes to produce a staged scene.
The 46 `choreo::` classes are the machinery that turns "these characters, this dialogue, these marks" into a
performance.

**Why split ambient animation from choreography.** Ambient animation (walking, idling) is *reactive* — driven
by the AI state (C25.2) moment to moment. Choreography is *authored* — a designer scripts a specific
performance. Keeping them separate (the `.cho` state map for ambient, `choreo::` for scripted) means the same
character can wander autonomously and also hit precise marks in a cutscene, using different systems for each.
It mirrors the ambient-vs-scripted split elsewhere: road graph vs. path segments (C13), traffic vs. mission
cars (C24.3).

**What happens if you bend it.**

- *Edit a clip but not the state that requests it* — the behaviour still asks for the old state name (C8.2).
  Keep the state map and clips in sync.
- *Rely on a `choreo::` class offset* — the classes are ✅, offsets ⏳. Diff (C4.3).
- *Expect ambient animation to produce cutscene precision* — use `choreo::` (scripted) for staged
  performances, the `.cho` state map (reactive) for ambient motion.
