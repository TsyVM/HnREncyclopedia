# C49.4 — The Manager Catalogue

> All **43 confirmed managers**, by domain, with what each owns/does. Addresses are retail
> `Simpsons.exe` (`0x00400000` base). Machine-readable: `RE-Data-And-Discoveries/data/managers.json`
> and `DonutsSDK/data/managers.csv`.

The full seven-domain table is in the chapter hub — [C49 §49.4](C49-The-Manager-Layer.md#494-the-catalogue--all-43-managers-verified).
This page adds the *reading* of it.

## How to read the catalogue
- **Domain** tells you which frame phase the manager ticks in (input → gameplay → physics → render →
  audio) and which chapter explains its subsystem in depth.
- **VA** is the vtable address — the key for identifying the live singleton (C28.7) and for a VTable
  hook (C49.5).
- **What it does** is the one-line owner/driver summary (C49.1).

## The seven domains at a glance
| Domain | Count | Ticks around | Deep chapters |
|---|--:|---|---|
| World & AI | 7 | gameplay | C25, C45, C46, C47, C44 |
| Navigation & World | 4 | gameplay/physics | C13, C41, C32 |
| Gameplay & Mission | 10 | gameplay | C16, C30, C31, C32, C27 |
| Rendering & UI | 5 | render/present | C33, C38, C21, C40 |
| Audio | 6 | audio | C18, C19 |
| Physics & Collision | 3 | physics | C11, C35 |
| Engine & Resource | 8 | early/late | C1, C30, C37, C39, C27 |

## The ones people ask about
- **`ChaseManager`** (`0x006077FC`) — the police pursuit ("the chaos"). Owns the cop chase state
  and cars; armed by `CreateChaseManager` in level init (C44.5/C31).
- **`PedestrianManager`** (`0x006078A8`) — owns the wandering crowd (C45).
- **`RoadManager`** (`0x0060B6D0`) — owns the road network traffic drives on (C13/C46); caught live
  in the diagnostic capture.
- **`PathManager`** (`0x006072A8`) — the AI navigation path graph (C13); also caught live.
- **`HitnRunManager`** (`0x00608D3C`) — the Hit & Run meter (C31).

## No `ChaosManager`
There is no class named `ChaosManager`. The manager that produces the chaos of a police chase is
**`ChaseManager`**. (Easy to mis-remember — the chaos *is* the chase.)

## Cross-references
The hub table (all 43), `managers.json`/`managers.csv`, and each domain's chapter (linked in the
table). C49.5 (hooking any of these).
