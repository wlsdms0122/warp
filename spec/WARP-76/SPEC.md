# WARP-76: Standard.Logic

Status: accepted

## Summary

Standard.Logic is the bundle of equality, negation and the short-circuit procedures. The rules decide what equal, not, and, or and select return, that sides are procedures read in order, and that nothing after the deciding side is evaluated.

## Motivation

A program has no operator for equality, negation or choice, so every condition it tests and every value it chooses is a call. A connective that ran every side would make `and` of a bounds test and the read it guards refuse on the very input the test excludes, so the sides are procedures, and the order they are asked in is part of the answer.

## Rules

| procedure | parameters | returns |
|---|---|---|
| `equal`, `notEqual` | `lhs`, `rhs` | whether the two are one value, and whether they are not |
| `not` | `value` | the other `Bool` |
| `and`, `or`, `tryAnd`, `tryOr` | `conditions`, the sides, each a procedure taking nothing, so one returning anything but a `Bool` **refuses at the build** where it is handed | whether every side returns `true`, and whether some side does. Over nothing, `and` and `tryAnd` return `true` and `or` and `tryOr` return `false`: no side decided the result, so the chain's own result stands |
| `select`, `trySelect` | `condition`, `then`, `else`, the two sides each a procedure taking nothing | what the side `condition` chooses returns |

`and` and `or`, and their twins, take procedures precisely so they need not run them all: the sides are read in order and the procedure stops at the first side that decides the result. The first false, the first true. What follows the stop is never evaluated. `select` takes them for the same reason and asks exactly one: the side not chosen never runs, so a side that would refuse is no refusal of the call. `equal` and `notEqual` decide by the value model's one sameness, and `not` turns a `Bool` around.

**`select` is how an operand chooses.** A `conditional` has no value, under [statements](../WARP-23/SPEC.md), and an operand is read rather than run, so choosing among values inside one is a procedure here rather than grammar. The two sides return one type, worked out from the call the way any type parameter is, so two sides returning two types neither takes **refuse at the build**, under [type parameters](../WARP-51/SPEC.md).

## Interactions

- `equal` decides by the sameness of [when two values are the same](../WARP-4/SPEC.md), and is the one builtin of the bundle under [the standard vocabulary](../WARP-74/SPEC.md).
- `tryAnd`, `tryOr` and `trySelect` are the twins of [WARP-75](../WARP-75/SPEC.md).
- `Standard.Optional.unwrapped` takes its fallback as a procedure for the reason `select` does, under [Standard.Optional](../WARP-81/SPEC.md).

## Alternatives considered

## Notes
