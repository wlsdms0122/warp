# WARP-64: Names

Status: accepted

## Summary

A name is its declared spelling. The rules decide that a dot is only a character of a spelling, that procedures and types are two namespaces, that one spelling has one declarer, refused at the load within one document and at the build across two, and that a spelling no module declares refuses at the build.

## Motivation

A scope that tried a bare name in the document's own namespace and then globally would make which declaration a mention means depend on what else is declared, and the build could not write down what a document sends until that chain was resolved against the link. A front end resolves its own scopes and writes the full spelling.

## Rules

**A name is its declared spelling.** The key a document declares a type, contract or procedure under is the whole of its name: `Standard.Math.floored` is declared under that key, and `Wallet.Account` under that one. A mention is a declared spelling, written out, and it means the same declaration wherever it was written, inside the declaring document too. A spelling no module in the link declares **refuses at the build** where it is mentioned.

**A dot is a character of the spelling and nothing more.** The language has no nesting, no scope and no prefix, so what a document chooses to put before a dot is the author's convention, and one document may declare `Wallet.fee` beside `Bank.rate` while another declares `Wallet.rate`.

**There are two namespaces, procedures and types**, and a procedure may be spelled like a type. Procedures, members and contracts' procedures share the first, a member under its spelling under [members](../WARP-58/SPEC.md) and a contract's procedure under its spelling, which names one contract's procedure by *the grammar* in [names](../WARP-67/SPEC.md#the-grammar). Types and contracts share the second, and a case's spelling and a type member's spelling are names of it too, under [enums](../WARP-93/SPEC.md) and [associated types](../WARP-59/SPEC.md).

**One spelling has one declarer.** No spelling in either namespace stands for two declarations, so a mention reaches whatever declares it: a call reaches one procedure, a slot one type or contract, and a bound one contract. Two declarations under one spelling in one namespace, whichever kinds of it they are, **refuse at the load** where one document declares both, since the document decides that alone, and **at the build** where two documents each declare one, under *one spelling has one declarer* in [what the build decides](../WARP-66/SPEC.md). So one document declaring `(type App.Thing Int)` beside `(contract App.Thing)`, or a procedure under `App.Named.name` beside the contract `App.Named` asking `name`, refuses at the load, and the same two declarations split across two documents refuse at the build.

**Every name in the second namespace holds its grammar** under [names](../WARP-67/SPEC.md): a type or a contract declared holds a type's name's, a case's or a type member's spelling its own, a mention a mention's, and a type parameter's name its own: a document declares no type under `Int` and names no type parameter `Int`, a mention spelled `a b` **refuses at the load**, and a mention of `Int` is the type the language names.

## Interactions

- What a document mentions from elsewhere is listed under [the imports list](../WARP-10/SPEC.md).
- A member's spelling and a contract procedure's spelling are under [members](../WARP-58/SPEC.md) and [calling a contract's procedure](../WARP-63/SPEC.md).

## Alternatives considered

- A dot that reads a field or calls a procedure by what stands before it. Resolving such a short name needs a table over everything a document reaches, which widens what one document's build reads.
- Choosing a declaration by the types of its arguments. A front end that overloads writes a distinct spelling for each declaration, so the IR looks up one spelling once.

## Notes

**Note.** One document holds everything the load reads of it, so two declarations under one spelling in it are found there, and which documents stand beside it is known only at the build. This is the line a scope-less IR draws: LLVM IR and SIL refuse a redefinition within one module where they parse it, and a linker refuses a duplicate symbol across modules where it links them.
