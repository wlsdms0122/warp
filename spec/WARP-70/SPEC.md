# WARP-70: Order

Status: accepted

## Summary

A run has a fixed order. The rules decide that statements and the parts of an expression evaluate in position order, how keys and values walk in key order, when cancellation is observed, and that a leave travels out and is not a failure.

## Motivation

Take `(call App.pair (call Standard.Numeric.dividedBy a b) (call Standard.Numeric.remainder a b))` with `b` holding `0`: both arguments would refuse, and the run reports the refusal at `dividedBy`, the one standing first. An implementation free to take the arguments in another order would report another place for the same document and the same arguments.

A loop carries no budget of its own, so cancellation is how a host stops a run that does not end, and the places a run observes it are named so that every implementation stops at them.

## Rules

- Statements run in order; each binds its name in the scope of what follows.
- The parts of an expression are evaluated in **position order**, the first first, each to its end before the next begins, and the expression is evaluated after them:

  | expression | its parts, in order |
  |---|---|
  | a call | its arguments, whether the callee is a body or the host's |
  | a call of a value | its callee, then its arguments |
  | a list literal | its elements |
  | a dictionary literal | its entries in the order they stand, each key before its value |
  | a struct literal, a case literal | its fields, in the order of their names, under [expressions](../WARP-30/SPEC.md) and [enums](../WARP-93/SPEC.md) |
  | a cast, `as` or `as?` | the value it reads |

  A part may call anything, so the order is observable: two parts that would each refuse or fail surface the one standing first.
- `Standard.Collection.keys` and `values` return in the dictionary's **key order**, under [the value model](../WARP-3/SPEC.md), so a program that walks them gets the same walk on every run, and their cases stand under [Standard.Collection](../WARP-80/SPEC.md).
- **A run observes cancellation** between statements and at the entry to every round, including a round with an empty body. Once told, a run raises no catch: a failure met after the cancellation reaches the host as it is, and no catch body runs.
- Leaving (`return`/`break`/`continue`) travels out through whatever it is inside, and is not a failure: no catch takes it. It does not cross a closure's edge: `return` inside a closure returns from the closure.

**Note.** Cancellation needs a host with a lever, which a data case is not, so stopping is held only by tests inside the implementation.

## Interactions

- `Standard.Concurrent.first` stops the pieces it no longer waits for where a run observes cancellation, under [Standard.Concurrent](../WARP-83/SPEC.md).

## Alternatives considered

- A budget on a loop, a key bounding how many rounds it runs. An author's bound is already written with a counter and `abort`, under [Standard.Control](../WARP-82/SPEC.md), and a host stops a run by cancellation, so a budget the language kept would be a promise neither the author nor the host relies on.
- Leaving written as a failure, an `abort` that a catch takes to end a body early. A success would travel in the shape of a failure, and a catch would take a leave it cannot tell from one.

## Notes
