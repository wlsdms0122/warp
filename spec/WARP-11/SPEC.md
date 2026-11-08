# WARP-11: A document says each thing one way

Status: accepted

## Summary

One program has one document. The rules decide which second spellings of a document reading refuses at the load, such as writing what an absence already says, so that a document that has been read and written is the document that was read.

## Motivation

A document's identity is the digest of its bytes, and what is compiled from it is kept under that identity. If `(access internal)` and no `access` at all were two documents of one program, everything keyed by identity would treat the program as two.

## Rules

A program has one document. Reading **refuses at the load** a document that says what it says another way, so a document that has been read and written is the document that was read, and one program never stands under two identities. A writer gives each program its one document by these rules; every other rule of form is the grammar's, in the WARP that writes it.

- **What its absence says is not written.** A key a document may leave out is left out where it would say what its absence says, which the table writing the key gives: a procedure's `access`, `returns`, `const` and `isolated` under [a procedure](../WARP-12/SPEC.md), a parameter's `type` under [a parameter](../WARP-17/SPEC.md), and a `var` statement's `value` under [a statement](../WARP-19/SPEC.md). So is a key that would hold an empty list or an empty dictionary: a signature's `parameters`, `failing`, `bounds` and `sameTypes`, a call's `arguments`, a procedure's `body`, a conditional's `else`, an unwrap's `else` beside a `then`, a struct's or an enum's `typeParameters`, `satisfies`, `types` and `procedures`, an arm's `binds`, a contract's `types` and `procedures`, an extension's keys, and the document's own `importedClaims`, `const`, `var`, `types`, `contracts`, `extensions` and `procedures`; an extension giving nothing is not written, under [members](../WARP-58/SPEC.md). An arm's `then` and a switch's `default` are written empty where they hold nothing, under [a switch](../WARP-95/SPEC.md): an arm holds its `then`, and an empty `default` says what its absence does not. `imports` is written whatever it holds, under [the imports list](../WARP-10/SPEC.md).
- **A list the document keeps in name order is written in it, each entry once**, compared by bytes: `imports`, each by the string it is written as; `importedClaims`, by the type and then by the contract; `satisfies` and `failing`; and a contract's `types`, each by the name it introduces whatever bound it writes. Every other list keeps the order it is written in, since the order is what it says: `parameters`, `arguments`, statements, a struct's `typeParameters`.
- **What is given a struct the document declares is written in its declaration**, under [members](../WARP-58/SPEC.md).
- **A bound stands where the name it bounds is introduced**, under [bounds](../WARP-52/SPEC.md).
- **A statement writes its expression under `value`**, a construct there as a dictionary of its one key, `{ value: { loop: … } }`, beside its binding and the `type` it declares, under [a statement](../WARP-19/SPEC.md). A `break` or `continue` names no loop where it ends the nearest one, under [`return`, `break` and `continue`](../WARP-28/SPEC.md).
- **A type and a path are written in their one spelling**: a type under [how a type is written](../WARP-46/SPEC.md), an extension's key as its head's type is, and a path under [a path](../WARP-31/SPEC.md#the-grammar).

## Interactions

- What a document's identity is and what it keys: [WARP-91](../WARP-91/SPEC.md).
- The binary's one spelling of a value, which this extends to the program's own forms: [WARP-5](../WARP-5/SPEC.md).

## Alternatives considered

## Notes
