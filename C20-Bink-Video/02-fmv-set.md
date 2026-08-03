# C20.2 — The FMV Set

**What it is.** The 16 movies in `movies/`, what each is, and how they group. Together they are the game's
non-interactive video — the logos that bookend it and the cutscenes that tell its story.

**How it works (✅ verified).** The set, by role:

| Role | Files | Plays |
|---|---|---|
| **Licensor / studio logos** | `foxlogo`, `radlogo`, `vuglogo`, `gracie` | at boot, before the menu |
| **Narrative** | `intro`, `credits` | game open / end |
| **Cutscenes & mission FMV** | `fmv1A`, `fmv2`, `fmv3`–`fmv8`, `loot`, `tele` | triggered in-story |

The logos are the rights-holders: **Fox** (the Simpsons license), **Radical** (developer), **VU Games**
(Vivendi Universal, publisher), and **Gracie Films** (the Simpsons production company). They play in sequence
at startup — the legally-required credits before you reach the menu. The **cutscenes** (`fmv1A`–`fmv8`, plus
named ones like `loot` and `tele`) are the animated story beats, triggered by the **`fmv` mission objective**
(C16.3, 6 uses) at scripted points.

**Why FMV rather than in-engine cutscenes.** SHAR uses *both* — in-engine choreography (`choreo::`, C25.4) for
most character scenes, and pre-rendered Bink FMV for the big moments and the logos. Pre-rendered video buys
**fidelity and certainty**: a Bink cutscene looks identical on every machine regardless of hardware, can
include effects the real-time engine can't, and can't be broken by a physics glitch. The cost is size (244 MB)
and inflexibility (it's a fixed video). So the game reserves FMV for what benefits most — the polished intro,
the story climaxes, the untouchable logos — and does the rest in-engine where interactivity and world state
matter.

**The 640×480 resolution.** All the Bink FMVs are 640×480 (C20.1) — standard-definition 4:3, the resolution
of 2003 televisions and monitors. The video was authored to fill the screen at the era's display standard;
on a modern widescreen it letterboxes or stretches. This is a fixed property of the source video, not
something the engine changes.

**Reading the set.** Dumping the Bink headers (C20.1) across the folder inventories the game's video: frame
counts and durations tell you which are short stings (the logos, a few seconds) versus full cutscenes (`fmv2`
is 1,333 frames ≈ 44 seconds at 30 fps). This is how you'd audit the FMV content without watching all 244 MB.

**What happens if you bend it.**

- *Reorder or remove the logo movies* — they're legally-required attributions; removing them has licensing
  implications beyond the technical. Handle with care.
- *Replace a cutscene with a different resolution* — the player expects the movie's own dimensions (C20.1);
  keep 640×480 or update the player's expectations.
- *Assume every `.rmv` is Bink* — 15 are; `credits.rmv` isn't (C20.3). Check the magic per file.
