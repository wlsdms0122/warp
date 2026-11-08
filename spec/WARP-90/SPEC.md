# WARP-90: Values, in an object

Status: accepted

## Summary

A value inside an object is an entry in the value table. The rules decide the tag and fields of each kind, closures and held-beside-a-type values among them, and what a reading refuses.

## Motivation

A value an object holds is what a constant folded to or a variable starts a run holding, and a closure among them must be read back beside another link, so a value is written by what the document says and never by where a run or a link put it.

## Rules

A *value* is the number of an entry in `valueTable`, and the entry is `[tag, …]`:

| tag | value | fields |
|---|---|---|
| 0 | null | |
| 1 | a bool | the bool |
| 2 | an int | the int |
| 3 | a double | the double |
| 4 | a string | the string |
| 5 | bytes | the bytes |
| 6 | an array | its elements, a list of *value* |
| 7 | a struct | its name, a *name*; its field names, a list of *name* in name order; its field values, a list of *value*, one for each name in that order |
| 8 | a closure | the identity of the document that wrote it, bytes, under [identity and dependencies](../WARP-91/SPEC.md); the *declaration* that wrote it; which of that declaration's closures it is, counted from zero; a list of `[slot, value]` for what it captured, in slot order; and name → *type* for what fills each type parameter of the declaration that wrote it, as a document writes a type |
| 9 | a dictionary | its keys, a list of *value* in the key order; its values, a list of *value* in the same order |
| 10 | a value held beside a type | the *value*; the *type* it holds, as a document writes a type |

A dictionary's key out of the key order or written twice **refuses**. A link reads a closure's types again as it resolves the closure, and a held value's type as it makes the box a variable starts in, lays down the value a constant folds to, or resolves the closure that captured it: a variable's start, the value a constant folds to, and what a closure captured, are written as tag 10 where the value, or a part of it, holds a type under *a value read as a contract* in [contracts](../WARP-53/SPEC.md). A closure written by a document nobody wrote down, or holding a box of the run that made it, is not a value an object holds, and such an object is not written. A program holding a closure written by a document nobody wrote down builds and runs with no object written for it, so a caller that caches does not build, write and refuse in a loop.

**Note.** A closure read back from an object holds a standing type parameter without its bounds. A closure value writes what fills each type parameter of the declaration that wrote it as a document writes a type, so a closure made where a bounded type parameter was filled by no call, as at an entry, reads that parameter back by its name alone. Only the refusal of a type parameter no call filled reads it there, and that asks whether the parameter stands, not what bounds it, so no answer changes.

## Interactions

- A closure's *declaration* and its count are written in `numbering` under [what an object holds](../WARP-85/SPEC.md), and its document's identity under [identity and dependencies](../WARP-91/SPEC.md).

## Alternatives considered

- A closure by its row's place in a link. The place is the link's and stands nowhere in an object, so a closure spelled by it could not be read back beside another link.

## Notes
