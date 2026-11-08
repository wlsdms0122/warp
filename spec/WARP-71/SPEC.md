# WARP-71: Doors

Status: accepted

## Summary

A door is where a value crosses between the host or a call and a slot. The rules decide how a return value is held to its returns, how a value arriving from the host is judged, and what is judged at the build and what at the run.

## Motivation

Judged only where the value is handed back, a body declaring `(returns Int)` that returns an `Int?` on one path would run to its end, after its host calls had done their work, and refuse at the last step.

## Rules

- A procedure's return value is held to its `returns`, `Null` where it writes none. A body and the declaration beside it are one document's text, so what the body reads is judged at the **build**: a reading the declaration does not take refuses there. Calling a value returns what the procedure type of the slot holding it writes after `->`, and that return value is held the same way. A reading the text opens to `Any` stands where *what a slot takes, exactly* in [types](../WARP-48/SPEC.md) says a value read as `Any` does. Where a call reads a return value narrower than its callee declares (a type parameter the call filled, the return type a value's slot wrote, the return type a contract wrote for a row the run picks), the build held what the body returns to it, so the call reads what arrives as it is. What a value standing in a procedure-typed slot may return is held under *what a slot takes, exactly* in [types](../WARP-48/SPEC.md). A call hands its return value on as it came, and the place it stands in reads it without remaking it. A variable the call hands in place is held the same way. A body cannot leak a value its declaration did not admit. What a native procedure hands back, and what it writes through a parameter handed in place, is a value from outside, as are the entry's arguments, what a host hands a closure, what a native procedure sends, and the failure a catch binds, whose `details` the failing procedure filled: each comes through a door, where every struct it holds, in a key as in a value, is fitted to the struct, or the case, its name declares, under *a declared struct is nominal* in [types](../WARP-49/SPEC.md) and [enums](../WARP-94/SPEC.md), and the value is judged against its slot's type, and a value that does not fit, or that holds a `Double` with no finite value, which no document carries, **refuses at the run** there. A native procedure is called by the run and what it hands back comes back into it, so a value there that holds the type it was read as keeps that type, under *a value read as a contract holds the type it was read as* in [types](../WARP-53/SPEC.md). The entry's arguments and a send are a call of the declaration they reach, so the door judges them the way the build judges a call's readings: what they read as once fitted fills the type parameters their slots name, and a parameter filled by two types, or a bounded one filled by what does not conform to its bounds, **refuses at the run**. A call of a native procedure fills its type parameters as any call does, and the run holds what filled them, under [type parameters](../WARP-51/SPEC.md), so what the procedure hands back at a type parameter is judged at the door against what its call filled there: `App.h` returning `some T`, called with `5`, that hands back a string **refuses at the run**. Where the call that made a closure filled a type parameter, a value a host hands the closure there is held to the bounds alone and taken at its host's word. A closure literal writes a signature and a body side by side too, and is held the same way where it is written.

## Interactions

- What a native procedure hands back and sends is held under [a native procedure](../WARP-14/SPEC.md), and the entry's arguments under [where a run starts](../WARP-69/SPEC.md).

## Alternatives considered

## Notes

**Note.** No document carries a `Double` with no finite value, and neither does a case, so no case hands one to a door, and the refusal of one is held only by tests inside the implementation.
