# The value model

What a value is, and when two of them are one. Nothing on this page needs a program: a value is what a document carries, what a slot judges, what an encoding writes and what a case compares, so every other page reads this one and this one reads none of them.

A program computes over eight kinds of data, plus one value that is not data:

| kind | writes as | notes |
|---|---|---|
| null | `null` | |
| bool | `true` / `false` | |
| int | `1`, `-3` | signed, 64-bit; overflow **refuses**, it does not wrap |
| double | `1.0`, `1e2` | IEEE-754 binary64; a document cannot carry infinity or NaN |
| string | `"hi"` | Unicode text |
| bytes | `x"6869"` | `Array<Int>` in a compact spelling, each element from 0 to 255; what a carrying form carries when the payload is not text |
| array | `[ … ]` | ordered |
| record | `{ … }`, or `Name { … }` | unordered fields, names unique; may carry the **name** of a declared record type |
| procedure | | code with what it captured; exists only at run time, never in a document |

**A record's name.** A record made by a literal, answered by a native procedure or read from a document has no name. It takes one where it is written into a declared type whose structure is a record: a literal written where the type is read, a value from outside at the door it comes through, and a cast to the type. From then on it carries that name through every slot declaring the type and through `Any`, and fits no other: an inline record type and `Dictionary<T>` take no named record, under [Types](type.md).

**When two values are the same:**

- A whole number and a fraction of the same worth are the same value. Numbers are compared by what they are worth, not by which of the two they are, and exactly, at **every** size: `9007199254740993` (2^53 + 1) is neither equal to nor below `9007199254740992.0`, however binary64 would round it, and ordering and `sorted` read the same worth equality does.
- A fraction that is not a number is not equal to itself. There is one such value, no way to write it down, and the standard vocabulary never answers one. Arithmetic with no finite answer refuses instead, so it arises only from a host's own procedure.
- Bytes are the same when their bytes are, in order. Bytes are not text: no encoding is assumed, so no Unicode rule applies. Beside an **array**, worth unifies the way it does across numeric width: `x"6869"` and `[104, 105]` are worth the same. One collection of the same whole numbers in the same order, spelled two ways, and `equal` says so. Which spelling a value wears takes no part in sameness.
- Arrays are the same when their elements are, in order.
- Records are the same when they hold the same field names bound to the same values and the same type name, or none. A record has no order, so order is not part of the answer; the name is part of what a record holds, so an `Account` and a `Vault` with the same fields are two values.
- Null is the same as null.
- A procedure is the same as no value, itself included, and so is a collection holding one.
- **Text is counted and compared as a person reads it**: by extended grapheme cluster, under Unicode canonical equivalence. A letter written as a letter and the same letter written as letter-plus-combining-mark are one character and are equal; `"é"` is `"é"` whichever way its bytes spell it, and its `count` is 1. An implementation whose platform strings compare by code unit must not expose that comparison here.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-procedure-is-the-same-as-no-value`
- `a-whole-and-a-fraction-meet-exactly`
- `a-whole-fraction-stays-a-fraction`
- `arrays-in-another-order-are-two-values`
- `bytes-and-an-array-share-their-worth`
- `null-is-the-same-as-null`
- `two-names-of-one-structure-are-two-values`
- `two-spellings-of-one-text-are-one-value`
- `values-are-the-same-by-what-they-hold`
