# WARP-2: What a value is

Status: accepted

## Summary

The value model: the eight kinds of data a program computes over, plus the procedure, which exists only at run time. The rules decide what each kind is, how a struct carries the name of the declared struct it is, and when two values are one. Every other WARP reads this one.

## Motivation

Without its name in the value, a struct that crossed `Any` could not say which declared struct it is, and a slot would have only its fields to judge it by.

## Rules

What a value is, and when two of them are one. A value is what a document carries, what a slot judges and what an encoding writes, so every other WARP reads this one.

A program computes over eight kinds of data, plus one value that is not data:

| kind | writes as, in a text | notes |
|---|---|---|
| null | `null` | |
| bool | `true` / `false` | |
| int | `1`, `-3` | signed, 64-bit; overflow **refuses**, it does not wrap |
| double | `1.0`, `1e+16` | IEEE-754 binary64; a document cannot carry infinity or NaN |
| string | `"hi"` | Unicode scalars |
| array | `(array …)`, or `x"6869"` | ordered; `x"…"` is **bytes**, the compact spelling of an `Array<Int>` whose every element is from 0 to 255 |
| dictionary | `(dictionary (entry k v) …)` | entries, each a value under a key that is a value, every key once; held in the key order under [a dictionary's keys](../WARP-3/SPEC.md) |
| struct | `(struct Name (field x v) …)` | unordered fields, names unique; carries a **struct's name**, under *what a name names* in [names](../WARP-67/SPEC.md#what-a-name-names): the name of the declared struct it is, which a slot of a declared struct takes only where it is that struct's, or a case's spelling, and is then a value of that case's enum under [enums](../WARP-93/SPEC.md). A struct named otherwise is no value, and **refuses** in either encoding |
| procedure | | code with what it captured; exists only at run time, never in a document |

**A struct's name.** Every struct is a value of a declared struct and carries its name, or a value of an enum and carries one of its cases' spellings, under [enums](../WARP-93/SPEC.md). A struct literal is read as the declared struct of the place it is written into and takes that name there, and a literal a program writes with one (`(struct Ghost.T (field x 1))` in a text) **refuses at the load**. A struct carries its name through every slot declaring the type and through `Any`, and fits no other: `Dictionary<String, T>` takes no struct, and a declared struct takes no dictionary. A value from outside under a name, through `Any` included, is held at the door to the struct the name declares. Both are under [a declared struct is nominal](../WARP-49/SPEC.md).

**A `Some` is a struct of exactly one field, `wrapped`, holding `null` or a `Some`**: the language declares it under [what the language declares](../WARP-61/SPEC.md). Any other `Some` is no value, and **refuses** in either encoding and at every door.

**Note.** A case hands a door only what a case's text writes, and a text refuses a `Some` that is no value wherever it stands, so the door refusing one a host's procedure hands is held only by tests inside the implementation.

## Interactions

- When two values are one: [WARP-4](../WARP-4/SPEC.md).
- A run making a dictionary keyed by a procedure refuses: [WARP-72](../WARP-72/SPEC.md).

## Alternatives considered

- A value could be a reference to something shared. A reference would stand outside the rule that what runs at once touches no name another body could touch, under [concurrency](../WARP-73/SPEC.md), so concurrency would need another model. State lives in variables, module variables and parameters handed in place, and where a program needs identity or sharing, a host's procedure hands out a handle as a value.
- A struct could have no name, a record whose fields alone say what it is. A value of `App.Account` would then fit a slot of `App.Vault` with the same fields, a struct and a dictionary of the same entries would be one value, and nothing would stop a struct's fields from growing.

## Notes
