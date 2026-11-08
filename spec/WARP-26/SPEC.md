# WARP-26: What a body may fail with

Status: accepted

## Summary

What a body may fail with is declared and known before it runs. The rules decide how failing is written, which failures a body has through its casts, calls and catches, and that failing with more than the declaration names refuses at the build.

## Motivation

The declaration is what a caller, a contract and a host read. A native procedure has no body to check, so for it the declaration is the only place the fact can be.

## Rules

**What a body may fail with is declared, and known before it runs.** A declaration and a closure literal name it under `failing`, written as [a procedure](../WARP-12/SPEC.md) writes it, each name the type a failure names itself by (`aborted`, `cast_refused`), and a body failing with more than its declaration names **refuses at the build**. A body fails with what its plain casts fail with (`cast_refused`, the one failure the runtime itself raises, and an asking cast none, under [a cast](../WARP-32/SPEC.md)), with what the declarations it calls say they fail with, and with whatever its catches fail with, the body under a catch being caught. Calling a value fails with what the type written for it says it may fail with, by the rule under *a const procedure* in [procedures](../WARP-15/SPEC.md), since nothing before the run says which value. A value called where that rule writes no type for it, a variable that writes no type among them, may fail with anything, as `failing: anything` says under [a procedure](../WARP-12/SPEC.md): no declaration says less of it.

A native procedure says what it may fail with the same way. **A procedure that says nothing fails nothing**, which is right for the many procedures that throw only at an author mistake, and a procedure that can fail says so. `Standard.Control.abort` says `aborted`; `Standard.Concurrent` says `concurrent_failed`, every piece's failure being gathered into that one. A piece that refuses at the run refuses the whole run instead, under [running](../WARP-73/SPEC.md), and the failures beside it are not gathered. A procedure that fails and does not say so has broken its contract, the same way one that holds state and calls itself isolated has.

## Interactions

- The `throws` spelling of a procedure type: [how a type is written](../WARP-46/SPEC.md).
- Leaving out `failing` and writing an empty one: [a procedure](../WARP-12/SPEC.md).
- A catch over a body that cannot fail: [`try`](../WARP-25/SPEC.md).
- `cast_refused` and `as?`: [a cast](../WARP-32/SPEC.md).

## Alternatives considered

- The build deriving what a body may fail with from the body. Inference that stands in for a declaration is a front end's convenience in writing the IR. A front end that wants it left unwritten fills it in where it writes the procedure.
- A procedure that fails with whatever a procedure handed to it fails with. It is an axis `const` and `isolated` do not have. The standard vocabulary gives such a procedure two names instead, one taking a procedure that fails with nothing and one taking a procedure that may fail, under [a procedure that takes procedures runs them](../WARP-75/SPEC.md).

## Notes

**Note.** A procedure type names a fixed list of failures, so a contract cannot declare a procedure that forwards whatever its callback fails with; its failure list is written out.
