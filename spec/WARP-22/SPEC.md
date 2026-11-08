# WARP-22: Calls

Status: accepted

## Summary

A call is an expression that sends a procedure by its spelling or calls a value. The rules decide the procedure and arguments keys, what a called value must read as, and that a body to run travels as a closure argument.

## Motivation

A call is how a document reaches the vocabulary. Every effect a program has is a procedure the host or this specification brings, so a front end lowering `count(items)` or `apply(f, 1)` has nothing else to write it with. `{ call: { procedure: "Standard.Collection.count", arguments: [{ ref: "items" }] } }` names the declaration by its spelling, so every runtime sends the same one, and `{ call: { procedure: { ref: "f" }, arguments: [1] } }` runs a closure the body was handed. Which declaration a spelling names, and what a value must be read as before it is called, are what two runtimes would otherwise answer differently.

## Rules

A call is an expression, `{ call: … }`, written wherever a value is wanted and as a statement's `value`. A procedure called, by its spelling or as a value:

| key | takes | required |
|---|---|---|
| `procedure` | a string names the declaration called, resolved at the build. Any other expression is a value the run calls, and a value whose reading writes no parameters, `Procedure`, `Any`, a type parameter or a contract, **refuses at the build**, since only a cast says what procedure it is, and so does one whose reading is an Optional: null is not called through, the way it is not read through, at the build where the reading is an Optional and at the run where a null arrives that the reading does not show. A string is never a value a call could take, so the two readings never meet | yes |
| `arguments` | list of expressions, by position: the first fills the first parameter, and so on, one for each parameter, under *one calling convention* in [procedures](../WARP-17/SPEC.md) | no |

A body a procedure is to run travels as a **closure argument**, like any other value.

## Interactions

- A path reads a name and does not call: [WARP-33](../WARP-33/SPEC.md).
- A call through a contract picks its row by `Self`: [WARP-63](../WARP-63/SPEC.md).

## Alternatives considered

- A path segment that sends a procedure, `items.count` reading a field where there is one and calling a procedure otherwise. Resolving which procedure a bare segment names takes a table built across everything a document reaches, so one shortening widens what a build must read, and such a segment does nothing a call does not. A shorter spelling is a front end's.

## Notes

**Note.** No case holds the run half of null not being called through. A value is held to its type at every door, and a value read as `Any`, `Procedure`, a type parameter or a contract is not called at all, so no document is known that calls a null its reading does not show. The half is written so that an implementation meeting one refuses rather than calls through it.
