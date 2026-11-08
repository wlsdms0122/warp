# WARP-42: Data, in the text

Status: accepted

## Summary

Data in the text is the nodes that hold values, read as values. The rules decide how scalars, arrays, dictionaries and structs are written, and that a dictionary entry writes its key as the value it is.

## Motivation

A case's `answers`, its arguments and an object hold values rather than expressions, and a value reads alike in every implementation or a case answering it measures nothing. With no node of its own for each kind of value, a reader could take `(dictionary (entry "null" 1) (entry null 2))` for one key written twice where another reads two keys, and a case answering either would pass on one and fail on the other.

## Rules

Data is the nodes that hold values, read as values. It reads `list` and the atoms from [Warp text](../WARP-7/SPEC.md#the-grammar), and each node is a `list`, its elements the atoms and nodes shown.

```
data             = scalar | array | dictionary | struct
scalar           = null-atom | bool-atom | integer-atom | double-atom | string-atom | bytes-atom
array            = "(" "array" { data } ")"
dictionary       = "(" "dictionary" { entry } ")"
entry            = "(" "entry" data data ")"
struct           = "(" "struct" name-atom { field } ")"
field            = "(" "field" name-atom data ")"
```

| part | what it may be |
|---|---|
| a `struct`'s `name-atom` | a struct's or a case's spelling, under [values](../WARP-2/SPEC.md) |

A `scalar` is the value its atom is, an `array` the array of its elements, a `dictionary` the dictionary from each `entry`'s first value to its second, and a `struct` the struct of that name holding each `field`'s value under the field's name. A dictionary is keyed by values, and each entry writes its key as the value it is, so the string `"null"` and the value `null` are two keys, and a dictionary keyed by a struct writes `(dictionary (entry (struct App.Point (field x 1)) 5))`. Data is what a case's `answers`, its arguments and an object are written in, and a sentence quoting a value writes it as data on one line.

## Interactions

- An object's values: [values, in an object](../WARP-90/SPEC.md).
- The order the writer gives entries and fields: [the writer's layout](../WARP-45/SPEC.md).

## Alternatives considered

## Notes
