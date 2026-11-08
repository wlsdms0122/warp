# WARP-28: `return`, `break` and `continue`

Status: accepted

## Summary

The leaves of a body are return, break and continue. The rules decide what each takes, which loop a name reaches, and which uses refuse at the load.

## Motivation

A front end cannot write a leave in place with what else the live set has. Answering from inside a loop without `return` means holding the answer in a variable read as `T?` and casting it after the loop, which adds `cast_refused` to what the procedure may fail with. Ending a loop or a round without `break` and `continue` means rewriting the statements after the leave and the condition of every loop around it.

## Rules

| key | does | takes |
|---|---|---|
| `return` | returns from the enclosing procedure here | an expression, what it returns, or `null`, `{ return: null }`, the text `(return)`, to return nothing |
| `break` | ends a loop | `null` for the nearest enclosing loop, or the statement name of a loop further out, a value's name under [names](../WARP-67/SPEC.md) |
| `continue` | ends the round and goes on to the next | as `break` does |

The return value must fit what the procedure declared, and it is the only way a body returns a value, under *a procedure* in [procedures](../WARP-12/SPEC.md). A `break`'s or a `continue`'s name is for reaching past the nearest: one naming the nearest says what naming none says, and a document says each thing one way, so it **refuses at the load**. A `break` and a `continue` reach the loops around them within the body of the procedure or closure they are written in, and no loop outside that body: a closure runs away from where it was written, so the loops around the writing are not around the running. One with no such loop around it, and one naming a loop that is none of them, **refuses at the load**.

## Interactions

- The loop a leave ends, and a loop with no `while`: [`loop`](../WARP-24/SPEC.md).
- What may follow a leave: [nothing after a leave](../WARP-29/SPEC.md).

## Alternatives considered

- A closing expression that answers a body, a `result` at its end. A front end writes it in place as a `return` of that expression.
- A branch to a label. A structured branch is another spelling of these leaves, and one that may go anywhere breaks the checks that trust the tree's structure.
- Leaving early by failing, with `Standard.Control.abort` under a `try`. A way that succeeds would read as one that failed.

## Notes
