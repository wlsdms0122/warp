# WARP-29: Nothing after a leave

Status: accepted

## Summary

Nothing may be written after a leave in the same body. The rules decide that this holds through conditionals, tries, unwraps and loops whose every way leaves, and after a call returning Never, and at which stage each is held.

## Motivation

Failing on purpose is declared `returns: Never` because `Never` is the type no value has. Joined with any other reading it gives that reading, so a way that fails does not widen what the other ways read, and a call to it ends the reading of a body where it stands.

## Rules

Nothing may be written after a statement that **never finishes**, among the statements it stands in: it would never run, and the name it would bind would never bind. A statement never finishes by its form, and the rule reaches through structure, because the fact does:

| statement | never finishes where |
|---|---|
| `return`, `break`, `continue` | always: it is a leave |
| `loop` | it is written with no `while` |
| a statement whose `value` is a call | the procedure it calls returns `Never`, by the callee's `returns` or by the return type the type written for a called value says, an alias of `Never` included |
| `conditional` | both its arms end in a statement that never finishes |
| `try` | its body and its catch both do |
| `unwrap` | its `then` and its `else` are both written and both do |
| `switch` | every arm, and its `default` where one is written, does, under [enums](../WARP-95/SPEC.md#switch) |

Any other statement may finish, however its other ways end: a conditional with no `else`, a loop written with `while`, a try whose body or catch may finish, an unwrap with no `then` or no `else`, and a switch with an arm or a `default` that may finish among them. A call returning `Never` written inside a statement's `value`, as an argument or an element, ends the evaluation it stands in, under [what a slot takes](../WARP-48/SPEC.md), and does not make the statement one that never finishes.

**The stage follows what the judgement reads.** Where the statement that never finishes is a leave, a loop written with no `while`, or a construct whose ways all end in those, the tree shows it, and a load is what one document decides alone, so a statement written after it **refuses at the load**. Where a way ends in a call, whether it returns `Never` is the callee's signature, judged at the build whichever document declares the callee, so a statement written after it **refuses at the build**.

Failing on purpose is a procedure, `Standard.Control.abort` under [the standard vocabulary](../WARP-82/SPEC.md), declared `returns: Never`: the signature says everything checking it needs.

## Interactions

- Every way through a body that writes `returns`: [a procedure](../WARP-12/SPEC.md).

## Alternatives considered

## Notes
