# WARP-43: An interface

Status: accepted

## Summary

An interface is the declarations of one module or more without their implementation. The rules decide how it is written in the text, which declarations it holds, and that a procedure written in Warp and one the host implements are declared alike.

## Motivation

A front end writes calls into modules it does not hold, the standard vocabulary's and a host's, and has to know their signatures without knowing which runtime will run what it writes. A front end reads the interface or bakes it into a form of its own, a runtime checks its own modules against it, and the two meet in the file and know nothing else of each other.

## Rules

An **interface** is the declarations of one module or more without their implementation: the types, contracts and claims they declare, and each procedure's signature. A front end reads an interface to write calls into its modules. It says nothing of how a declaration is implemented, so a procedure written in Warp and one the host implements are declared alike. The standard vocabulary's is [`lib/standard/interface/standard.interface.warpt`](../../lib/standard/interface/standard.interface.warpt), under [the standard vocabulary](../WARP-74/SPEC.md), and a host declares modules of its own the same way.

```
(interface 1)
(import Standard.Comparable)
(struct App.Range (field low Int) (field high Int))
(contract App.Named (procedure name (parameter of (type Self)) (returns String)))
(extension (head Int) (satisfies App.Named) (procedure name (parameter of (type Int)) (returns String)))
(procedure App.largest (parameter of (type (array (some T Standard.Comparable)))) (returns (optional (some T))))
```

- It is written in a document's nodes, `(interface 1)` in the place of `(warp 1)`, and its tree is a document's tree with `interface` in the place of `warp`: the language version its declarations are written for.
- It holds what another document may name, the keys of the table below, each as a document holds it under [the document format](../WARP-8/SPEC.md). A constant and a module variable are private to their document, so it writes no `const` and no `var`.
- A procedure, a member included, is its signature's nodes, as a contract's procedure is. It writes no `body`, since an interface implements nothing, and no `access`, since what it declares is what another document may send.
- It is written one way, as a document is, under *a document says each thing one way* in [the document format](../WARP-11/SPEC.md). An interface writing a document's `const` or `var` key, or a procedure in it, a member and an extension's procedure included, writing a `body` or an `access`, **refuses**. A procedure's `(const)` and `(isolated)` are its signature's, and an interface writes them as a contract's procedure does.

| key | takes | required |
|---|---|---|
| `interface` | int. The language version its declarations are written for, in the place of a document's `warp` | yes |
| `imports` | array of strings, as a document's: the types and contracts its declarations name and it does not declare | yes, and empty where they name none |
| `types` | as a document's | no |
| `contracts` | as a document's | no |
| `extensions` | as a document's, each procedure its signature | no |
| `procedures` | as a document's, each procedure its signature | no |

**Note.** An implementation brings modules whose declarations are the ones their interface gives, so that a call a front end wrote against the interface is a call those modules take. How it checks its modules against the interface is its own, and no case holds it.

## Interactions

- A case's `vocabulary` is written the same way: [a case, in the text](../WARP-44/SPEC.md).

## Alternatives considered

- A front end reading a runtime's modules for their declarations. The front end would then know the runtime, and it cannot know which runtime will run what it writes.
- A prose table of signatures copied by hand into each front end. A difference between the table and a runtime would show only when a front end's output ran.

## Notes
