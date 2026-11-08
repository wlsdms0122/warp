# WARP-65: What an implementation checks, and when

Status: accepted

## Summary

This unit lists which stage makes which refusal. The rules decide what is refused at the load and what at the build, since a program is read, checked and built before any of it runs and two implementations must agree on that.

## Motivation

Two implementations can agree on every value a program returns and still not be the same language, if one of them refuses a program the other runs, or refuses it later, after a host has acted on a load the other refused. A host decides from a document's load before anything runs, so which refusals the load makes and which the build makes is fixed as one list rather than left to how an implementation divides its work.

## Rules

Which stage makes which refusal. This WARP and [WARP-66](../WARP-66/SPEC.md) are a list rather than a rule, and the list is the contract.

A program is read, checked and built before any of it runs, the arms nobody takes included. All of the following are decided while nothing has happened yet. At `load`, since a document decides them alone: the leaves (`break`/`continue` having a loop, a `break` ending only a loop written with `while`, nothing following one, a `loop` written with no `while` or a construct every way of which leaves), every name in normal form C and holding the grammar of where it is written, every `ref`'s head, the value's name before its first step, resolving within its own document to a parameter, a constant, a module variable, a statement written before it or a binding the construct holding it opened (a loop's round, a try's failure, an unwrap's payload, the names a switch's arm binds), a procedure's `access` being one of its three values, a closure writing no `access`, no bound and no `sameTypes`, a bound standing only where a name is introduced, under [bounds](../WARP-52/SPEC.md), and a key of a signature's `bounds` naming an associated type, a literal writing no struct's name, a construct written only as a statement's value, constants naming no cycle, every `set` writing a path headed by a variable and through no optional step, what stands between a path's brackets being an integer literal, a string literal or a path, a contract's procedure taking `Self` first, writing no bound and no `sameTypes` and naming as `Self.Item` only a type its contract asks, a same type keyed by an associated type, naming no associated type `sameTypes` also names and no type parameter no slot writes, one document giving a type one type member under a name once, no declared name that is no struct and no enum coming back to itself, an [enum](../WARP-93/SPEC.md) declaring at least one case, a case literal of one entry, a switch writing at least one arm, each with a `then`, binding no name twice in one arm and setting no bound name, no two declarations under one spelling in one namespace within one document, under *one spelling has one declarer* in [names](../WARP-64/SPEC.md), no case's spelling written as a type in the document declaring its enum, and where `inout`, `var`, `Self`, a type parameter and an associated type are written, under *where a type is written* in [bounds](../WARP-52/SPEC.md#where-a-type-is-written), the type parameter an associated type stands on being one a parameter writes. The rest at `build`, since each is judged against a signature or another document. What the grammar WARPs refuse as form (a type spelled wrong, a catch holding no statement, an unwrap with neither `then` nor `else`, a leave with nothing to leave) is `load` too, and those WARPs say so where the form is written. Each rule names its stage: a call that misfits a declaration in its own document refuses at `build` all the same, and two declarations under one spelling refuse at `load` within one document and at `build` across two.

`imports` is held at `load`, under *the imports list* in [documents](../WARP-10/SPEC.md), because a host decides from it before any of this runs.

Reading does not decide everything: whether a number will be zero when something divides by it is found out by running, under [running](../WARP-72/SPEC.md).

**What a refusal names.** A refusal at `load` or `build` about one spot in a document names that spot, its **place**, carried as the value `[identity, steps]`, so it crosses in either encoding as any value does:

| field | holds |
|---|---|
| `identity` | the document's identity, bytes, under *identity and dependencies* in [objects](../WARP-91/SPEC.md) |
| `steps` | a list of the steps from the document's root to the spot, each a key the document writes, a string, or a position in a list the document writes, an int counted from zero |

So the steps lead through the document's tree and through nothing else: `procedures`, `App.g`, `body`, `2`, `value`, `call`, `arguments`, `0` is the first argument of the call the third statement of `App.g` writes. A refusal about a document as a whole names it with no step, `[identity, []]`. Input that reads as no document, bytes the binary reader refuses or a text the text reader refuses, has no identity, so its refusal names no place; a refused text names a line and a column instead, under [encodings](../WARP-7/SPEC.md). A place names the document and never the file the document was authored in. A refusal that is a fact about the whole link and no spot in it names no place, since it has none. The sentence beside the place is the implementation's: a case says the stage and reads nothing else.

**Note.** A case writes the stage a document is refused at and no place, so which spot a refusal names, and the line and column a text refusal names under [encodings](../WARP-7/SPEC.md), are held only by tests inside the implementation. The sentence beside the place is the implementation's, and two implementations agreeing on every case may still say the reason in different words.

## Interactions

- A run's refusal names the places of the frames it stopped in, under [running](../WARP-72/SPEC.md).

## Alternatives considered

- Four stages, compile and link apart. Nothing runs between the two halves of the build, so which half refused is no fact a program or a host can observe; naming it would bind how an implementation divides its own work.

## Notes
