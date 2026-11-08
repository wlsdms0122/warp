# WARP-4: When two values are the same

Status: accepted

## Summary

Sameness is what Standard.Logic.equal decides. The rules say when an Int and a Double, bytes and an array, and arrays, dictionaries and structs are the same value, so that a spelling takes no part in it. A String is counted and compared by extended grapheme cluster under Unicode canonical equivalence.

## Motivation

Left to a platform, `(call Standard.Logic.equal 1 1.0)` would answer by whether the platform compares numbers by kind, and `"é"` written as one scalar and as a letter with a combining mark would be equal in one host language and unequal in another.

## Rules

**When two values are the same**, which is what `Standard.Logic.equal` decides:

- An `Int` and a `Double` of the same worth are the same value. Numbers are compared by what they are worth, not by which of the two they are, and exactly, at **every** size: `9007199254740993` (2^53 + 1) is not equal to `9007199254740992.0`, however binary64 would round it. Ordering compares two of one type, under [Standard](../WARP-77/SPEC.md).
- A run holds no `Double` without a finite value. No document and no encoding writes one, and a door a host hands one through **refuses at the run**, a return value of the standard vocabulary's arithmetic among them, under [doors](../WARP-71/SPEC.md).
- Bytes are an array spelled compactly, so they are the same as an array of the same integers in the same order: `x"6869"` and `(array 104 105)` are one value, and `equal` says so. Bytes are not a `String`: no encoding is assumed, so no Unicode rule applies. Which spelling a value wears takes no part in sameness.
- Arrays are the same when their elements are, in order.
- Dictionaries are the same when they hold the same keys bound to the same values. Structs are the same when they hold the same name and the same field names bound to the same values. A struct has no order, so order takes no part in sameness; the name is part of what a struct holds, so an `Account` and a `Vault` with the same fields are two values, and a dictionary is never the same as a struct.
- Null is the same as null.
- A procedure is the same as no value, itself included, and so is a collection holding one.
- **A `String` is counted and compared as a person reads it**: by extended grapheme cluster, under Unicode canonical equivalence. A letter written as a letter and the same letter written as letter-plus-combining-mark are one character and are equal; `"é"` is `"é"` whichever way its bytes spell it, and its `count` is 1. An implementation whose platform strings compare by code unit must not expose that comparison here.

**Note.** The string decision is cheap in Swift and dear elsewhere. Grapheme-cluster counting and canonical equivalence come with the platform in Swift and are a library obligation in most other languages; the decision stands, and the cost lands on implementations unevenly.

**Note.** A `Double` with no finite value reaches a door from the standard vocabulary's arithmetic, which cases hold, and from a host's own procedure, and what a case's vocabulary returns is written in a document's spelling, which has none, so the door refusing one a host's procedure returns is held only by tests inside the implementation.

**Note.** Which scalars make one extended grapheme cluster, and which spellings are canonically equivalent, Unicode's tables decide, and which version of the tables an implementation reads is its base language's. The rule promises the reading and not a version, so a cluster Unicode drew differently in two versions can count differently on two implementations, and no case holds one.

**Note.** Two equivalences coexist, and the border is drawn. Values compare as a person reads. `equal`, `contains`, ordering and `count` all read strings under canonical equivalence, stated under the value model. Names are matched as bytes and held to NFC at `load`, so a document cannot declare `é` one way and reference it the other. What remains here is only the cost: an implementation whose platform compares by code unit owes a library the difference.

## Interactions

- Keys that are the same value are one key: [WARP-3](../WARP-3/SPEC.md).
- An encoding keeps `1` and `1.0` apart, and they are still one value: [WARP-5](../WARP-5/SPEC.md).
- A conformance case matches by kind and spelling, which is stricter than sameness: [WARP-1](../WARP-1/SPEC.md).

## Alternatives considered

## Notes
