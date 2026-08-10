# C46.5 — Traffic & Hit & Run

> Traffic is both the thing you dodge and the thing you smash — and smashing it has consequences.

## The interaction (✅ verified — C31)
Driving recklessly through traffic — ramming cars, causing pile-ups — is exactly the kind of chaos
that feeds the **Hit & Run** meter (C31). Fill it and the police escalate (`ChaseManager`,
`SetNumChaseCars`), spawning cop cars that pursue you through the same traffic. Stop offending and
the meter decays (`SetHitAndRunDecay`, set in init, C44.5).

## Why traffic matters to the loop
Traffic gives the open world friction: it's the obstacle course you weave through, the collateral
that raises heat, and the cover/hazard during a chase. Without it the streets would be a sterile
racetrack. It's a core part of what makes "Hit & Run" the game's signature meter.

## Traffic as target
Some gags and destructive fun involve traffic (smashing specific vehicles). Traffic vehicles are
breakable/collidable like other props (C11/C32), and count toward the mayhem the meter tracks.

## What happens if you bend it
More traffic (C46.4) = more collateral = faster Hit & Run buildup; less traffic = calmer. Tuning
`SetHitAndRunDecay` (C44.5) changes how forgiving the meter is.

## Cross-references
C31 (Hit & Run meter & police), C46.4 (traffic cap), C44.5 (decay setup), C11/C32 (collision/destruction).
