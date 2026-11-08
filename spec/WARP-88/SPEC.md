# WARP-88: Operations

Status: accepted

## Summary

An operation is an entry in the operation table. The rules decide the tag and fields of each construct and expression form, with every name the build resolved written as a slot or a row. They also decide how a body is lowered: each slot takes the next number in the order the body is written, parameters first, and a closure is lowered on a frame of its own; and where each instruction stands in its document.

## Motivation

The operations are the document's constructs and expression forms with each resolved name written as a slot or a row, so putting the lowering in the specification adds no concept beyond those the document has. Nothing jumps, since flow stays structured as the document writes it.

## Rules

An *operation* is the number of an entry in `operationTable`, and the entry is `[tag, …]`. These are the constructs and the expression forms of a document with every name the build resolved written as the slot or the row it stands for; nothing computes: what a body does it does by calling, under [the standard vocabulary](../WARP-74/SPEC.md).

| tag | operation | fields |
|---|---|---|
| 0 | a literal | *value* |
| 1 | a slot, read through a path | *address* |
| 2 | an array built from parts | list of *operation* |
| 3 | a struct built from parts | `[layout, operations]`: the *layout*, and a list of *operation* in the layout's field order |
| 4 | a closure literal | the closure's number, as the document numbers it under [objects](../WARP-85/SPEC.md), after the spellings it sends and its rows; its captures, a list of `[outer slot, inner slot]` in inner slot order |
| 5 | calling a value | the callee *operation*, arguments: list of *argument*, in position order |
| 6 | a cast | *operation*, *lowered type*, *optional* |
| 8 | a conditional | the condition *operation*, then: *instruction* list, else: *instruction* list or nothing |
| 9 | a loop | the condition *operation*, a literal `true` for a loop written with no `while`, the round: *instruction* list, the round's slot or nothing |
| 10 | a try | the body: *instruction* list, the catch: *instruction* list, the failure's slot or nothing |
| 11 | a call | *call* |
| 12 | a call through a contract | *dispatch* |
| 13 | leaving | *reach*, then for the procedure what it returns: *operation* or nothing, and for the loop and the round the target name or nothing |
| 14 | a dictionary built from parts | a list of `[key, value]`, each an *operation*, in the order written |
| 15 | a value meeting a place that reads it another way | the *operation*, and the *coercion* of its value there |
| 16 | an unwrap | the *operation* it takes apart; then: *instruction* list or nothing; else: *instruction* list or nothing; the payload's slot or nothing, a slot where `then` reads the payload under the statement's name. With no `then`, the operation's value is the payload, which the instruction binds under the statement's name |
| 17 | a switch | its fields, and how a body lowers it, under [enums](../WARP-95/SPEC.md#in-the-binary-and-in-an-object) |

A *layout* is `[name, fields]`: the declared struct's name or a case's spelling, and the field names ascending. A *call* is `[procedure, arguments, handed, types]`: the row the call reaches, numbered by the document; one *operation* or nothing per parameter of the callee, in parameter order, nothing exactly where the call hands that parameter an address in place; `[position, address]` for each parameter handed in place, by position ascending; and one *lowered type* per type parameter and associated type the callee's signature names, each by a type parameter's name or a type member's label under [names](../WARP-67/SPEC.md#the-grammar) as it is written there, `T` or `T.Item`, in the order its parameters and then what it returns first name them, what the call fills it with. That order is the signature's, which the object writes once, so neither the call nor the frame writes it again; a closure literal writes no types, since the closure it makes holds every type the activation making it holds. A *dispatch* is `[contract, procedure, types, first, arguments]`: the contract's name, the procedure's, one *lowered type* per position of the procedure in position order, what the position reads as with the contract's type parameters filled as the call fills them, the first being what fills `Self`; and the first argument and the arguments after it by position, each an *argument*. A lowered type a call or a dispatch writes may name a type parameter of the body it stands in. Which row a dispatch reaches is the link's, and stands nowhere in an object. An *argument* is `[0, operation]` by value or `[1, address]` by reference: the place a call of a value hands in place, or one a call through a contract hands to whichever row takes it in place.

### How a body lowers

A body is lowered in the order it is written, and that order gives each slot its number: a slot is the next one free when the walk first meets its name. The parameters come first, in the declaration's order. Then each statement in turn: what its construct reads is lowered, and then the name the statement binds takes its slot. A loop's round takes a slot before its condition, a try's failure one after the tried body and before the catch, and an unwrap's payload one after what it takes apart and before `then`; with no `then` the statement binds it, after `else`; a switch's bound names take their slots as [enums](../WARP-95/SPEC.md#in-the-binary-and-in-an-object) says. Inside a construct the parts are walked in the order its operation writes them, a callee before its arguments, a struct's fields in name order, a key before its value, and `then` before `else`. A name introduced in a nested body takes a slot of the same frame, and a name introduced twice takes two.

A name a body reads and did not introduce takes a slot the first time it is read: a module variable, written under the frame's `variables`, and a constant the build could not fold into the reading, which is one read at an index the run reads. A closure is lowered on a frame of its own, the same way, where it stands; every name from the body around it, a module variable and a constant included, is taken from that body, so it takes a slot in that body as a read there would and one in the closure's frame, written under the frame's `captures`, and the closure literal writes the two as a pair.

A constant read at an index the run reads holds its slot from the body's start, written under the frame's `constants` as the value it folded to, so every instruction is a statement of the body, in the order written.

A body stands on a declared type through a cast, a coercion, of a value or of an address's key, a call and a dispatch, the entries that write a *lowered type*, and through a switch, which names its enum as a layout names a struct; the types a document's `typeNumbering` holds are the declared types the entries writing a *lowered type* name, so a switch adds none.

### Where an instruction stands

Each instruction stands at a [place](../WARP-65/SPEC.md) in its document, the place of the statement it is. The place follows from the object and the document, so an object writes none. Its identity is the object's `document`, and its steps are the steps of the body the instruction stands in, then the instruction's position in that body, counted from zero.

A declaration stands in its document at these steps:

| declaration | where it stands |
|---|---|
| a member `members` gives under a bare head, where the document declares the type | `types`, the type's name, `procedures`, the member's name |
| a member `members` gives under any other head | `extensions`, the head as a string under [heads](../WARP-55/SPEC.md#the-grammar), `procedures`, the member's name |
| any other procedure | `procedures`, its spelling |
| a constant | `const`, its spelling |
| a module variable | `var`, its spelling |

The body of a row in `rows` is at the steps of where its declaration stands, then `body`. The body of a row in `lifted` is the `body` of the closure literal it was lifted from: the one its declaration wrote that the numbering counts it as, under *the rows* in [objects](../WARP-85/SPEC.md). A list of instructions an operation holds is a body standing inside the statement whose instruction holds the operation, or a coercion around it, at that statement's steps, then:

| operation | list | steps |
|---|---|---|
| 8, a conditional | then | `value`, `conditional`, `then` |
| | else | `value`, `conditional`, `else` |
| 9, a loop | the round | `value`, `loop`, `body` |
| 10, a try | the body | `value`, `try`, `body` |
| | the catch | `value`, `try`, `catch` |
| 16, an unwrap | then | `value`, `unwrap`, `then` |
| | else | `value`, `unwrap`, `else` |
| 17, a switch | an arm's then | `value`, `switch`, `cases`, the arm's case, `then` |
| | the default | `value`, `switch`, `default` |

So the first statement under `then` of a conditional that the third statement of `App.g` writes stands at `procedures`, `App.g`, `body`, `2`, `value`, `conditional`, `then`, `0`.

## Interactions

- The constructs are those of [a statement](../WARP-19/SPEC.md) and the forms those of [an expression's forms](../WARP-30/SPEC.md).
- A constant read at a run index is the one [what a constant folds from](../WARP-16/SPEC.md) leaves unfolded.
- A *dispatch* is a call under [calling a contract's procedure](../WARP-63/SPEC.md), and the types a call hands are those its [type parameters](../WARP-51/SPEC.md) were filled with.
- An instruction's binding and an argument by reference write an *address* of [rows](../WARP-87/SPEC.md).

## Alternatives considered

- A place written beside each instruction, or beside a row in `lifted`. The place of a statement follows from its body and its position, and a lifted row's from the declaration that wrote it and its count, so a written one is a second account that may disagree with the first, and an object, a lower form than the document, would spell the document's keys.

## Notes

**Note.** Where an instruction stands is the place a run's refusal names, and a case writes the stage a program is refused at and not the place, under [a run refuses](../WARP-72/SPEC.md#notes), so where an instruction stands is held only by tests inside the implementation.
