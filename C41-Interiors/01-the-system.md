# C41.1 — The Interior System

> Interiors are separate on-foot spaces (shops, houses, landmarks) you enter from the street.
> They're managed by a small set of confirmed classes.

## The classes (✅ verified vtables)
| Class | VA | Role |
|---|---|---|
| `InteriorManager` | `0x00613C48` | owns the active interior; performs the world↔interior swap |
| `InteriorEntranceLocator` | `0x006070D4` | a world locator marking an entrance (and which interior) |
| `InteriorExit` | `0x00613C54` | the way back out |
| `ActionButton::EnterInterior` | `0x0061723C` | the context action offered at an entrance |
| `InteriorObjective` | `0x006115E8` | mission objective: be inside a named interior |
| `LeaveInteriorCondition` | `0x00611348` | mission condition: leave the interior |

## How it works
Interiors aren't a live streamed part of the open world — they're a **swap**. When you enter,
`InteriorManager` hides the exterior world and brings up the interior space (its geometry,
lighting, gags, and ambient NPCs), placing you at the interior's origin. When you leave, it
reverses the swap and returns you to the street at the exit locator.

## Why a swap, not seamless
The exterior and interior are different, non-overlapping spaces at (often) the same or reused
world coordinates. Swapping keeps only one resident at a time (memory), lets each have its own
lighting/ambience, and gives a clean point to gate input and play the transition. This is why
the enter/exit is wrapped by the C40 black-box fade — it hides the swap.

## What happens if you bend it
Hooking `InteriorManager` lets you observe or alter the swap (e.g. keep the exterior loaded,
change the destination). Moving an `InteriorEntranceLocator` relocates a doorway.

## Cross-references
C40 (the fade that hides the swap), C8 (locators), C41.2 (the enter/leave flow), C33 (lighting).
