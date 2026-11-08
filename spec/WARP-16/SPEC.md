# WARP-16: What a constant folds from

Status: accepted

## Summary

Being const lets a procedure run at the build, but a constant must fold from something that does not depend on the host. The rules decide that a constant folds only from a body in another document of the link, a closure a constant of its own document holds, or a procedure the specification names.

## Motivation

A host's procedure that answers the device's locale is const within a run. Two hosts building one document from it would bake two constants into it, and nothing that keys a compiled document would tell them apart.

## Rules

**What a constant folds from.** Being const is what lets a procedure be run at the build. It does not decide *which* run's return value that is. A procedure reaches nothing outside the run it was handed and still returns one thing in one run and another in the next: a host brings a procedure that reads the device it is on, and every run of it inside a run agrees.

What a constant folds to is written into the compiled document, and a compiled document outlives the run that made it. It is kept, it is read again, and it may be made on one machine and read on another, where a procedure the host brought would answer for another device. So a constant folds from what the build runs without the host, which is three things and nothing else:

- a **body** in another document of the link, since the document it is written in is what the compiled document is made from. A body the constant's own document declares is still being resolved beside it, under *a constant-headed path* in [expressions](../WARP-35/SPEC.md);
- a **closure** a constant of its own document holds, called through that constant: the closure is a value written in the document the compiled document is made from, held to its signature where it is written, under [a parameter](../WARP-17/SPEC.md), and not a declaration still being resolved beside the constants;
- a procedure this specification **names**, under *what an implementation must write* in [the standard vocabulary](../WARP-74/SPEC.md), since an implementation writes it and no host brings it.

A call through a contract runs the member a claim is held to, and a document asks a contract of the claims within what it stands on, under [what a document stands on](../WARP-57/SPEC.md). So a constant folds through a contract only where the claim and the declaration backing it stand in documents the constant's document stands on, near or far: what it names, what those name, and the claims it imports. A constant whose call through a contract reaches a type with no claim for it within that reach **refuses at the build**, however the host handed the documents over, and so does one whose cast turns on such a type, one that would succeed were the type to conform to the contract, under [what a document stands on](../WARP-57/SPEC.md).

Folding a constant or a variable's start **refuses at the build** where the fold calls a procedure the host brought, whether its own expression calls it or a body the fold runs does. What the fold calls is what it ran: a call written on a way the fold did not take is not one. A **slot** asking a `const` procedure type and an **operand** are untouched: both are read while the program runs, and neither writes anything down.

**A value the build folds is written in a document.** A body in another document of the link is what a constant folds from, so a value baked in is a document declaring a procedure that returns it, which a constant elsewhere calls. The document is a document like any other: it has an identity, that identity stands among what a compiled document was built against, under *identity and dependencies* in [objects](../WARP-91/SPEC.md), and a value that moved is a build that moves with it. What the rule above turns away is a procedure in the host's own language, whose return value no document carries; a value written in a document is carried whole.

What folds at the build, a constant or a variable's start, folds to a value. A body run at the build may return a closure holding a variable of that run, and folding to one **refuses at the build** as well: the run is over when the build is, and a compiled document carries no box of it. Whatever stops one folding, a refusal the standard vocabulary gives at the run or a failure, which nothing there catches, **refuses at the build** too, whether or not anything reads the constant or the variable.

## Interactions

- Const, which this narrows: [WARP-15](../WARP-15/SPEC.md).

## Alternatives considered

- Judging a fold by every call written in the bodies it reaches, the way a const body is judged by what it reaches under [WARP-15](../WARP-15/SPEC.md). The rule is about what the compiled document carries, and a call the fold did not make put nothing in it.

## Notes
