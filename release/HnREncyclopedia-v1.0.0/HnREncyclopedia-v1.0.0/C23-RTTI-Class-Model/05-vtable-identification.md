# C23.5 — Identifying a Class by its VTable

**What it is.** The technique for recognising *which class* a live object is, from nothing but a pointer to
it. It is how a runtime mod (DonutsSDK) turns an anonymous address into "this is a `Vehicle`" — and it is why
class *identity* is usable today even while member *offsets* stay ⏳.

**How it works.** Every polymorphic C++ object begins with a hidden pointer to its class's **virtual method
table** (vtable). All instances of one class share the same vtable, so the vtable pointer is a reliable
class fingerprint:

```
object ──► [ vtable ptr | member data … ]
              │
              ▼
           vtable ──► [ &method0, &method1, … ]   (one table per class)
```

To identify an object: read its first pointer (the vtable), and match it against a table of known
class-vtable addresses. If it matches `Vehicle`'s vtable, the object is a `Vehicle` (or a subclass — subclass
vtables are distinct but their layout is compatible). DonutsSDK's runtime does exactly this: `shar::identify(obj)`
reads the vtable and returns the `ClassInfo` from the verified DB (C23.6).

**Why this works when offsets don't.** RTTI proves the class hierarchy (C23.1), and the vtable pointer is a
*structural* feature of every polymorphic object — its presence and position (offset 0) are guaranteed by the
C++ ABI, not by any reverse-engineered offset. So identifying a class needs only the vtable *address* (a
constant you can recover once by disassembly or by RTTI's complete-object-locator), not the object's internal
layout. That is why the book can say with confidence "this becomes a `Vehicle`" while marking the byte where
the vehicle's speed lives as ⏳: identity is structural, member layout is not.

**The current state (✅ mechanism / ⏳ addresses).** The *mechanism* is solid and implemented in the SDK. The
*per-class vtable addresses* are the ⏳ part in this data set — the RTTI gives class names and inheritance, and
the complete-object-locator ties a vtable to a class, but the SDK's tables mark vtable addresses that haven't
been pinned as `0`/TODO. Recovering them is a mechanical disassembly task (walk the RTTI complete-object
-locators), and each recovered address promotes one class from "named" to "identifiable at a known address."

**Using identity without offsets.** Even with offsets ⏳, class identity alone is powerful: a mod can walk a
list of objects, identify each by vtable, and act only on `Vehicle`s or only on `Character`s — filtering by
type without knowing any member layout. Combined with a *user-supplied* offset (from their own diff, C4.3),
that becomes "for every `Vehicle`, write offset 0x1A4" — safe, because the type check is verified and the
offset is the user's own, clearly marked.

**What happens if you bend it.**

- *Match on a member value instead of the vtable* — fragile and ambiguous. The vtable pointer is the reliable
  fingerprint; use it.
- *Assume a matched vtable means an exact class, not a subclass* — subclasses have their own vtables but pass
  "is-a" checks. Decide whether you want exact-type or is-a matching.
- *Trust a vtable address you didn't verify for your build* — addresses shift between builds. Recover them
  from your own `.exe`.
