# WARP-92: What a reading refuses

Status: accepted

## Summary

A reading refuses what it cannot read and traps on nothing. The rules decide which layout violations and which layouts the language cannot stand on a reading refuses, such as bad numbering, frames, slots and self-referring types.

## Motivation

An object comes off a disk, a cache or a wire into a host's process, so what a reading does with one that is malformed has to be decided before any number in it is used, or one bad object could end the host.

## Rules

A reading refuses what it cannot read and traps on nothing: the reading runs inside a host's process, and a trap there ends the host. What a reading asks is closed: **every number a reading would index, count or allocate with stands inside what the object numbers there**, and a number standing past it, or at another kind of thing than the one its place reaches, **refuses**. What refuses is the layout: every form [WARP-85](../WARP-85/SPEC.md) to [WARP-91](../WARP-91/SPEC.md), [enums](../WARP-93/SPEC.md#in-the-binary-and-in-an-object) and [a switch](../WARP-95/SPEC.md#in-the-binary-and-in-an-object) give an object's parts, an enum's cases at least one, a switch's arms and binds in name order, a lowered procedure type's fields and a native procedure's sends one to a place among them; and what a layout admits but the language cannot stand on, where one field stands against another:

- a lifted row where the numbering counts no closure, a numbering counting more closures than `lifted` holds, and counts that add up past what an int holds
- a frame naming other than one name per slot, standing other than one slot per parameter its declaration takes, or standing a parameter, a variable, a constant or a capture past its end
- a body standing on a slot past its frame, a switch's bound slot among them, or on a variable past its document's `variables`
- a call or a closure literal numbering past the sends, rows and closures the numbering counts, or a closure literal numbering anything but a closure
- a call handing in place at other positions than the ones it writes nothing at
- a call through a contract writing other than one lowered type per position it stands an argument at
- a closure literal taking what it captured into slots other than the captures of its own row's frame
- a lowered type standing on a place past `typeNumbering`
- a declared type that is no struct and no enum and comes back to itself through what it stands for, which the load refuses in a document, under [types](../WARP-50/SPEC.md)
- a struct built from parts holding other than one part per field its layout names
- a row of a native procedure whose sends reach a spelling the document's `numbering` does not number
- an object standing against a document other than the one it was kept under

Every one of these is refused where the object is read, before it is laid beside anything. What only the documents beside it can decide is refused at `build`, where a compile lays the object down or a link does, under [checking](../WARP-66/SPEC.md): whether every object under its `dependencies` is beside it, which row a number is and whether a call stands as many arguments as that row takes and hands one type per type parameter and associated type its signature names, which type conforms to a contract, and whether it stands after every document it names, so two objects that need each other refuse as two documents do. A type its declarations, signatures and bodies name is the declaration its compile read, which its `dependencies` say is beside it, and a build does not ask that again.

The names an object writes are the ones its document wrote, and each held the grammar of where it is written when that document was loaded, under [names and their grammar](../WARP-67/SPEC.md): a type's, a contract's, a claim's, a member's, a failure's, a bound's and a part joined with `&` alike. An object is what a build wrote, so a reading asks those names no grammar again, only what a *name* is under [how a part is laid out](../WARP-86/SPEC.md), and what a name stands for beside the documents is the link's to say, for an object as for a document.

What a build judged, an object writes down as judged: what a signature says, `returns`, `failing`, `const` and `isolated`, and the type every reading in a body was judged to be. A reading, a link and a run take each of those as written and judge none of them again. A body is held to its declaration once, by the compile of its document, under [checking](../WARP-66/SPEC.md). An object a reading admits and no build would write, a body returning what its declaration does not take or calling what is no procedure, is one this specification gives no meaning to, save one: a run of it **traps on nothing**, for the reason a reading does not, and where it stops, it stops by refusing the run. Whether an object handed over is the one a build wrote is the transport's to say, by whatever seals what it carries. Nothing an object writes proves it, so a reading does not ask.

## Interactions

- An object standing against another document is told by [identity and dependencies](../WARP-91/SPEC.md), and a run that stops refuses as [a refusal](../WARP-72/SPEC.md) does.

## Alternatives considered

- A verifier that checks what an object means, as a platform does that runs code from strangers. An object is what a build of the same language wrote, read back from a cache, and a document a server sends is built where it runs, which is its check.

## Notes

**Note.** What a reading asks is closed, so an implementation can count the places it asks at. Asking whether an object was forged has no such end, and that question is the transport's.

**Note.** An object a reading admits and no build would write has no meaning here beyond that its run traps on nothing, so a case expecting how such a run stops would hold an implementation to more than this says, and that rule is held only by tests inside the implementation.
