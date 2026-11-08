# WARP-8: The module

Status: accepted

## Summary

The outline of a document: the dictionary a program travels as, and the module it declares. The rules decide which keys a document has, that each dictionary the grammar names is closed and keyed by strings, and which slots take expressions, statements or types. They also decide that a module variable declares the type it holds, how its start folds, and that it is private to its document.

## Motivation

A reader that skipped a key it did not know would run a program with part of it unread, and two implementations would disagree on whether a misspelled key is a mistake or something to ignore. A module variable is where state that several procedures share lives, since a value is never a reference. Each other key holds what a program says and no procedure body can: `const`, a value the build folds once and every body reads; an alias, a second name for a type, which other documents name as they name the type; `contracts`, what every declaration satisfying one must say; `extensions`, what a document gives a type it does not declare; and `importedClaims`, the claims of other documents its build asks of.

## Rules

What a document is: the dictionary a program travels as, and the module it declares. This WARP is the outline. What each of its slots holds is [a procedure](../WARP-12/SPEC.md), [a statement](../WARP-19/SPEC.md), [an expression's forms](../WARP-30/SPEC.md) and [how a type is written](../WARP-46/SPEC.md), and the bytes it arrives as are [encodings](../WARP-5/SPEC.md).

A document is one dictionary. Every dictionary this grammar names, in this WARP and in the WARPs it points to, is keyed by strings, each in normal form C and not empty, and is **closed**: a key that is no such string, and a key the grammar does not give there, **refuse at the load**. Where a key is a name, a declaration's, a field's or a member's, it holds the grammar its role has under [names and their grammar](../WARP-67/SPEC.md). Every slot marked *expression*, *statements* or *type* takes the grammar of that name.

| key | takes | required |
|---|---|---|
| `warp` | int. The language version this document is written for | yes |
| `imports` | array of strings. Every name the program uses and does not declare: the procedures it sends, and the types and contracts it names, under [the imports list](../WARP-10/SPEC.md) | yes, and empty where the program uses none |
| `importedClaims` | array of `[type, contract]`, each two strings: the claims other documents make that this document stands on, each by the type and the contract it is about, under *a claim imported* in [the imports list](../WARP-10/SPEC.md) | no |
| `types` | dictionary: name → a struct, an enum or an alias, under *a type a document declares* below | no |
| `contracts` | dictionary: name → `{ types?, procedures? }`: the types the contract asks, an array of entries under [associated types](../WARP-59/SPEC.md), `"Item: Hashable"`, none listed twice, and dictionary: procedure → `{ parameters, returns?, failing?, const?, isolated? }`, written the way a declaration's are under [a procedure](../WARP-12/SPEC.md), an empty dictionary for a contract asking nothing; the procedure takes `Self` first, so one leaving `parameters` out **refuses at the load**, and writes no bound and no `sameTypes`, so one writing them **refuses at the load**, under [contracts](../WARP-53/SPEC.md); what it says, it asks of every declaration satisfying it | no |
| `extensions` | dictionary: head → `{ satisfies?, types?, procedures? }`: what the document gives a type under a head, under [heads](../WARP-55/SPEC.md#the-grammar), `Array<Int>`, `App.Box<some T: Hashable>`: the contracts the type adopts under the head, the type's type members and its members | no |
| `const` | dictionary: name → expression; a constant may read the constants beside it, and constants that read each other back have no order to fold in and **refuse at the load** | no |
| `var` | dictionary: name → a module variable, below; a variable every procedure beside it may read and write | no |
| `procedures` | dictionary: name → procedure | no |

**A type a document declares** is one of three, told apart by what its entry writes:

| entry | is | its keys |
|---|---|---|
| a dictionary writing `struct` | a struct | the table below |
| a dictionary writing `enum` | an enum | under *the declaration* in [enums](../WARP-93/SPEC.md#the-declaration) |
| a string | an alias, the name a second spelling of the type the string writes under [how a type is written](../WARP-46/SPEC.md) | none |

A dictionary writing both `struct` and `enum` **refuses at the load**, under [enums](../WARP-93/SPEC.md#the-declaration), and so does one writing neither, which is no type's string.

| key | takes | required |
|---|---|---|
| `struct` | dictionary: field → type. Each field by its name, a value's name under [names and their grammar](../WARP-67/SPEC.md), and its type | yes |
| `typeParameters` | the type parameters it takes, in order, each an `entry` under *the grammar* in [a struct may take type parameters](../WARP-50/SPEC.md#the-grammar), `"K: Hashable"` | no |
| `satisfies` | the contracts it adopts, under [claims](../WARP-54/SPEC.md) | no |
| `types` | its type members, a dictionary from a type member's name to a type under [associated types](../WARP-59/SPEC.md), which an object writes under `typeMembers`, under [what an object holds](../WARP-85/SPEC.md) | no |
| `procedures` | its members, dictionary: member's name → procedure, under [members](../WARP-58/SPEC.md) | no |

**A module variable** is written `{ type, value }`, both keys written: `type` the type it declares it holds, and `value` its start, an expression. An entry written any other way, an expression alone or a dictionary writing one of the two keys without the other among it, **refuses at the load**: a module variable always declares its type and writes its start.

Its start is written like a constant and folds the same way: at the **build**, from what a constant folds from, beside the constants and reading them, and them only: a start that reads another variable **refuses at the load**. A closure literal written in a constant or a start is a procedure of the document: its body reads and writes a module variable when the closure is called, as a body the document declares may, and the constant or the start holding it does not read that variable. A start the declared type does not take **refuses at the build**, and every write into the variable is judged against that type. It is private to the document like a constant, as a procedure written `private` is under [who may name a declaration](../WARP-13/SPEC.md), read by the same spelling (`ref`), and written by a `set` in a procedure the document declares, or through a parameter such a procedure hands it to in place; another document reaches it only through such a procedure. A name is a constant or a variable, not both: one declared under both keys **refuses** at the load. Either may be spelled like a procedure: a reference reads the constant or the variable, and a call names the procedure. Every run starts each variable at its folded value, so two runs of one image never see each other.

**Note.** A module variable declares its type as a parameter does, so what every body beside it reads and writes is set by a declaration and not by what the build reads off an expression, and a start that says nothing of what the box will hold, an empty list or `null`, needs no rule of its own. A front end that works the type out writes the type it worked out.

**Note.** A case starts one run of its image, so that every run starts each module variable at its folded value is held only by tests inside the implementation.

## Interactions

- The version and the imports list, the two keys every document writes: [WARP-9](../WARP-9/SPEC.md), [WARP-10](../WARP-10/SPEC.md).
- What is left out, an empty `const` or `var` among it: [WARP-11](../WARP-11/SPEC.md).
- A constant and a variable's start fold from what [WARP-16](../WARP-16/SPEC.md) allows.
- A variable is written in place through [WARP-18](../WARP-18/SPEC.md).

## Alternatives considered

- A module variable written as its start alone, holding the type its start reads as. What every body beside it may write would be decided by the build's reading of an expression, a cast, a constant's element and an empty collection each read by a rule of its own, rather than by a declaration, against what *what a declaration leaves out says the least* in [a procedure](../WARP-12/SPEC.md) chose for a call.
- A constant or a start that reads the module variables a closure literal in it reads. A closure's body runs when the closure is called, in the run that calls it, as a body the document declares does; Swift and Go each let a closure a global holds read and write another global for the same reason.

## Notes
