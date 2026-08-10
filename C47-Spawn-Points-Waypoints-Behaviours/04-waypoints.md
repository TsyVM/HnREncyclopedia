# C47.4 — Waypoints & Routes

> Waypoints & Routes — grounded in the verified level-script vocabulary.

AddAmbientNPCWaypoint(actor, waypoint) links an NPC to ordered waypoint locators forming a route the NPC walks; 55 links build level 1's ambient foot-traffic. Named characters (C45.3) and crowd peds alike can be routed. Why: authored routes make NPCs look purposeful and keep them where the designer wants (out of the road, around a plaza) far more cheaply than pathfinding from scratch. Bend it: add waypoints to route an NPC along a custom path; combine with AddAmbientCharacter (C45).

## Cross-references
C8 (locators), C31 (wasps), C42/C25 (behaviours/AI), C45 (peds), C44 (level init), C39.4 (loading), C28 (modding).
