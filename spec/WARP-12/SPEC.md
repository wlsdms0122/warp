# WARP-12: A procedure

Status: accepted

## Summary

A procedure declaration says everything a call may expect of it. The rules decide its keys and their defaults, namely access, parameters, returns, failing, const and isolated, and that the build holds the body to what the declaration says.

## Motivation

A call is built against a declaration, often one in another document or one a host implements. If the build read a return type, the failures, constness or isolation off the body, a change inside one body would change what every caller may do without its declaration changing, and a native procedure, which has no body, could not be read the way a document's is.

## Rules

What a declaration says about itself, and what saying it permits. This WARP gives a declaration's form. Who may name one is [who may name a declaration](../WARP-13/SPEC.md), one whose code the host implements is [a native procedure](../WARP-14/SPEC.md), what `const` means and where that claim is spent is [a const procedure](../WARP-15/SPEC.md), and what a parameter takes is [a parameter](../WARP-17/SPEC.md). A declaration says everything a call may expect of it, and the build holds its body to what it says.

| key | takes | required |
|---|---|---|
| `access` | `public`, `internal` or `private`: who may name the declaration, under [who may name a declaration](../WARP-13/SPEC.md). `internal` when absent | no |
| `parameters` | list of parameters, in the order the declaration writes them, which is the order every call hands its arguments in | no |
| `returns` | type. What a call returns. Absent, a call returns null: `Null` is what a procedure returning nothing returns | no |
| `failing` | what may come out of a call when the work goes wrong: a list of the failures' names, each a failure's name under [names and their grammar](../WARP-67/SPEC.md), in name order and each once, as a procedure type's `throws(…)` lists them under [how a type is written](../WARP-46/SPEC.md), or `anything`, which names none. Absent, nothing may | no |
| `const` | `true`: the procedure is const, under [a const procedure](../WARP-15/SPEC.md) | no |
| `isolated` | `true`: a call touches no name another body could touch at once, under [concurrency is isolation, and it is granted](../WARP-73/SPEC.md) | no |
| `bounds` | dictionary: an associated type of a type parameter, `T.Item` → a `bound` under *the grammar* in [how a type is written](../WARP-46/SPEC.md#the-grammar), its names in name order, each once. A type parameter is bounded beside the first `some T` the slots write, `some T: Standard.Comparable`, so a key naming one **refuses at the load**, and so does one standing on a parameter no slot mentions, under [bounds](../WARP-52/SPEC.md) | no |
| `sameTypes` | dictionary: an associated type of a type parameter, `T.Item` → the type it is, under [the associated types of a type parameter](../WARP-60/SPEC.md) | no |
| `body` | statements | no |

**A procedure returns through `return`.** One that writes `returns` leaves on every way through its body, by a `return`, by a call returning `Never` or by a loop written with no `while`, which does not finish, and a way that reaches the end of the body **refuses at the build**, under [what the build decides](../WARP-66/SPEC.md). One that writes no `returns` returns null when its body reaches its end.

**What a declaration leaves out says the least.** A call reads the declaration and nothing else, so nothing a declaration leaves out is read off its body: a body returning more than `returns` admits, failing with more than `failing` names, or doing what `const` or `isolated` says it does not, **refuses at the build**, under [what the build decides](../WARP-66/SPEC.md). What leaving a key out says is not written, and `failing` is kept in name order, each failure once, under [a document says each thing one way](../WARP-11/SPEC.md). `failing` written as anything but a list of names or `anything` **refuses at the load**, and so does a failure's name that does not hold its grammar under [names and their grammar](../WARP-67/SPEC.md), in `failing` and in a procedure type's `throws(…)` alike.

## Interactions

- What a parameter takes: [WARP-17](../WARP-17/SPEC.md).
- A declaration with no body: [WARP-14](../WARP-14/SPEC.md).
- What absence says, and the keys written as it: [WARP-11](../WARP-11/SPEC.md).

## Alternatives considered

- Reading what a declaration leaves out off its body: a return type, the failures, constness or isolation inferred. Inference is a convenience a front end has when it writes the IR.
- A body ending in a value, a last expression a body answers with. A front end writes it in place as a `return`, and the IR keeps one way to answer.

## Notes
