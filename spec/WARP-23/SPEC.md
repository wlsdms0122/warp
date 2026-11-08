# WARP-23: `conditional`

Status: accepted

## Summary

A conditional chooses a way through a body by a Bool condition. The rules decide its when, then and else keys, that it has no value and takes no name, and that both arms are checked whether or not they are taken.

## Motivation

Running one of two bodies is the IR's, because nothing else in the live set does it. `Standard.Logic.select` chooses between two values, and both are read before it chooses, so `if ok { send() } else { log() }` written through it would run both calls. Each arm written as a closure, handed to a procedure that runs one, would make each arm a procedure of its own: a `return` in it returns from the closure, and a `break` in it reaches no loop around the writing, under [leaves](../WARP-28/SPEC.md). `{ conditional: { when: { ref: "ok" }, then: [ … ], else: [ … ] } }` runs one arm in the flow it is in.

Both arms are checked whether or not a run takes them, so that whether a document builds does not depend on which way a run goes.

## Rules

| key | takes | required |
|---|---|---|
| `when` | expression. Must be a `Bool` | yes |
| `then` | statements | yes |
| `else` | statements | no |

A conditional is a statement: it **has no value**, and it **takes no name**. The condition chooses a way through the body. An arm is statements. What an arm keeps it writes to an outer variable with `set`, and a value leaves the procedure through `return`. Both arms are checked whether or not they are taken.

## Interactions

- What a variable reads as after the arms: [WARP-68](../WARP-68/SPEC.md).
- Its `when` is an operand, held to const: [WARP-15](../WARP-15/SPEC.md).
- Choosing a value in an operand is `Standard.Logic.select`: [WARP-76](../WARP-76/SPEC.md).

## Alternatives considered

## Notes
