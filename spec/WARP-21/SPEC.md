# WARP-21: Where a name may be introduced

Status: accepted

## Summary

A body introduces a name once. The rules decide where a second let or var of a name refuses at the load, which scopes parameters, rounds, failures and payloads stand in, and how far a name declared inside a construct is read.

## Motivation

Without these rules, a body that introduces `x` inside a loop after an outer `x` could read the outer box in one implementation and the inner one in another, and a `break` naming a loop could reach a different loop.

## Rules

**Where a name may be introduced.** A body introduces a name once, and a second `let` or `var` of it **refuses at the load**. A procedure's parameters stand in a scope around its body, and a closure's around the closure's body, so a body may introduce one of its own parameters again. A loop's round, a try's failure and an unwrap's payload stand the same way, in a scope around the body that reads them, so that body may introduce the name again, and from the statement after it the name is the new one. The names a `switch`'s arm binds, under [enums](../WARP-95/SPEC.md#switch), are introduced as an unwrap's payload is and are read in that arm's `then` alone, so that `then` may introduce one again, as an unwrap's `then` may its payload. A name declared inside a `conditional` arm, a `loop`'s round, a `try`'s body or catch, an `unwrap`'s `then` or `else`, a `switch`'s arm or its `default`, or a closure's body is read from the statement after it to the end of that body, and nowhere after, so two bodies side by side may each introduce it. A body may introduce any name it sees: a constant or a variable its document declares, a parameter of the procedure it is written in, or a name a body around it introduced. From the statement after it the name is the new one, with a box of its own: the outer name keeps what it held, a parameter handed in place keeps the caller's variable, and a `set` of that spelling writes the inner name, which **refuses at the load** where a `let` fixed it. A procedure's body stands inside its document, so a parameter may take a constant's or a variable's spelling, and a closure's parameter may take any name around the closure.

**One name, several askers.** A statement's name names the statement, and every reader of it reads that one fact: an expression reads the value the statement bound; a body inside a binding construct reads the construct's own binding under it (`round.index`, `tried.message`, an unwrap's payload); a `break` or `continue` names the loop statement it ends. These are not three names sharing a spelling. They are one name, asked three questions, and which question applies is fixed by where the asker stands. What keeps the readings from colliding is scope, stated per construct: a loop's round is readable in its condition and body, and its name reads nothing after it; a try's name binds the failure only while the catch runs, and an unwrap's the payload only while `then` runs, or, written with no `then`, from the statement on, so the binding reading and the value reading are never live at the same place. A name a body introduces again is the new one to every asker, a leave included: after a `let` or `var` of a loop's spelling in a body inside the loop, in a catch whose failure takes it and where an unwrap's payload takes it, a `break` or `continue` naming that spelling names no loop around it, and **refuses at the load**.

## Interactions

- The constructs whose round, failure and payload stand around their bodies: [WARP-28](../WARP-28/SPEC.md).

## Alternatives considered

- Keeping a constant's, a module variable's and a parameter's spelling out of every body at any depth. Such a rule reads a name by its spelling, where the build reads a name by the binding it stands for, so it refuses documents for no reason the language has.

## Notes
