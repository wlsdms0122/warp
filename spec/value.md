# The value model

What a value is, and when two of them are one. Nothing on this page needs a program: a value is what a document carries, what a slot judges and what an encoding writes, so every other page reads this one and this one reads none of them.

A program computes over eight kinds of data, plus one value that is not data:

| kind | writes as | notes |
|---|---|---|
| null | `null` | |
| bool | `true` / `false` | |
| int | `1`, `-3` | signed, 64-bit; overflow **refuses**, it does not wrap |
| double | `1.0`, `1e2` | IEEE-754 binary64; a document cannot carry infinity or NaN |
| string | `"hi"` | Unicode text |
| array | `[ … ]`, or `x"6869"` | ordered; `x"…"` is **bytes**, the compact spelling of an `Array<Int>` whose every element is from 0 to 255, what a carrying form carries when the payload is not text |
| map | `{ … }` | entries, each a value under a key that is a value, every key once; held in the key order below |
| struct | `Name { … }` | unordered fields, names unique; carries the **name** of the declared struct it is, a type's name under [checking](checking.md) or one the language declares, which a slot of a declared struct takes only where it is that struct's |
| procedure | | code with what it captured; exists only at run time, never in a document |

**A struct's name.** Every struct is a value of a declared struct and carries its name. A struct literal is read as the declared struct of the place it is written into and takes that name there, and a literal a program writes with one (`Ghost.T { x 1 }` in a text) **refuses at the load**. A struct carries its name through every slot declaring the type and through `Any`, and fits no other: `Dictionary<String, T>` takes no struct, and a declared struct takes no map, under [Types](type.md). A value from outside under a name, through `Any` included, is held at the door to the struct the name declares, under *a declared struct is nominal* in [Types](type.md).

**A map's keys.** A key is a value, and a map holds each key once, by the sameness below: `1` and `1.0` are one key, and so are bytes and the array of the same numbers. A text key is data, the empty text included. A map holds its keys in one order, whatever order its entries were written in: by kind first, null, then booleans, numbers, text, lists, maps and structs; then false before true, numbers by worth, text by the UTF-8 bytes of its composed spelling, lists element by element with a shorter one first on a common start, maps entry by entry, and structs by name and then field by field. A fraction that is not a number is not the same as itself, so a map holding one as a key never finds it again.

**When two values are the same**, which is what `Standard.Logic.equal` answers:

- A whole number and a fraction of the same worth are the same value. Numbers are compared by what they are worth, not by which of the two they are, and exactly, at **every** size: `9007199254740993` (2^53 + 1) is not equal to `9007199254740992.0`, however binary64 would round it. Ordering compares two of one type, under [the standard vocabulary](vocabulary.md).
- A run holds no fraction without a finite value. No document and no encoding writes one, the standard vocabulary's arithmetic refuses where its answer has none, and a door a host hands one through **refuses at the run**, under [running](running.md).
- Bytes are an array spelled compactly, so they are the same as an array of the same whole numbers in the same order: `x"6869"` and `[104, 105]` are one value, and `equal` says so. Bytes are not text: no encoding is assumed, so no Unicode rule applies. Which spelling a value wears takes no part in sameness.
- Arrays are the same when their elements are, in order.
- Maps are the same when they hold the same keys bound to the same values. Structs are the same when they hold the same name and the same field names bound to the same values. A struct has no order, so order is not part of the answer; the name is part of what a struct holds, so an `Account` and a `Vault` with the same fields are two values, and a map is never the same as a struct.
- Null is the same as null.
- A procedure is the same as no value, itself included, and so is a collection holding one.
- **Text is counted and compared as a person reads it**: by extended grapheme cluster, under Unicode canonical equivalence. A letter written as a letter and the same letter written as letter-plus-combining-mark are one character and are equal; `"é"` is `"é"` whichever way its bytes spell it, and its `count` is 1. An implementation whose platform strings compare by code unit must not expose that comparison here.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-map-is-never-the-same-as-a-struct`
- `a-procedure-is-the-same-as-no-value`
- `a-struct-literal-written-with-a-name-refuses`
- `a-whole-and-a-fraction-meet-exactly`
- `a-whole-fraction-stays-a-fraction`
- `a-whole-key-and-a-fraction-of-its-worth-are-one-key`
- `arrays-in-another-order-are-two-values`
- `bytes-and-an-array-share-their-worth`
- `null-is-the-same-as-null`
- `two-names-of-one-structure-are-two-values`
- `two-spellings-of-one-text-are-one-value`
- `values-are-the-same-by-what-they-hold`
