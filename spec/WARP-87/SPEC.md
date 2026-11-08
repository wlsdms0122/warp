# WARP-87: Rows

Status: accepted

## Summary

A row is a declaration as its own document compiled it. The rules decide its label, signature, access and implementation, whether written body or native sends, and what a frame holds. They also decide how an address reaches a slot through steps, and what a coercion makes of a value where its reading meets a place that reads it another way.

## Motivation

A native procedure's code is in the host's language, and the host brings it at the link. A link that matched a native procedure by name alone would take another procedure with the same name and the same claims in silence, and a different value would settle with no refusal and no trap, so the row writes the whole signature and the link matches declaration to declaration.

## Rules

A *row* is a declaration as its own document compiled it:

    [ label, signature, access, implementation ]

The label is the declared spelling, a *name*. A row in `lifted` is the same without the label, its fields starting at the signature. `access` is `0` private, `1` internal or `2` public, under [who may name a declaration](../WARP-13/SPEC.md); a lifted row is private, since nothing names it.

The *implementation* is `[tag, …]`:

| tag | implementation | fields |
|---|---|---|
| 0 | a written body | *body*, *frame* |
| 1 | a native procedure | its sends, a list of *send* |

A *send* is `[position, selector, handing]`: where the send stands among the declaration's sends, a count; the spelling it reaches, a *name*; and how many arguments it hands over, from the first position of what that spelling declares, a count. The sends stand one to a place from the first, and each reaches the number the document's `numbering` gives its spelling.

A *frame* is `[size, parameters, variables, constants, captures, names]`: how many slots; which slots the parameters fill, in parameter order; `[variable, slot]` for each module variable the body reads, the variable by its position in `variables`, in slot order; `[value, slot]` for each constant the body reads at an index the run reads, in slot order, the *value* the constant folded to, which the slot holds from the body's start; which slots a closure fills from what it took with it, ascending; and what each slot was called, one *name* per slot, for a refusal that names one.

A *body* is a list of *instruction*, one for each statement of the body, in the order written. An *instruction* is `[binding, operation]`: a *binding* or nothing, and what to compute, under *how a body lowers* in [operations](../WARP-88/SPEC.md#how-a-body-lowers). A *binding* is `[tag, …]`:

| tag | binding | fields |
|---|---|---|
| 0 | to bind | slot |
| 1 | to declare | slot |
| 2 | to assign | *address* |

A *reach* is `0` the procedure, for `return`, `1` the loop, for `break`, or `2` the round, for `continue`.

An *address* is the number of an entry in `addressTable`, and the entry is `[slot, steps, promoted]`: the slot; a list of *step*; and *promoted*, a bool, true where the path's end is a promotion: the value a read finds is its Optional's some, as a *coercion* makes one, unless a marked step met a none. A *step* is `[tag, …]`:

| tag | step | fields |
|---|---|---|
| 0 | a field of a struct whose layout the build proved | its position in the layout, its *name*, *optional* |
| 1 | a field read by its name, written past a null or a `Never` the build laid out no struct for | its *name*, *optional* |
| 2 | a *value* between the brackets, a position on a list and a key on a dictionary | the *value*, *optional* |
| 3 | one read from a slot | the *address* it is read at, *optional*, and a *coercion* or nothing: for a key a path reads or writes in a dictionary whose key type reads it another way, what becomes of the key there |

An *optional* is a bool, true for a step written `?.` or `?[` and for a cast written `as?`.

A *coercion* is what becomes of a value where its reading meets a place that reads it another way, `[tag, …]`:

| tag | where | fields |
|---|---|---|
| 0 | a reading that is no contract meets a place reading one there or in a list's, a dictionary's or an Optional's part | the reading and the place, two *lowered types* |
| 1 | a reading that may hold a contract meets `Any` | |
| 2 | the reading or a part of it may hold a none and meets an Optional as its some | a *coercion* or nothing, what becomes of the value first, then the *steps* |

At `0` the value is held beside what it reads as wherever the place reads a contract, and every type held in a part the place reads as `Any` drops. At `1` every type held in the value and its parts drops. At `2` the *steps* are one walk from the value to the parts that may hold a none, a list of integers, each going into every part the one before reached: `0` into each element of a list, `1` into each value of a dictionary and `2` into each key of a dictionary, and none for the value itself. Each part the walk reaches is the struct `Some` holding it where it is `null` or a `Some`, and itself otherwise; a step finding no list or no dictionary passes the value as it is.

## Interactions

- A native procedure's sends are [a native procedure's](../WARP-14/SPEC.md).
- An address's steps read a [path](../WARP-31/SPEC.md) and [brackets](../WARP-36/SPEC.md) as the build resolved them.
- A coercion holds a value beside the type it was read as, under *a value read as a contract* in [contracts](../WARP-53/SPEC.md).
- A body's operations are [operations](../WARP-88/SPEC.md), and its coercions' types are [lowered types](../WARP-89/SPEC.md).

## Alternatives considered

## Notes
