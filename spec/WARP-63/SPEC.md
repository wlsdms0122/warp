# WARP-63: Calling a contract's procedure

Status: accepted

## Summary

A body calls a contract's procedure by writing the contract's name and the procedure's with a dot between them. The rules decide that the type filling Self picks the declaration, that the build builds a table with one call lowered per conforming type, and that the run reads it.

## Motivation

A generic body, or one holding a value of a contract, calls a procedure whose declaration depends on a type it does not know where it is written. The contract's spelling says which contract is meant and the type filling `Self` says which declaration runs, so one spelling reaches every conforming type, as a call through a Swift protocol requirement reaches the witness of the type it is called on. The build gathers every conforming type into one table and shows, before anything runs, that each declaration in it takes what the call hands and returns what the call reads.

## Rules

**A body calls a contract's procedure by writing its spelling**, under [names](../WARP-67/SPEC.md#the-grammar): `App.Describable.describe`. That spelling is the contract's declaration of the procedure, and it is a send like any other: a document calling a contract another module declares lists the spelling in `imports`. It names no type's declaration, and what it means is decided by the type that fills `Self` at its first position, so a call writing nothing there **refuses at the build**, as any call handing its declaration fewer arguments than it takes does, under [what the build decides](../WARP-66/SPEC.md). What a call hands it and what it returns are the contract's, not any one declaration's.

**The build builds the table and the run reads it.** For every contract, the build gathers every type that conforms to it and lowers one call per type, each against the row that backs it, arguments in that row's own slot order. The build writes the type each position of the procedure reads as at the call, the contract's type parameters, `Self` among them, filled as the call fills them, and each may name a type parameter of the body the call stands in. The run reads those types, each such parameter as the call it runs in filled it, and picks by the name of the first, the type that fills `Self`. A reading of a contract there is read as the type the value standing first holds, and the row takes the value. An Optional's reading is picked by the name `Optional`, whatever value stands first. The row picked is handed what fills its type parameters as its parameters read them off those types, as any call fills them. Nothing is resolved while a program is running.

**A declaration satisfying a contract's procedure is reached through the contract**, which is the spelling that says which contract is meant. Two types satisfying one procedure is the ordinary case. Such a declaration takes exactly the contract's positions and returns what the contract's return type takes: its own type first, then at the contract's positions a parameter taking everything the contract's takes there and taking a place only where the contract hands one, the contract's type parameters standing for types no call fills and the declaration's own filled by what the contract writes at the same positions; the names are its own. One declaring a parameter beyond them, `T?` included, **refuses at the build**, at the claim. The run hands the arguments to the same positions whichever declaration satisfies it.

## Interactions

- Which types conform is under [claims](../WARP-54/SPEC.md) and [what a document stands on](../WARP-57/SPEC.md).
- What filled a call's type parameters, which the run holds, is under [type parameters](../WARP-51/SPEC.md).
- The member that backs a row is under [members](../WARP-58/SPEC.md).

## Alternatives considered

- Picking the row by the value's own name. A value of an Optional is its payload or `null`, so it does not say it is an Optional, and a claim about an Optional would never be reached; forbidding Optionals to conform would be an exception to every type being a type.
- A table a front end bakes for each type. The run could not show that a value answers what the contract asks, and the table the link fills would have no source in the document.

## Notes
