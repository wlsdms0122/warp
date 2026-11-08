# WARP-62: A dictionary's key

Status: accepted

## Summary

A dictionary's key must conform to the contract Hashable. The rules decide which types the language claims it for, how a declared struct conforms, and that a dictionary type or literal whose key does not conform refuses at the build.

## Motivation

A dictionary finds a value by its key, so a key has to be a value whose sameness the value model decides, the same in every implementation and with no procedure deciding it. Which types key a dictionary is therefore declared, as conformance to a contract, the way Swift asks a dictionary's key to be `Hashable`, and the build refuses a dictionary type keyed by `Any` or by a procedure type where it is written, before any value arrives.

## Rules

**The language declares one contract, `Hashable`**, which asks no procedures and which the key of every dictionary type conforms to. A type conforms to it as this table says, and an alias as the type it names:

| type | conforms to `Hashable` |
|---|---|
| `Never`, `Null`, `Bool`, `Int`, `Double`, `String`, `Array` and `Dictionary` | always, since the language claims it for each, whatever an `Array` or a `Dictionary` holds |
| an Optional | where what it wraps conforms, under `(some Wrapped: Hashable)?` |
| a struct or an [enum](../WARP-94/SPEC.md), a document's or one [the language declares](../WARP-61/SPEC.md) | where a document claims it does: `{ struct: { x: Int }, satisfies: ["Hashable"] }` |
| a contract | where it is `Hashable` |
| a composition | where it names `Hashable` among its parts: `App.Named & Hashable` |
| a type parameter or an associated type | where its bounds hold it to `Hashable` |
| `Any`, a procedure type | never |

A contract or a composition conforms by what it names and not by what conforms to it: `App.Named`, which only `Int` conforms to, keys no dictionary. `Never` has no value, so the claim for it admits no key, and the empty dictionary literal, which holds `Never` at its key under [expressions](../WARP-30/SPEC.md), reads as a dictionary wherever it stands. Which keys are one key is the value model's sameness, under [the value model](../WARP-3/SPEC.md), and no procedure decides it.

**Every dictionary type is keyed so, written or read.** A dictionary type whose key does not conform to `Hashable` **refuses at the build** where it is written, reached or not, and so does a dictionary literal whose keys read as such a type where its place declares no dictionary, since the literal reads as a dictionary keyed by what its keys join to; where the place declares a dictionary, each key is held to the key it declares. Whether a key conforms is judged against the claims within what the document stands on, under *what a document stands on* [above](../WARP-57/SPEC.md).

**A constant's dictionary keeps the key its expression was read as.** A constant's type is its value's, read position by position. A dictionary it holds, at any depth, takes the key of the reading the expression it folded from has at that position, where that reading is a dictionary type: folded from a call returning `Dictionary<Hashable, Int>`, a dictionary holding `1` and `"a"` is a value of that type, and folded from one returning `Array<Dictionary<Hashable, Int>>`, so is each such dictionary in the list. Where the reading at that position is no dictionary type, `Any` among them, a dictionary whose keys join to `Any` reads `Any` whole, as two dictionaries keyed apart do.

## Interactions

- `Hashable` is one of the names under [what the language declares](../WARP-61/SPEC.md).
- A dictionary keyed by a contract holds the type its keys were read as, under [contracts](../WARP-53/SPEC.md).

## Alternatives considered

## Notes
