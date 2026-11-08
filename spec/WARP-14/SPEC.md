# WARP-14: A native procedure

Status: accepted

## Summary

A native procedure is one the host implements, so no document holds its body. The rules decide how it is declared, that it declares the procedures it sends, and that those sends are held to the rest of what the declaration says.

## Motivation

A host's procedure has no text in any document, so a build knows of it only what the host declares, and a front end cannot write that declaration, since the code is in the host's language. Two runtimes reading different things from it would build one document two ways: `App.fresh` declares itself const and sends `App.clock`, which does not, and a document handing `Standard.Collection.filter` a closure that calls `App.fresh` would build in a runtime that reads only the signature and be refused in one that reads the sends. So the IR fixes what a native procedure declares, the procedures it sends among it, and what a runtime hands one.

## Rules

A native procedure is one the host implements, so no document holds its body, and a declaration in a document with no `body` is one whose body holds no statement. Its declaration is written as any other is in its module's interface, under *an interface* in [the text](../WARP-43/SPEC.md), which says nothing of how a declaration is implemented. The host's procedure arrives at the link in a module the host assembled in its own language, declared there under its spelling the way any declaration is, its return type, what it may **fail** with, whether it **touches** a name another body could touch at the same time and whether it is **const** among it, and beside that the **procedures it sends**, because there is no text to read them off. A **send** is a call the native procedure makes, declared before it runs:

| part | takes |
|---|---|
| spelling | the name of the declaration it reaches |
| count | how many arguments it hands, by position from the first, under [a parameter](../WARP-17/SPEC.md) |

A call reaches one of these the way it reaches any other declaration, and is judged against the declaration the same way.

**Its sends are held to the rest of what it said.** They are declared beside the signature in the module the host assembles, so the build reads them, and no document and no interface writes them: an interface says nothing of how a declaration is implemented, under [an interface](../WARP-43/SPEC.md), and an object writes them as the row's native implementation, under [rows](../WARP-87/SPEC.md). A native procedure **refuses at the build** where one of its sends:

- names a contract's procedure: which declaration satisfies one is a call's to say, by the type that fills `Self`, and a send has no call to read it from;
- reaches a `private` declaration of another document, under [who may name a declaration](../WARP-13/SPEC.md);
- reaches a procedure taking a parameter in place, under [a parameter handed in place](../WARP-18/SPEC.md);
- hands another count than the declaration it reaches takes: the send names its callee, so the build knows the count, under [a parameter](../WARP-17/SPEC.md);
- reaches one that does not declare itself const, where the native procedure declares itself const;
- reaches one that does not declare itself isolated, where the native procedure declares itself isolated, that it touches no name another body could touch at the same time.

A native procedure declaring itself const and implemented as one that reaches outside the run **refuses at the build** too, under *what a runtime hands one* below.

**Nothing else about a native procedure is checked.** One that reaches outside the run and says it does not has broken its contract, and the defect belongs to whoever put it in the link rather than to the program that called it, which is where its claim about what it touches is taken too.

**Note.** A link holds the code, not the text it was written as, and no reading of a built procedure says whether it asked the clock.

**What a runtime hands one is where the claim is kept.** A const procedure is handed what its call wrote, each a value with no type held beside it, a parameter handed in place as what it holds when the call is made, a way to send the procedures it declared, and a way to call a procedure it was handed. One that reaches outside is handed those and two more: a parameter handed in place as the caller's variable, read and written as it runs, and whatever the host keeps beside the program. Those two are what the first kind is refused.

**Note.** What a native procedure does with what it is handed is the host's code, and a case writes none of it. So a native procedure calling a procedure it was handed that takes a parameter in place, refused at the run, and what it hands a closure it was handed and writes through a parameter handed in place, fitted and judged at the door, are each held only by tests inside the implementation. A case's vocabulary declares a send by its spelling alone and picks how a procedure is implemented by its `const`, under [conformance](../WARP-1/SPEC.md), so a send handing another count and a procedure declaring itself const and implemented as one that reaches outside the run are each held only by tests inside the implementation too.

## Interactions

- What const means and permits, [WARP-15](../WARP-15/SPEC.md), and why a constant does not fold from a host's procedure, [WARP-16](../WARP-16/SPEC.md).
- Its sends hand their arguments by position, [WARP-17](../WARP-17/SPEC.md), are refused when they reach a `private` declaration of another document, [WARP-13](../WARP-13/SPEC.md), and never go to a procedure taking a parameter in place, [WARP-18](../WARP-18/SPEC.md).
- What it returns and writes is judged at the door: [WARP-71](../WARP-71/SPEC.md).

## Alternatives considered

- Checking a native procedure's claim by calling it twice and comparing the answers. A clock read to the second agrees with itself within a second and a procedure that caches always agrees, so the check misses what it is for, and one that sometimes catches a difference would make one build answer two ways.
- Calling a procedure const when it writes nothing through what the runtime hands it. A procedure that reads the clock writes nothing and still reaches outside the run, and folded into a constant it would put one reading of the clock into the compiled document.

## Notes
