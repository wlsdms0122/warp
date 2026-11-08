# WARP-3: A dictionary's keys

Status: accepted

## Summary

A dictionary holds each key once, and a key is a value, so keys that are the same value are one key. The rules decide which values may be keys, what writing an existing key does, and the single order in which a dictionary holds its keys whatever order its entries were written in.

## Motivation

A dictionary is written in canonical bytes and compared by sameness, so which keys are one key and the order they stand in cannot be left to each implementation's own hash table. If either were an implementation's choice, a dictionary's count and its document's identity would depend on which implementation built it.

## Rules

**A dictionary's keys.** A key is a value, and a dictionary holds each key once, by the sameness under [when two values are the same](../WARP-4/SPEC.md): `1` and `1.0` are one key, and so are bytes and the array of the same numbers. A `String` key is data, the empty one included. A value holding a procedure is the same as no value, so it is no key: a dictionary holding one as a key is no value, and a run making one **refuses at the run**, under [a run refuses](../WARP-72/SPEC.md). Writing a key the dictionary already holds writes its value and keeps the key it holds, so a dictionary holding `1` and written under `1.0` holds the new value under `1`, in a literal's later entry, a path and `Standard.Collection.setting` alike.

**The key order.** A dictionary holds its keys in one order, whatever order its entries were written in. Keys fall into groups, which stand in the order of the table, and two keys of one group stand as its second column says:

| group | within it |
|---|---|
| null | |
| booleans | false before true |
| numbers, an `Int` and a `Double` alike | by worth |
| `String` | by its UTF-8 bytes once in Unicode Normalization Form C |
| arrays, bytes among them | element by element |
| dictionaries | entry by entry, each entry by its key and then its value |
| structs | by name, by its UTF-8 bytes, and then field by field in the order of their names, each field by its name and then its value |

Of two arrays, two dictionaries or two structs sharing a start, the shorter comes first.

## Interactions

- The key order is the order a writer writes and a binary reader holds keys to: [WARP-5](../WARP-5/SPEC.md), [WARP-6](../WARP-6/SPEC.md).

## Alternatives considered

## Notes
