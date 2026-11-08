# WARP-24: `loop`

Status: accepted

## Summary

A loop runs rounds while its condition is true. The rules decide its keys, what the round binding is, when a nameless loop binds nothing, and that a loop written with no while does not finish.

## Motivation

A loop that does not finish is the IR's to say, because a front end cannot write it in place with anything else the live set has. A procedure that serves until its host cancels it loops with no `while` and says `returns Never`. Without a loop that declares it does not finish, a front end has no honest lowering: a `return` after the loop needs a value of the procedure's return type, which a body returning `some T` does not have; ending with `Standard.Control.abort` makes `aborted` part of what the procedure and every caller may fail with; a helper declared `returns Never` has the same problem one call down; and holding the answer in a `T?` variable and casting it after the loop adds `cast_refused`.

The round is the language's because counting rounds in place would take a variable and a call to `Standard.Numeric.plus` in every body, and a vocabulary call is not an IR form, so a counter a front end writes is not a rewriting in place.

## Rules

| key | takes | required |
|---|---|---|
| `while` | expression. Must be a `Bool`. Runs another round while true | no |
| `body` | statements | yes |

A loop is a statement: it **has no value**, the way a `conditional` does, and what a round keeps it writes to an outer variable. The loop's own statement name binds the round it is on, a `Round`, a struct the language declares as `{ struct: { index: Int } }`, readable where the loop speaks, the `while` condition and the `body`, and nowhere after the loop. A loop written nameless binds no round: a `break` or `continue` naming no loop still ends it, and one naming a loop passes through it. The condition reads the state before the round it would start, so `round.index` there is how many rounds have finished.

**A loop written with no `while` does not finish.** Leaving out `while` declares it: a round runs after every round, and only a leave reaching past the loop ends it, a `return` or a `break` or `continue` naming a loop further out. A `continue` of it starts the next round, and a `break` that would end it, one naming no loop included, **refuses at the load**. It never finishes, so nothing may follow it, and a body ending in one leaves on every way through it. A loop written with `while` may finish whatever its condition reads: `(while true)` is one, and a `break` ends it.

Bounding a loop is the author's to write, with a counter in its condition, and stopping one is the host's **cancellation**, under [running](../WARP-70/SPEC.md).

Walking a collection is this construct too: the round is read against the collection's count and the element is read at that index, so what a walk needs beyond a loop is `Standard.Collection.count`, a comparison and an index.

Running things at once is **vocabulary**: `Standard.Concurrent`, under [the standard vocabulary](../WARP-83/SPEC.md).

**Note.** A closure is the one body that is safe to run beside another, and "takes closures" is a thing a signature can say. A loop's body writes the enclosing names, which no signature can say. So a walk whose rounds write outward or lean on the round before is a loop, and one where each element's work stands alone is a procedure (`Standard.Collection.map`, `filter`, `Standard.Concurrent.map`), which is what lets the concurrent `map` run it at once.

## Interactions

- Which loop a `break` or `continue` ends: [leaves](../WARP-28/SPEC.md).
- A loop written with no `while` as a leave nothing may follow: [nothing after a leave](../WARP-29/SPEC.md), and as a way a procedure that writes `returns` leaves: [a procedure](../WARP-12/SPEC.md).
- `Round`, a struct the language declares: [what the language declares](../WARP-61/SPEC.md).

## Alternatives considered

- A loop with a result, a value the loop answers when it ends. What a round keeps is written to an outer variable, which a front end writes in place, so a result adds nothing the IR cannot already say.
- Reading `(while true)` as a loop that does not finish. That reads the value of an expression, which is inference, and a line would then be owed for every other expression that reads `true`.
- Deriving whether a loop finishes from whether its body holds a `break` that ends it. That fills a fact in from the body, and the IR holds the fact as a declaration the build checks the body against.

## Notes
