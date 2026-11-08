# WARP-27: `unwrap`

Status: accepted

## Summary

An unwrap takes an Optional apart one level. The rules decide its of, then and else keys, what the payload name binds, and which unwraps refuse at the load or the build.

## Motivation

An Optional is a sum, and `Int??` is a type of its own, so taking an Optional apart takes off one level, and only the language knows where a level is: the none and a some holding the none are two values of `Int??`. A front end with `if let` or `guard let` has nothing else in the live set to write it with. A plain cast to the payload's type fails with `cast_refused` where the value is the none, which makes the body one that may fail under [what a body may fail with](../WARP-26/SPEC.md) though the author has written what happens at the none, and a cast takes no level off at all.

## Rules

| key | takes | required |
|---|---|---|
| `of` | expression. Its reading is an Optional | yes |
| `then` | statements. Runs where `of` holds a some | no |
| `else` | statements. Runs where `of` holds the none | no |

An unwrap is a statement, and written with a `then` it **has no value**, the way a `conditional` does. It takes an Optional apart one level, under [types](../WARP-48/SPEC.md): where `of` holds `null` it takes the `else` way, and otherwise the `then` way, where the statement's own name binds the **payload** while `then` runs and nowhere after the unwrap. The payload is what a `Some` holds, and any other value itself, and it reads `T` where `of` reads `T?`. An unwrap written nameless binds no payload. The two ways meet past the unwrap as a conditional's arms do, a way not written as the way that wrote nothing. What `of` takes apart is an operand, read rather than run, under [procedures](../WARP-15/SPEC.md). An unwrap with neither `then` nor `else` **refuses at the load**, since no way through it reads what it takes apart, and an `of` whose reading is no Optional **refuses at the build**, since it holds no none to take apart.

**An unwrap written with no `then` has the payload past it**, its value, whether or not a name binds it, so a none has no way on: every way through `else` leaves, ending in a statement that never finishes under [nothing after a leave](../WARP-29/SPEC.md), and an `else` with a way that finishes **refuses at the build**, where whether a way ends in a statement whose call returns `Never` is known. A name, where one is written, holds the payload from the statement after the unwrap to the end of the statements it stands among.

## Interactions

- An unwrap whose ways both leave, and one with no `then`: [nothing after a leave](../WARP-29/SPEC.md).
- `?.` and `?[` read past every level at once: [null is not read through](../WARP-34/SPEC.md).
- `Standard.Optional.unwrapped`, written from `unwrap`: [`Standard.Optional`](../WARP-81/SPEC.md).

## Alternatives considered

## Notes
