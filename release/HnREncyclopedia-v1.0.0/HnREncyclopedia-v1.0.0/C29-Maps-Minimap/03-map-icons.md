# C29.3 — The Map Icons

**What it is.** The vocabulary of markers the map draws on top of the model — 12 icon sprites, each meaning
one kind of point of interest. Reading the icon set is reading what the game wants you to *do*.

**How it works (✅ verified).** The icons are PNGs in `images\hud\mapicons\`, declared as page resources
(C21.2) and drawn as pooled sprites (C29.1). The complete verified set and its gameplay meaning:

| Icon | Marks | Ties to |
|---|---|---|
| `user` | the player's position | C29.5 |
| `mission` | an available story mission | C16 |
| `phone` | a mission phone (where a mission starts) | C14/C16 |
| `aicar` | a target or AI car (chase/race rival) | C24 |
| `collect` | a collectible to pick up | C14.4 |
| `checker` | a race checkpoint | C16.5 (races) |
| `blueflag` | a race start/flag | C16.5 |
| `bonus` | a bonus mission | C16.5 |
| `camicon` | a camera / view point | C14.6 |
| `harascar` | a harassing car (e.g. the wasp cars) | C25 |
| `dice` | a gambling/wager spot | C15.5 (`SetGamblingOdds`) |
| `dollar` | a shop / purchasable | C16.6 (`forsale`) |

Each icon corresponds to a gameplay system documented elsewhere in the book — the map is a *visual index of
the game's systems*. A player reading the map sees, at a glance, where the missions (`phone`/`mission`), the
races (`checker`/`blueflag`), the shops (`dollar`), the collectibles (`collect`), and the threats
(`harascar`) are.

**Why a fixed icon vocabulary.** A closed set of clear, distinct icons is what makes a map instantly
readable — the player learns 12 symbols and can navigate any level. It also mirrors the game's closed
gameplay vocabularies elsewhere: 20 objective types (C16.3), 12 map icons — SHAR is built from small, fixed
vocabularies recombined, and the map icons are the *navigational* one. Each icon is one PNG, tinted and
positioned per instance (C21.3), so adding a new kind of point of interest is adding an icon to the set.

**The pooling.** Icons are drawn from a fixed pool of sprite slots (`IconPhone0_0…_7`, C29.1), not created
per point of interest. The runtime, each frame, assigns each *currently visible* point of interest to a free
slot, sets that slot's image to the right icon PNG, and positions it at the projected map location (C29.5).
When a point of interest leaves the map (out of range, completed), its slot frees. This bounds the icon count
(you never draw more than the pool size at once) and avoids per-frame allocation — the standard HUD approach.
The pool size limits how many icons show simultaneously, which is why distant points of interest may not
appear until you're closer.

**What happens if you bend it.**

- *Add a point-of-interest type without an icon* — it can't be marked on the map. Add an icon PNG and wire it
  up.
- *Exceed the icon pool* — beyond the pool size, extra points of interest don't draw. Size the pool for the
  busiest case, or prioritise which show.
- *Swap an icon PNG for an unclear image* — the map's legibility drops. Keep icons distinct and simple.
