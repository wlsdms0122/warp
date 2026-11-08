# WARP-30: An expression's forms

Status: accepted

## Summary

An expression is what is read rather than run. The rules decide the forms an expression takes, namely scalars, arrays, and the dictionaries with one key such as ref, struct, dictionary, call and closure, and that a construct is refused where an operand stands.

## Motivation

Every runtime has to read one dictionary in a document as one thing. A front end writes `{ ref: "user.name" }`, `{ struct: { x: 1 } }` and `{ call: … }` as dictionaries in one tree, and a dictionary whose key named no form, or a bare dictionary read as a struct, would leave two runtimes to guess which value it is. Fixing the keys, and refusing every other dictionary at the load, lets a value be written with no escape and a struct's fields be named anything.

## Rules

What is read rather than run. A literal, a name, a path through one, a cast, a struct, a dictionary, an array, a call and a closure written where a value is wanted. The line between this WARP and [statements](../WARP-19/SPEC.md) is the line an operand stands on: a construct runs a body and is refused here.

A scalar is itself, a literal. A string is always literal text; nothing inside it is ever re-parsed. An array is an array of expressions. A dictionary is an expression by its **one key**, and that key is one of these:

| form | means |
|---|---|
| `{ ref: "a.b[0]" }` | a name, resolved in the scope that reads it |
| `{ struct: { … } }` | a struct of the declared struct the place it is written into reads, under *a declared struct is nominal* in [types](../WARP-49/SPEC.md), its fields each an expression, made in the order of their names. A field is called by a value's name under [names](../WARP-67/SPEC.md), `ref` and `value` among them |
| `{ case: { <case>: { … } } }` | a case literal: a value of the enum the place it is written into reads, under one of its cases' spellings, its form and reading under [enums](../WARP-93/SPEC.md#a-cases-value) |
| `{ dictionary: [[<key>, <value>], …] }` | a dictionary, its entries each a list of two expressions, a key and a value. Its entries are written in the order they stand, each as [a dictionary's keys](../WARP-3/SPEC.md) says a key is written. The keys join to one type and the values to another, the way a list literal's elements do, an empty one holding `Never` at both; written where a dictionary type is declared, every key and value is held to it part by part. An entry that is not a list of two **refuses at the load** |
| `{ call: <call> }` | a call where a value is wanted, under *calls* in [statements](../WARP-22/SPEC.md) |
| `{ closure: <procedure> }` | a procedure written where a value is wanted, its keys a procedure's under [a procedure](../WARP-12/SPEC.md) short of `access`, `bounds` and `sameTypes`: `parameters`, `returns`, `failing`, `const`, `isolated` and `body`. Nothing names a closure, and its `some T` is the `T` of the procedure it is written in, which says what bounds it and what its associated types are. A closure writing `access`, `bounds` or `sameTypes`, or a bound beside a `some T`, **refuses at the load** |
| `{ as: { of: <value>, type: <type> } }` | read the value as that type: how a value the build could not type, one read as `Any` or as a contract, is held to one |
| `{ as?: { of: <value>, type: <type> } }` | an asking cast, under [a cast](../WARP-32/SPEC.md): the result is exactly `T?`, so a match is its some, and a match that is `null` or a `Some` is a `Some` holding it |

A dictionary with another key, or with more than one, **refuses at the load**. A key names a form and never a field, so no field name is reserved.

A construct's key is read under a statement's `value` and nowhere else, under [statements](../WARP-19/SPEC.md).

## Interactions

- A closure's `some T`: [type parameters](../WARP-51/SPEC.md).
- `as` and `as?`: [a cast](../WARP-32/SPEC.md); `ref`: [a path](../WARP-31/SPEC.md).

## Alternatives considered

- A bare dictionary read as a struct, with an escape such as `{ value: … }` for one whose key names a form. That gives one value two spellings, and a struct literal whose fields are named like forms has no plain spelling at all.

## Notes
