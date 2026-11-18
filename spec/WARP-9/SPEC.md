# WARP-9: The version

Status: accepted
Release: 0.1

## Summary

Every document names the version it is written for: the major and the minor of the release of this specification it was written to. The rules decide that a document without one refuses at the load, which documents a reader reads and that it refuses the rest, and what moves each number.

## Motivation

A document crosses machines as bytes and outlives the reader that wrote it, so a reader handed one has to tell from the bytes alone which rules it was written to. Were `{ warp: "2.0", … }` read by a reader of `1.4`, a type the later release reads differently would be read the earlier way and run to another result, and two implementations would answer one document differently with nothing to show that either was wrong. No front end can say this for the reader: the number has to travel in the document.

The number is the release's, so a document, the specification it was written to and the implementation reading it name one thing. Past major 0 a release adds without changing what a document already says, and a reader of the later release reads the earlier documents of its major as they were written. The patch number is left out, since what a patch moves is nothing a document can say.

## Rules

**The version.** Every document says it, and one that does not **refuses at the load**, as not a document rather than as a malformed one. `warp` is a string, `"<major>.<minor>"`, each part an int in decimal digits with no sign and no leading zero, `0` written as itself. One written as any other value **refuses at the load**: the Double `0.1`, the Int `1`, and a string of another form, `"0.1.0"`, `"v0.1"` and `"0.01"` among them.

**What moves each number.** This specification is released as `<major>.<minor>.<patch>`, and a document writes the major and the minor of the release it is written for.

- The **major** goes up when anything portable changes what an existing program *means*: a type the language names added, a type read differently, a checking rule moved, a standard procedure returning differently.
- The **minor** goes up when the language adds and every existing document means what it meant: a procedure, a key, a kind of declaration, as an [enum](../WARP-93/SPEC.md) is. A name the language takes can change what an existing document's own declaration under that name means, and a new kind of declaration cannot.
- The **patch** goes up when the text or the cases are supplemented and no case's answer moves. A document does not write it.
- While the major is **0**, the language is not settled, and the minor goes up for any change, one that changes what a program means among them. A document of an earlier minor is still read, by the later release's rules, and where those changed what it says it runs to what the later release says.

**What a reader reads.** A reader implements one release. It reads a document whose major is the release's and whose minor is no later than the release's, and it **refuses** any other, before judging the document's keys. A document for another major is written again: a document is spelled the way the writer of its version spells it, so one written for another major is another text.

The current release is **0.1.0**, and a document written to it says `"0.1"`.

**Note.** A reader that filled in a missing version would be deciding, on the sender's behalf, the one question that has to be decided from the bytes alone, and a file of some other kind would get as far as having its keys judged. A later release may add keys, and checking the keys first would turn "I am too old for this" into "this is malformed". A document writing a key a release added says that release's minor, and an earlier reader refuses it as too new. A document written for a version a reader does not read is refused as that, rather than read by rules it was not written to and run to a different result.

**Note.** That a reader judges the version before the keys is held by no case: a document of another version and one writing a key no reader knows both refuse at the load, and a case holds the stage, not which reason was given.

**Note.** The minor a document says is the earliest release it asks for, and a reader does not hold each name the document uses to the release that added it. A document sending a procedure a later minor added while saying an earlier one is read, and refused at the build where the procedure is sent, as any procedure no module declares is.

**Note.** A procedure the language adds changes nothing for a document that neither sends nor declares its spelling, and spellings under `Standard.` are not reserved. A document that declares a spelling the language later takes breaks at the build in the release that takes it, where two declarers of one spelling refuse under [what the build decides](../WARP-66/SPEC.md), and that is its author's cost, as it is in Swift, whose standard library adds declarations within a language version.

## Interactions

- An interface says its version under `interface` by the same rules: [WARP-43](../WARP-43/SPEC.md).
- The case format says its own number, `test`, for the same reason and on its own schedule: [WARP-1](../WARP-1/SPEC.md).
- The binary's format version is another number, how the bytes are laid out: [WARP-5](../WARP-5/SPEC.md).
- The text is laid out by the version the tree says it is in: [WARP-37](../WARP-37/SPEC.md).
- A runtime conforms to the release it pins: [the series](../README.md).

## Alternatives considered

- The whole release number in the document, the patch included. Every supplement would make every document another version though nothing it says moved.
- Under major 0, a reader reading its own minor alone. Every release would write every document again, every case of the series among them, to keep a promise major 0 does not make.
- A number of its own, counting only the changes of meaning. A reader could not tell a document using what a later release added from one that does not, and the number a document says would stand apart from the release an implementation pins.

## Notes
