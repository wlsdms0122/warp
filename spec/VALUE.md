# The value model

What a value is, and when two of them are one. Nothing on this page needs a program: a value is what a document carries, what a slot judges and what an encoding writes, so every other page reads this one and this one reads none of them.

A program computes over eight kinds of data, plus one value that is not data:

| kind | writes as, in a text | notes |
|---|---|---|
| null | `null` | |
| bool | `true` / `false` | |
| int | `1`, `-3` | signed, 64-bit; overflow **refuses**, it does not wrap |
| double | `1.0`, `1e+16` | IEEE-754 binary64; a document cannot carry infinity or NaN |
| string | `"hi"` | Unicode scalars |
| array | `(array …)`, or `x"6869"` | ordered; `x"…"` is **bytes**, the compact spelling of an `Array<Int>` whose every element is from 0 to 255, what a carrying form carries when the payload is not a `String` |
| dictionary | `(dictionary (entry k v) …)` | entries, each a value under a key that is a value, every key once; held in the key order below |
| struct | `(struct Name (field x v) …)` | unordered fields, names unique; carries the **name** of the declared struct it is, a type's name under [checking](CHECKING.md) or a struct's the language declares, which a slot of a declared struct takes only where it is that struct's. A struct named otherwise is no value, and **refuses** in either encoding |
| procedure | | code with what it captured; exists only at run time, never in a document |

**A struct's name.** Every struct is a value of a declared struct and carries its name. A struct literal is read as the declared struct of the place it is written into and takes that name there, and a literal a program writes with one (`(struct Ghost.T (field x 1))` in a text) **refuses at the load**. A struct carries its name through every slot declaring the type and through `Any`, and fits no other: `Dictionary<String, T>` takes no struct, and a declared struct takes no dictionary, under [Types](TYPE.md). A value from outside under a name, through `Any` included, is held at the door to the struct the name declares, under *a declared struct is nominal* in [Types](TYPE.md).

**A `Some` holds `null` or a `Some`** under its one field, `wrapped`: the language declares it under [Types](TYPE.md). One holding anything else is no value, and **refuses** in either encoding and at every door.

**A dictionary's keys.** A key is a value, and a dictionary holds each key once, by the sameness below: `1` and `1.0` are one key, and so are bytes and the array of the same numbers. A `String` key is data, the empty one included. A dictionary holds its keys in one order, whatever order its entries were written in: by kind first, null, then booleans, numbers, `String`, arrays, dictionaries and structs; then false before true, numbers by worth, a `String` by the UTF-8 bytes of its composed spelling, arrays element by element, dictionaries entry by entry, each entry by its key and then its value, and structs by name and then field by field in the order of their names, each field by its name and then its value; of two arrays or two dictionaries sharing a start, the shorter comes first.

**When two values are the same**, which is what `Standard.Logic.equal` decides:

- An `Int` and a `Double` of the same worth are the same value. Numbers are compared by what they are worth, not by which of the two they are, and exactly, at **every** size: `9007199254740993` (2^53 + 1) is not equal to `9007199254740992.0`, however binary64 would round it. Ordering compares two of one type, under [the standard vocabulary](VOCABULARY.md).
- A run holds no `Double` without a finite value. No document and no encoding writes one, and a door a host hands one through **refuses at the run**, a return value of the standard vocabulary's arithmetic among them, under [running](RUNNING.md).
- Bytes are an array spelled compactly, so they are the same as an array of the same integers in the same order: `x"6869"` and `(array 104 105)` are one value, and `equal` says so. Bytes are not a `String`: no encoding is assumed, so no Unicode rule applies. Which spelling a value wears takes no part in sameness.
- Arrays are the same when their elements are, in order.
- Dictionaries are the same when they hold the same keys bound to the same values. Structs are the same when they hold the same name and the same field names bound to the same values. A struct has no order, so order takes no part in sameness; the name is part of what a struct holds, so an `Account` and a `Vault` with the same fields are two values, and a dictionary is never the same as a struct.
- Null is the same as null.
- A procedure is the same as no value, itself included, and so is a collection holding one.
- **A `String` is counted and compared as a person reads it**: by extended grapheme cluster, under Unicode canonical equivalence. A letter written as a letter and the same letter written as letter-plus-combining-mark are one character and are equal; `"é"` is `"é"` whichever way its bytes spell it, and its `count` is 1. An implementation whose platform strings compare by code unit must not expose that comparison here.

## Cases

What `conformance/` asks about this page, by the name each case's file carries.

- `a-dictionary-holds-two-keys-of-each-kind-in-order`
- `a-dictionary-is-never-the-same-as-a-struct`
- `a-door-fills-a-type-parameter-from-a-some-of-a-none-with-its-optional`
- `a-host-handing-some-for-an-inner-none-is-taken`
- `a-procedure-is-the-same-as-no-value`
- `a-some-holding-what-is-not-a-none-refuses`
- `a-some-holding-what-is-not-a-none-written-as-text-refuses`
- `a-string-key-and-its-decomposed-spelling-are-one-key-refuses`
- `a-struct-literal-written-with-a-name-refuses`
- `a-struct-named-as-the-contract-the-language-declares-refuses`
- `an-int-and-a-double-meet-exactly`
- `an-int-key-and-a-double-of-its-worth-are-one-key`
- `an-integral-double-stays-a-double`
- `arrays-in-another-order-are-two-values`
- `bytes-and-an-array-share-their-worth`
- `null-is-the-same-as-null`
- `two-names-of-one-structure-are-two-values`
- `two-spellings-of-one-string-are-one-value`
- `values-are-the-same-by-what-they-hold`
- `values-of-an-optional-are-the-same-by-what-they-hold`
