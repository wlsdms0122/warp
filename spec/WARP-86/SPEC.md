# WARP-86: How a part is laid out

Status: accepted

## Summary

A part inside the object's dictionary is written as its fields in order, and a variant as its tag first. The rules decide how names, lists, optional fields and counts are written, and how types are laid out in the type table.

## Motivation

An object is read back by an implementation that never saw the build that wrote it, with nothing beside the bytes to say what a field is, so each part needs one writing that a reader takes back field by field and that no two writers can lay out differently.

## Rules

Inside the dictionary, a part is written as its fields **in order**, and a variant as its **tag** before them, so a reading beside the same tables reads it back and one that is not refuses it. The rules, used everywhere below:

- A *name* is a string that is written and in normal form C, under [names](../WARP-67/SPEC.md#rules), and one that is not, `""` among them, **refuses**. What else a reading asks of a name is under [what a reading refuses](../WARP-92/SPEC.md).
- A list a name keys is `[[name, value] …]`, in name order.
- A field that may hold nothing is a list of none or one: `[]` or `[value]`. So a value that is itself null is told from no value at all.
- The fields a row gives after *where …, then* stand only where that holds, and the entry ends before them otherwise: a struct or an enum writes its type parameters and their bounds only where it takes type parameters, and a declared name its list of types only where it applies the type to some. So a struct's or an enum's type parameters and a declared name's list of types are never written empty, and one entry has one writing. Every other field always stands.
- A variant is `[tag, fields …]`, and a tag [WARP-85](../WARP-85/SPEC.md) to [WARP-90](../WARP-90/SPEC.md), [WARP-93](../WARP-93/SPEC.md) and [WARP-95](../WARP-95/SPEC.md) do not name **refuses**.
- A count, a slot, a row and a position are integers at or above zero, and one below zero **refuses** where it is read.

### Types, as a document writes them

A *type* is the number of an entry in `typeTable`, and the entry is `[tag, …]`:

| tag | type | fields |
|---|---|---|
| 0 | `Any` | |
| 1 | `Never` | |
| 2 | `Null` | |
| 3 | `Bool` | |
| 4 | `Int` | |
| 5 | `Double` | |
| 6 | `String` | |
| 7 | `Array<T>` | *type* |
| 8 | `Dictionary<K, V>` | the key's *type*, the value's *type* |
| 9 | struct, written in `types` as the declaration itself and never as an entry | name → *type*; where it takes type parameters, then their names in order, at least one and none twice, and name → the contracts bounding the type parameter of that name, ascending, at least one, for each one it bounds |
| 10 | `Procedure` | *procedure type* or nothing, *constness*, *isolation* |
| 11 | `var T` | *type* |
| 12 | `inout T` | *type* |
| 13 | `T?` | *type* |
| 14 | a declared name | name; where it applies a struct or an enum to types, then a list of *type*, at least one |
| 15 | a type parameter | name |
| 16 | a composition `A & B` | a list of names, ascending, two or more: one contract is written as its name, tag 14 |
| 18 | `Self` | |
| 19 | an associated type, `some T.Item` or `Self.Item` | what it stands on, a type parameter's name or another associated type's label, `T.Item` for `some T.Item.Key`; its name |
| 20 | enum, written in `types` as the declaration itself and never as an entry | where it is written and its fields under [enums](../WARP-93/SPEC.md#in-the-binary-and-in-an-object) |
| 21 | a type member of an applied type, `App.Wrapper<String>.Item` | the applied type's *type*; the type member's name |

A *head* is what a document gives a type under, under [types](../WARP-55/SPEC.md): where it is bare, the name of the type it is about, and otherwise `[name, arguments, bounds]`: that name, `Optional` for an Optional's head; the types it applies the named type to, a list of *type*, at least one; and name → the contracts bounding the type parameter of that name, ascending, at least one, for each one it bounds. A list a head keys stands ascending by the heads' spellings under *the grammar* in [heads](../WARP-55/SPEC.md#the-grammar), compared as names are, none twice, so `Bool?` stands before `Int`.

A *procedure type* is `[parameters, returns, failing]`: a list of *type*, in position order, a *type*, and a *failing*. A *signature* is `[parameters, returns, failing, constness, isolation, bounds, sameTypes]`: a list of *parameter*, in the declaration's order; a *type*; a *failing*; a *constness*; an *isolation*; name → the contracts bounding the type parameter or the associated type of that name, ascending, at least one, for each one the signature bounds; and name → *type* for each associated type the signature says is a type. A *parameter* is `[name, type]`: the name, then a list of none or one *type*, none where the parameter takes anything, so `Any` is never written there.

*Constness* is `0` unstated or `1` const. *Isolation* is `0` unstated or `1` isolated. *Failing* is `[0]`, anything, or `[1, names]`, the names ascending.

## Interactions

- A *type* entry is a type as [how a type is written](../WARP-46/SPEC.md) writes it.
- An associated type entry and a signature's `sameTypes` are [associated types](../WARP-59/SPEC.md).
- *Constness* and *isolation* are what [a const procedure](../WARP-15/SPEC.md) and [concurrency](../WARP-73/SPEC.md) declare, and *failing* is [what a body may fail with](../WARP-26/SPEC.md).
- A *name* holds the grammar of [names and their grammar](../WARP-67/SPEC.md).

## Alternatives considered

## Notes
