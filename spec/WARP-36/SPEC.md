# WARP-36: Brackets read what a list or a dictionary holds

Status: accepted

## Summary

Brackets read what a list or a dictionary holds. The rules decide that the index reads as an Int on a list and as the key type on a dictionary, how a key finds its entry, and that brackets on any other type refuse at the build.

## Motivation

What brackets read is the IR's, because a bracket is a path step and a path is judged where names resolve. `{ ref: "scores[name]" }` reads the entry under what `name` holds, and the value between the brackets is judged against the dictionary's key type before anything runs, so no runtime compares a key of one type against keys of another and finds nothing where another would refuse.

## Rules

**Brackets read what a list or a dictionary holds** at the value between them, judged against what is indexed: on a list it stands where an `Int` is read, a position, and on a dictionary where the dictionary's key type is read, a key. So `d[3]` on `Dictionary<Int, String>` reads the entry under `3`, `d["a"]` on `Dictionary<String, Int>` the entry under `"a"`, and `d[k]` the entry under what `k` holds; a key finds the entry under the key that is the same value, under [values](../WARP-3/SPEC.md). The place between the brackets takes what a slot of the type read there takes, under [what a slot takes](../WARP-48/SPEC.md): a value written there, an `integer` or a `string` under [a path](../WARP-31/SPEC.md#the-grammar), is a literal written into that place, and a path there is a reading handed to it, so one the place does not take **refuses at the build**. A path between the brackets is a path of its own, judged as one even where the outer walk stops. Brackets on any other type, a declared struct among them, **refuse at the build**: a struct's fields are its type's, read by a dot. An entry the dictionary does not hold refuses at the run, and at the build where the path folds, under [a constant-headed path](../WARP-35/SPEC.md), and `?[` reads it as the none. A constant written between the brackets folds at the build to the value it reads and is judged at the type it holds, as a path there is.

## Interactions

- `?[` and an index past the end: [null is not read through](../WARP-34/SPEC.md).
- A constant between brackets: [a constant-headed path](../WARP-35/SPEC.md).

## Alternatives considered

## Notes
