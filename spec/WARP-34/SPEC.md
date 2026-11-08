# WARP-34: Null is not read through

Status: accepted

## Summary

Null is not read through. The rules decide that a segment reading a null or an Optional refuses, what the optional spellings ?. and ?[ expect to be absent, and what such a path reads as.

## Motivation

A field that is absent and a field that holds null would both read as null where nothing marks the reading, and a document that misread a length or a name would run on with a null that says nothing of where it came from.

## Rules

- **Null is not read through.** A segment reading a null, or one whose reading is an Optional (`T?`), **refuses**: at the build where its reading is an Optional or `Null`, and at the run where a null arrives that its reading does not show. `?.` is the one spelling that expects absence on a name: it reads past every level of an Optional, and reads a none at any level as null for the whole path. A path whose last step reads an Optional reads that Optional, and one whose last step reads no Optional reads its Optional; where that last reading is no Optional and may hold a none, the value the path finds is the Optional's some unless a marked step met a none, so `o?.v` on a field read as `Any` is `Some` holding `null` where the field holds a none, and the none where `o` is absent. `?[` is that same mark on brackets. On a list what it expects absent is the **list itself**, never an element; on a dictionary it is the dictionary or the entry, and the step reads the entry as the Optional of the dictionary's value type exactly, and that Optional is what the path's last step reads: the none where the dictionary holds no entry, and the entry's some where it does, so on `Dictionary<String, Int?>` an absent key reads `null` and a present `null` reads `Some` holding it.
- An **index past the end refuses at the run**, and at the build where the path folds, under [a constant-headed path](../WARP-35/SPEC.md); a write's is under [what a write reaches](../WARP-20/SPEC.md). The array is there and says how long it is, so a reading that misses it read the length wrong. `?[` does not change this: it is `?.`'s mark on an index. It expects the **array's** absence, not the element's, so `items?[0]` reads the none of `items` as null for the whole path, and refuses past the end of one that arrived. Between the brackets a digit begins an `integer` and never a name, under [a path](../WARP-31/SPEC.md#the-grammar), so one past what an `Int` holds **refuses at the load**. On a list an integer below zero is no position: one written or folded between the brackets **refuses at the build**, and one the run reads refuses at the run as a position past the end does.
- A `?.` or `?[` that could not have read past anything (on a struct's declared field, on an array the type says is there) **refuses at the build**. The claim of absence has to be one the types leave open.
- The **head of a path takes no mark**: a path begins with an `identifier`, and a `?` stands before a step after it, under [a path](../WARP-31/SPEC.md#the-grammar). A head is a name a scope holds, and there is nothing before it to read past: a name that names nothing is a reading gone wrong, not an absence a mark can expect. A string beginning with a mark is no path, and it **refuses at the load** with every string the grammar does not produce.

## Interactions

- What an Optional is and its none: [what a slot takes](../WARP-48/SPEC.md).

## Alternatives considered

- An Optional as a union of `Null` and `T`. `Int??` would collapse into `Int?`, and `?[` on a dictionary whose values are Optional could not tell an absent key from a present null.

## Notes

**Note.** No case holds the run half of null not being read through. A value is held to its type at every door, and a value read as `Any`, a contract or a type parameter takes no dot and no index, so no document is known whose segment reads a null its reading does not show. The half is written so that an implementation meeting one refuses rather than reads past it.
