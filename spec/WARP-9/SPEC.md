# WARP-9: The version

Status: accepted

## Summary

Every document names the language version it is written for. The rules decide that a document without one refuses at the load, that a reader reads only the version it implements and refuses any other, and what makes the number go up.

## Motivation

A document crosses machines as bytes and outlives the reader that wrote it, so a reader handed one has to tell from the bytes alone which rules it was written to. Were `{ warp: 2, … }` read by a reader of version 1, a type the later version reads differently would be read the earlier way and run to another result, and two implementations would answer one document differently with nothing to show that either was wrong. No front end can say this for the reader: the number has to travel in the document.

## Rules

**The version.** Every document says it, and one that does not **refuses at the load**, as not a document rather than as a malformed one. `warp` is an int, and one written as any other value, the Double `1.0` among them, which `equal` takes for `1`, **refuses at the load**.

The current version is **1**. A reader reads the version it implements and **refuses** any other, before judging the document's keys. A document for an earlier version is written again: a document is spelled the way the writer of its version spells it, so one written for another version is another text. The number goes up when anything portable changes what an existing program *means*: a type the language names added, a type read differently, a checking rule moved, a standard procedure returning differently. It does not move when a procedure is *added*. Nor does it move when a kind of declaration is added, as an [enum](../WARP-93/SPEC.md) is under version 1: a name the language takes can change what an existing document's own declaration under that name means, and a new kind of declaration cannot, so every existing document means what it meant.

An implementation implements the **current** version only.

**Note.** A reader that filled in a missing version would be deciding, on the sender's behalf, the one question that has to be decided from the bytes alone, and a file of some other kind would get as far as having its keys judged. A later version may add keys, and checking the keys first would turn "I am too old for this" into "this is malformed". A key added under the same version costs that: a document writing a key an older reader does not know, an enum's `enum` among them, is refused by that reader as malformed rather than as too new. A document written for another version is refused as that, rather than read by rules it was not written to and run to a different result.

**Note.** That a reader judges the version before the keys is held by no case: a document of another version and one writing a key no reader knows both refuse at the load, and a case holds the stage, not which reason was given.

**Note.** A procedure the language adds changes nothing for a document that neither sends nor declares its spelling, and spellings under `Standard.` are not reserved. A document that declares a spelling the language later takes breaks at the build in the edition that takes it, where two declarers of one spelling refuse under [what the build decides](../WARP-66/SPEC.md), and that is its author's cost, as it is in Swift, whose standard library adds declarations without a new language version.

## Interactions

- The case format says its own number, `test`, for the same reason and on its own schedule: [WARP-1](../WARP-1/SPEC.md).
- The binary's format version is another number, how the bytes are laid out: [WARP-5](../WARP-5/SPEC.md).
- The text is laid out by the version the tree says it is in: [WARP-37](../WARP-37/SPEC.md).

## Alternatives considered

## Notes
