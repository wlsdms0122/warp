# WARP-55: Heads

Status: accepted

## Summary

An extension's key is its head. The rules decide how a head names a type, an applied type or an Optional, how each some T in a head is its own type parameter, and that a head is held as a parameter's type is.

## Motivation

Some claims hold for only some values of a type: a box conforms to `Hashable` where what it holds does, and a list of integers can be given what a list of strings is not. A front end that has conditional conformance cannot write that in place, since the condition decides whether a call builds.

## Rules

**An extension's key is its head**: a type's name, the type applied to what its brackets hold, `Array<Int>`, `App.Box<some T: Hashable>`, or an Optional, `Int?`, a string under the grammar below. What an extension gives under a head applying its type holds for the values the head takes, the way a parameter written as the head takes an argument. `Array<Int>` takes every list of integers.

### The grammar

A head reads `qualified-name` from [names](../WARP-67/SPEC.md) and `applied`, `operand` and `joined` from [how a type is written](../WARP-46/SPEC.md#the-grammar).

```
head            = qualified-name | applied | optional
optional        = operand | joined
```

| part | what it may be |
|---|---|
| the `qualified-name` of a bare head | a type's name, `Array`, `Dictionary`, or a `language-name` that names a type a value is an instance of: `Null`, `Bool`, `Int`, `Double`, `String`, `Failure` and `Round`. Why the rest are not is under [claims](../WARP-54/SPEC.md) |
| an `optional` | one ending in `?` |
| each type an `applied` or an `optional` holds | a type written as a head writes it, under *where a type is written* in [bounds](../WARP-52/SPEC.md#where-a-type-is-written): a `some T` bounded where the head first names `T`, and no `some T.Item`, `Self` or mark |

A head is not a `type`: `Array`, `Dictionary` and a struct listing type parameters stand bare in one. Its parts are written as a type's are, one way, so a bound's names stand in name order, under [how a type is written](../WARP-46/SPEC.md#the-grammar). The **name of the type a head is about** is the `qualified-name` of a bare head or of an `applied`, and `Optional` for an `optional`: a member's spelling and a type member's spelling under [names](../WARP-67/SPEC.md#the-grammar), and a claim among [the imports](../WARP-10/SPEC.md#the-grammar), write it.

### What a head takes

**An Optional's head is written by its `?`**, since no head or slot writes the Optional by name: `Int?` takes every reading of `Int?`, `some W?` every Optional, and `(some W: P)?` every Optional of what conforms to `P`.

**Each `some T` a head writes is the head's own type parameter**, held to the contracts written beside it where the head first names it, `some T: Hashable & Standard.Comparable`, so `App.Box<some T: Hashable>` takes every box of something that conforms to `Hashable`.

**A head is held as a parameter's type is**, being a mention of the type it applies: one applying a struct or an [enum](../WARP-94/SPEC.md) to what its bounds do not hold, or a dictionary to a key that does not conform to `Hashable`, **refuses at the build**, and so does a bound naming what no module declares as a contract. A key the head grammar does not produce, one with a part the table above does not let it be, and two keys of one document reading as one head **refuse at the load**.

**Two keys read as one head where they are one string once their type parameters are renamed**: each key's `some` names renamed, in the order the key first names them, to one list of names, and every other part, each bound among them, compared as written. So `Array<some T>` and `Array<some U>` read as one head, and `Array` and `Array<some T>`, or `Array<Int>` and `Array<App.Num>` with `App.Num` an alias of `Int`, are two, though each pair takes the same values.

**A claim under a head says the values it takes conform to the contract**: a reading the head takes conforms to it, and one it does not take **refuses at the build** where it is handed.

**A value conforms where it settles into the head.** A value carries no type's arguments, so where a value is what is judged, at a cast, a door and a call a constant folds through, it conforms where it settles into the head, the head's own type parameters filled by what its parts read as, the way a door fits a value to a slot writing the struct. Values meeting at one type parameter of a call or a struct from outside are one type where they are of one struct, or of cases of one enum, each held to the bounds by what it is: a box holding `1` conforms by a claim under `App.Box<Int?>`, and a cast of a value the head does not take is null where it reads `as?`.

**What holds for some of a struct's values is written under a head applying it**, in the document declaring it as in any other, since a struct's declaration gives what every value of it has.

## Interactions

- Members under a head are under [a claim holds to members](../WARP-56/SPEC.md) and [members](../WARP-58/SPEC.md).
- Two claims under heads taking the same values are one claim, under [what a document stands on](../WARP-57/SPEC.md).
- A head writes no associated type, under [the associated types of a type parameter](../WARP-60/SPEC.md).

## Alternatives considered

- The condition read off the signatures of the members that back the claim. A condition a member's signature does not happen to state could not be said at all.
- The condition written as bounds put back on the struct's parameter, apart from the claim. Systems that let a type conform after it is declared, or under a condition, write each conformance as an item of its own with its condition in its head, and none moves the condition elsewhere; it would also write the parameter's name a second time.

## Notes
