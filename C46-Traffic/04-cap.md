# C46.4 — The Traffic Cap (`SetMaxTraffic`)

> How many traffic cars exist at once, and why missions turn it down.

## The command (✅ verified)
`SetMaxTraffic( N )` sets the maximum concurrent traffic vehicles. The level init sets a base
(e.g. `SetMaxTraffic(4)`); mission and race scripts **lower** it (e.g. `SetMaxTraffic(2)`, and some
set it very low) so background traffic doesn't interfere with a timed race or a chase.

## Why lower it for missions
During a street race or a tailing mission, random traffic is noise — it blocks the road, causes
accidental collisions, and muddies the Hit & Run signal. Turning it down (or off) keeps the mission
readable. Restoring it after keeps the world alive between missions.

## The limit tier
This is the **script tier** of the engine-limit taxonomy (C39.2): a plain number you edit. Raising
it puts more cars on the road — up to what the vehicle/actor pools and the road network can bear
(C39; C46.2). It pairs with the traffic groups (C46.1) which decide *what* spawns, while
`SetMaxTraffic` decides *how many*.

## What happens if you bend it
Raise it for busier roads (mind the pools, C39); lower it for calmer driving. Set it to 0 for empty
streets. A raise with no pool headroom simply won't add cars (measure first, C39.6).

## Cross-references
C39.2 (script-tier limits), C46.1/46.2 (what & where spawns), C16 (missions that lower it), C31 (Hit & Run).
