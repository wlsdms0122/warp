# WARP-13: Who may name a declaration

Status: accepted

## Summary

The access of a declaration says from where it may be named: private from its own document, internal from every document in the link, public from the link and the host. The rules decide that a run starts from a public declaration only and that a call reaching a private declaration of another document refuses at the build.

## Motivation

Without access, every procedure a document declared would be an entry a host could start from, and a document could not change a helper without breaking whatever named it from elsewhere.

## Rules

A declaration is named from inside its scope and refused from outside it. Three scopes, and `access` says which:

| `access` | named from |
|---|---|
| `private` | the document that declares it |
| `internal` | every document in the link |
| `public` | the link, and the host that assembled it |

A declaration that writes nothing is `internal`: what a document declares is the program's, and only what says so is the host's. A run starts from a `public` declaration and from no other: the host names one when it starts the run, and naming one that is `internal` or `private` **refuses at the run**, before anything runs, the way naming one nothing declares does. A call standing in one document that reaches a `private` declaration of another **refuses at the build**, at the call, and so does a native procedure whose declared sends reach one. A `private` declaration takes no spelling from the link: its own document reaches it, and two documents may each declare one under one spelling, where two declarations any other document could name **refuse at the build** under [what the build decides](../WARP-66/SPEC.md). A `private` declaration backs no claim: a contract is how a document that never names a declaration calls it, so a claim it would back does not hold, and refuses at the build, at the claim, the way a claim nothing backs does. A native procedure declared `private` in a module the host assembled with no document **refuses at the load**: `private` names a document, and there is none. `access` written as any other value **refuses at the load**.

A constant and a module variable are the document's own and write no `access`, under [the module](../WARP-8/SPEC.md): a name is a scope question, and another document reaches either only through a procedure declared beside it.

A declaration's `access` travels with it: an object writes it on the row, under [rows](../WARP-87/SPEC.md), and a document compiled against another reads it there. Nothing else about a declaration moves with it. What it takes and returns, and what it sends, are judged the same whoever may name it.

**Note.** A case's vocabulary stands as a document of its own, under [conformance](../WARP-1/SPEC.md), so a `private` native procedure in a module the host assembled with no document, refused at the load, is held only by tests inside the implementation.

## Interactions

- The entry a case runs from is `public`: [WARP-1](../WARP-1/SPEC.md).

## Alternatives considered

## Notes
