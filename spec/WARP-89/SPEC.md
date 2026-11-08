# WARP-89: Lowered types

Status: accepted

## Summary

A lowered type is a type as a body stands on it. The rules decide the tag and fields of each entry in the lowered type table, including procedures, declared types, type parameters and compositions.

## Motivation

An alias, a type member's spelling among them, is already the type it stands for, and a declared type is its place in `typeNumbering`, so nothing a run or a link reads in a body asks a name again.

## Rules

A *lowered type* is a type as a body stands on it, the number of an entry in `loweredTypeTable`, and the entry is `[tag, …]`:

| tag | lowered type | fields |
|---|---|---|
| 0 to 6 | `Any` `Never` `Null` `Bool` `Int` `Double` `String` | |
| 7 | array | *lowered type* |
| 8 | dictionary | the key's *lowered type*, the value's *lowered type* |
| 10 | procedure | parameters or nothing, a list of *lowered type* in position order; returns or nothing, and a *failing* or nothing, each nothing exactly where the parameters are nothing; *constness*; *isolation* |
| 12 | inout | *lowered type* |
| 13 | optional | *lowered type* |
| 14 | a declared type | its place in `typeNumbering`; where it applies a struct or an enum to types, then a list of *lowered type*, at least one |
| 15 | a type parameter, or an associated type as it is written, `T.Item` or `Self.Item` | a type parameter's name, `T`, or a type member's label under [names](../WARP-67/SPEC.md#the-grammar), `T.Item` or `Self.Item`; a list of the contracts bounding it, ascending, those of an associated type being what the contracts asking it and the signature hold it to |
| 16 | a composition | a list of the contracts, ascending, at least one |

A field that may hold nothing, and the fields a row gives after *where …, then*, are written as a *type*'s are under [how a part is laid out](../WARP-86/SPEC.md).

## Interactions

- A *lowered type* mirrors the *type* entries of [how a part is laid out](../WARP-86/SPEC.md), and `typeNumbering` is the list of [operations](../WARP-88/SPEC.md).

## Alternatives considered

## Notes
