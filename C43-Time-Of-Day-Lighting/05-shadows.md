# C43.5 — Shadows (`SetShadowAdjustments`)

> The only lighting-related *commands* in the scripts are shadow tweaks — and they are **per
> vehicle / per prop**, not a time-of-day control. Don't confuse them.

## `SetShadowAdjustments` (✅ verified — it's a vehicle setting)
`SetShadowAdjustments( 8 floats )` appears in the **`.con` vehicle scripts** (e.g.
`cars/IStruck.con`, `cars/Missions/level01/M1race.con`, `sr2_1st.con`, …) — the vehicle-handling
config files (C15), *not* the level scripts. It tunes that **vehicle's** blob/projected shadow.
The eight floats vary per car/mission, e.g.:
```
SetShadowAdjustments( -0.1, -0.1, -0.1,  0.0, -0.1,  0.0, -0.1,  0.2 );
SetShadowAdjustments( -1.0,  1.0, -1.0,  0.0, -1.0, -0.35, -0.3, -0.8 );
```
The eight values are 🟡 (exact semantics need disassembly) but read as a small set of
offset/tint/size parameters for the shadow blob under the car. Because they're in the *car*
config, they follow the vehicle between levels — clear evidence they're not a level-time setting.

## `SetStatepropShadow` (✅ verified)
Controls whether/how a **state-prop** (an animated world prop) casts its shadow. Also a per-object
setting, not a global one.

## Why this matters
It's the classic trap: a modder finds `SetShadowAdjustments`, sees "shadow", and assumes it's the
lighting/time-of-day control. It isn't — it's cosmetic per-object shadow tuning. The time of day
is art (C43.1). Keeping these separate prevents a lot of wasted effort.

## What happens if you bend it
Tune a car's shadow (softer/darker/offset) by editing its `.con` `SetShadowAdjustments`; toggle a
prop's shadow with `SetStatepropShadow`. Neither changes the level's light.

## Cross-references
C15 (CON vehicle scripts — where `SetShadowAdjustments` lives), C35 (vehicles), C43.1 (what
actually sets time of day), C33 (real lighting).
