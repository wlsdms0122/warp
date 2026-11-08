# WARP-31: A path

Status: accepted

## Summary

A path is a name followed by field and bracket steps. The rules decide how a path is cut, what may stand between brackets, and the one spelling each path has, so that other spellings refuse at the load.

## Motivation

A path is held in the tree as one string, so its grammar decides which names it reads. Its names are identifiers, which hold no character a step is written with, so every step a path writes is read the one way the grammar gives it.

## Rules

A path is a name, then `.name` for a field and `[…]` for what a list or a dictionary holds.

### The grammar

A path reads `identifier` from [names](../WARP-67/SPEC.md#the-grammar), and `integer-atom`, `quote` and `backslash` from [encodings](../WARP-7/SPEC.md#the-grammar).

```
path             = identifier { step }
step             = [ "?" ] "." identifier | [ "?" ] "[" index "]"
write-path       = identifier { "." identifier | "[" index "]" }
index            = integer | string | path
integer          = integer-atom
string           = quote { string-character | path-escape } quote
path-escape      = backslash ( quote | backslash )
string-character = any Unicode scalar other than quote and backslash
```

| part | what it may be |
|---|---|
| an `integer` | one an `Int` holds, under [values](../WARP-2/SPEC.md) |

The first `identifier` of a path is its **head**, a name a scope holds. A `.` step reads the field its `identifier` names, under [a dot reads a name](../WARP-33/SPEC.md), and a `[` step what a list holds at a position or a dictionary under a key, under [brackets](../WARP-36/SPEC.md). A `?` before a step is the mark that expects an absence, under [null is not read through](../WARP-34/SPEC.md). Between the brackets an `integer` is that integer in decimal, a `string` is the string whose characters are its `string-character`s and, for each `path-escape`, the quote or backslash after its backslash, and a `path` is a path of its own. Between the brackets a digit or a `-` begins an `integer`, a quote a `string` and a letter or a `_` a `path`, so `a[1]` reads at the integer 1, `a[k]` at what the name `k` holds, and `a[1x]` is no path. A `write-path` is the path a `set` writes, under [what a write reaches](../WARP-20/SPEC.md): its own steps are unmarked, and its brackets hold any `index` a read's do.

A string the grammar does not produce, and one with a part the table above does not let it be, **refuses at the load**. **A path is written one way**: the grammar writes no white space but what a `string` holds and each integer as an `integer-atom`, so every other spelling of a path is a string it does not produce, as a document says each thing one way under [the document format](../WARP-11/SPEC.md).

## Interactions

- One spelling: [a document says each thing one way](../WARP-11/SPEC.md).
- What a step reads: [a dot reads a name](../WARP-33/SPEC.md), [brackets](../WARP-36/SPEC.md), and the marks under [null is not read through](../WARP-34/SPEC.md).

## Alternatives considered

## Notes
