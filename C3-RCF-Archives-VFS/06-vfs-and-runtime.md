# C3.6 — The Virtual File System at Runtime

**What it is.** The layer that lets the game ask for `art\cars\ambul.p3d` without knowing or caring
whether that file is loose on disk or packed inside an `.rcf`. Loose trees and archives resolve into one
**virtual file system** (VFS) with a single path namespace.

**How it works.** A file request (typically an `.mfk` `LoadP3DFile("art\…")`, Chapter 14) is resolved by
the VFS against its mounted sources. Each source — the loose `art/` tree, each `.rcf` archive — can
answer a path. The resolver normalises the path, and for archive sources hashes it (C2.2) and
binary-searches the directory (C3.2); for the loose tree it is an ordinary filesystem open. The first
source that has the path wins, and its bytes are handed to the loader (C1.8).

**Why it's built this way.** One namespace over many backings is what lets the same game code run
whether an asset was shipped loose or packed, and whether it was patched later or not. It decouples "what
asset do I want" (a path) from "where does it physically live" (loose vs. archive, this disc vs. that) —
the classic reason every shipping engine has a VFS rather than raw `fopen` calls scattered through the
code.

**Resolution order and shadowing (🟡 reasoned, exploited in practice).** Because multiple sources can
answer a path, there is a precedence: a loose file can **shadow** a packed one when the loose tree is
consulted first (or mounted with higher priority). This is the mechanism behind essentially all SHAR
loose-file modding — and behind Lucas' Mod Launcher (Chapter 28): you don't have to rebuild a 228 MB
archive to change one asset; you drop a replacement into the loose path the VFS checks first, and it wins.
The exact precedence is a property of how the retail build mounts its sources; treat "loose shadows
packed" as the reliable working rule and confirm for a specific asset by testing.

**The modding consequence, concretely.** To replace a packed sound or a packed script you have two
routes: rebuild the archive (C3.4 — heavy, exact, permanent) or shadow it with a loose file (light,
reversible, launcher-friendly). To replace loose art you simply overwrite or shadow the `.p3d`. This is
why Chapter 3 sits in the foundations: understanding that the game addresses everything through one
hashed namespace tells you *where* an edit has to go and *which* of the two routes is appropriate.

**Runtime residency.** The VFS resolves a path to bytes; the loader (C1.8) turns bytes into objects; and
a higher layer decides *when* to load and *when* to free — level transitions load a level's assets and
release the previous level's. The classes that own that lifetime (streaming and resource managers) are
part of the runtime model in Part VII; here it is enough to know that an asset's *identity* is its path,
resolved through the VFS, regardless of which of the ten archives or the loose tree ultimately provides
it.

**What happens if you bend it.**

- *Edit a packed file in place inside a giant archive without the size discipline of C3.4* and you
  corrupt the directory or overlap members. Prefer the loose-shadow route when you can.
- *Assume your loose file will always shadow the packed one* without confirming precedence for that asset
  class — verify by testing; if the packed source wins for a given path, you must repack.
- *Rely on a path that differs only in case or slashes from what the game requests* — the VFS normalises
  before hashing, so match its normalisation or your replacement is never consulted.

**Next:** [Chapter 4 — Byte-Level Toolcraft](../C4-Byte-Level-Toolcraft/C4-Byte-Level-Toolcraft.md).
