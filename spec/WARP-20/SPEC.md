# WARP-20: What a write reaches

Status: accepted

## Summary

A set names a path whose head is the variable written. The rules decide which segments a write may pass through, what the written value must fit, and when a write to a whole local variable retypes it.

## Motivation

A write is where a program changes what a box holds, and two runtimes that disagree on where one may land run one document two ways: a `set` of `xs[2]` on a list of two would append in one and stop in the other, and a write through a field its type did not declare `var` would land in one and be refused in the other. So the IR fixes which segments a write passes through, what the written value must fit, and when a write retypes the box it lands in.

## Rules

**What a write reaches.** A `set` names a path, a `write-path` under *the grammar* in [a path](../WARP-31/SPEC.md#the-grammar), whose steps after the head are `.name` and `[…]`, since a write reads no absence; a string `write-path` does not produce **refuses at the load**. The head of the path is the variable written. Every segment after the head is judged at the **build** against the type the walk has reached, and passes through as this table gives; a segment the table does not pass **refuses at the build**:

| the walk has reached | `.name` | `[…]` |
|---|---|---|
| a struct type declared in `types` | the field, where the declaration wrote it `var` | refuses |
| a dictionary | refuses | the entry under that key |
| a list, bytes among them | refuses | the element at that position |
| any other type: `Any`, an Optional, `String`, `Int`, `Double`, `Bool`, a procedure, an enum, a type parameter | refuses | refuses |

At the run, an entry the dictionary does not hold yet is made by the write that lands on it, and a write passing through one **refuses at the run**, as a read of one does. A position the list does not hold **refuses at the run**, whether the write lands on it or passes through it, as a read of one does, under [null is not read through](../WARP-34/SPEC.md).

What is written has to fit the type the path reaches, and is judged against it, so a box that said what it holds holds a value of its declaration after a write as it did after its declaration, and a box that said nothing holds what the build reads the path as. A write to a whole local variable retypes it unless the variable declared what it holds, under *what a variable reads as* in [checking](../WARP-68/SPEC.md). A variable a closure captured, or a call handed in place, holds from there on the type it read as there, and a later write has to fit it, since the closure or the callee reads and writes the box as that type. Two ways that took one variable as different types **refuse at the build** where they meet, since what each took goes on writing its own type; two names for one declared struct or [enum](../WARP-94/SPEC.md) are one type. A way meets the others where its leave lands. A write to a module variable or to an `inout` parameter has to fit the type the box holds and retypes nothing. At the run the value is computed first, and then the box is rewritten once, so nothing observes the box halfway, and the path reaches what the names hold once the value has run, the head and the names it indexes with included. What stands between the brackets is judged as a read's is, under [expressions](../WARP-36/SPEC.md), and a path there is read where the write stands: the write lands on that one position of a list, or on that entry of a dictionary.

## Interactions

- A parameter handed in place takes a path this allows: [WARP-18](../WARP-18/SPEC.md).

## Alternatives considered

## Notes
