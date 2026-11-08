# WARP-17: A parameter

Status: accepted

## Summary

A parameter is a dictionary with a name and an optional type. The rules decide how a parameter and a closure's signature are written, that a missing type means Any, that duplicate names refuse at the load, and the one calling convention that arguments follow.

## Motivation

If each way a procedure is called matched arguments to parameters its own way, one closure would be handed different things depending on who called it, and a closure written for `Standard.Collection.map` could not be called from a document.

## Rules

Written as a dictionary, one per entry of `parameters`:

| key | takes | required |
|---|---|---|
| `name` | string. The name the body reads the argument by | yes |
| `type` | type | no; absent means `Any`, and `Any` written out **refuses at the load**, since leaving it out says it |

A closure literal, its keys under `closure` in [expressions](../WARP-30/SPEC.md), writes its signature the way a declaration does, and what it leaves out says the least, wherever it is written: the place it stands in completes nothing, and a closure that writes no `returns` returns null. Its body is held to its signature where it is written, and the place takes the closure by the procedure type the signature is, under *what a slot takes, exactly* in [types](../WARP-48/SPEC.md).

The name is the declaration's own, and a closure literal's names are its own the same way. A procedure type carries the types in position order and no names, under [types](../WARP-46/SPEC.md), so two closures naming their parameters differently are one type where the types agree. Two parameters under one name **refuse at the load**.

**One calling convention.** Lowering puts every parameter in a slot, in the declaration's order, and every call a program or a procedure makes hands its arguments **by position**: a `call` to a declaration, a `call` of a value, a procedure handing values to a closure it was given, and a native procedure sending one it declared. The host hands a run's entry its arguments by name, under [where a run starts](../WARP-69/SPEC.md), and each fills the slot of the parameter it names. A call hands exactly as many arguments as the callee takes. Any other count **refuses**, at the build where the callee is known and at the run otherwise. An argument the parameter at its position does not take **refuses at the build**, and the run judges one only where a value from outside is handed, under [running](../WARP-71/SPEC.md). A call through a contract picks its row by the type that fills `Self`, under [types](../WARP-63/SPEC.md), and hands the arguments on as they are. In a `call` of a value, a type parameter the slot holding the value names at a position is the body's own, which no call of the value fills, so what stands there is a value of it already, the way a write into a box of it is, and anything else **refuses at the build**. Writing an argument is giving it: an argument holding null was given, and a slot takes it where `null` is a value of its type: `Null`, `Any`, an Optional as its none, a type parameter, which stands for what arrived.

**Note.** Wherever a body writes a call, the build knows the callee's count: a value whose type writes no parameters is called only once a cast says what procedure it is, under [a parameter handed in place](../WARP-18/SPEC.md), and the cast judges the procedure type, its count among it, before the call, under [what a slot takes, exactly](../WARP-48/SPEC.md). The count is judged at the run only where host code calls a value it was handed, so the run's refusal of another count is held only by tests inside the implementation.

## Interactions

- A parameter handed in place: [WARP-18](../WARP-18/SPEC.md).

## Alternatives considered

- A parameter `default`, a value the declaration fills where a call writes nothing. A parameter that takes an Optional and a body that reads null as the default does the same, and a front end that sees the declaration fills a default at the call. The IR holds only calls written in full.

## Notes
