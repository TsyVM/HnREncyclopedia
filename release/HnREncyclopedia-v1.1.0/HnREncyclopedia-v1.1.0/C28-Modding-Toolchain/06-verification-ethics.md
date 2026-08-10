# C28.6 — Verification & Ethics

**What it is.** The discipline that separates safe, honest mods from crashes and cheating — and it's the same
discipline that runs through this whole book. This closing page distils it into rules, drawn from the shipped
tooling and the SDK's own stance.

**Rule 1: Re-verify addresses against your own executable.** Vtable addresses, member offsets, and singleton
pointers (⏳, C23.1) are properties of a *specific build*. A different exe version, a different patch, a
recompile — any of these shifts addresses. The shipped `NoTrafficDiag` mod says this in its own log — *"Re
-verify these VAs against your own exe before trusting them"* — and it's the first rule of native modding
(C28.4). An address that worked in one build is a guess in another until re-checked. This is why the book
marks every offset ⏳ and the SDK takes offsets as user-supplied (C28.5): no address is portable across
builds.

**Rule 2: Read before you write; prefer reversible.** The safest native mod reads and never writes —
`NoTrafficDiag` is exactly this (a read-only vtable watch, C28.4), and it *cannot* crash the game because it
only observes. When you must write, prefer **reversible** edits: DonutsSDK's RAII patches (C28.5) and loose
-file shadowing (C28.2) both undo cleanly. Permanent, blind writes are the last resort. The progression is:
read-only → reversible write → permanent write, and you climb it only as far as the task demands.

**Rule 3: Verify by two independent methods where you can.** The book's strongest findings come from
*convergence* — the 20 script objective types matching the 21 RTTI classes (C26.2), the `.con` values (C15)
matched to live members by diffing (C4.3/C24.4). A single method can mislead; two agreeing is confidence.
For a recovered offset, verify it *both* by diffing the file *and* by watching the live value (C24.4). For a
class, name it from RTTI (✅) and confirm its behaviour matches. This is the C4.4 confidence ladder applied to
modding.

**Rule 4: Single-player only — no online cheating.** SHAR has a multiplayer mode, and the ethical line — the
one the DonutsSDK enforces in its own guidance — is **single-player/offline only**. Modding your own
offline game (handling, content, cosmetics, tools) is the craft this book supports; using the same techniques
to cheat other players online is not. Keep mods to the single-player experience.

**Rule 5: Non-destructive by default.** Loose-file shadowing (C28.2) never touches the packed originals; mod
folders are toggleable; reversible patches undo. Prefer techniques that leave the game recoverable — a user
should be able to disable your mod and get a clean game back. This is why the whole toolchain favours
shadowing over repacking and reversible over permanent.

**Why the discipline is the point.** A reverse-engineering-based mod is only as good as its verification.
The difference between a mod that works and one that corrupts saves or crashes on the next patch is exactly
these rules: verified addresses, read-first, converging evidence, reversibility. They're the same rules that
make the book trustworthy (✅/🟡/⏳, two evidence bases, C4.5) — because a mod *is* applied reverse
engineering, and the discipline that makes RE honest makes mods safe.

**The whole toolchain, in one line.** Start at the highest layer that works (C28.1); package loose-file mods
in folders (C28.2); script with Lua through the Mod Launcher (C28.3); go native via ASI/DonutsSDK only when
needed (C28.4–C28.5); and at every native step, **re-verify per build, read before you write, converge your
evidence, stay single-player, and keep it reversible**. That's the craft.

**Next:** [Chapter 6 — Shaders & Materials](../C6-Shaders-Materials/C6-Shaders-Materials.md), or the [chapter map](../README.md#chapters).
