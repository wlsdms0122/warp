# WARP-54: Claims

Status: accepted

## Summary

A type conforms to a contract when a document says it does. The rules decide how a claim is written in a struct's declaration or an extension, which types a claim may be about, and whom a claim holds for.

## Motivation

Were conformance found by looking for a declaration spelled `Bank.Account.describe` whose signature fits `App.Describable`, whether a document builds would turn on whether some other document is in the link, and what a document builds to would not be a fact of it and what it stands on. A document that never names `App.Describable` would also be refused because a declaration it wrote happens to share a spelling with what the contract asks and returns another type.

## Rules

**A type conforms to a contract when a document says it does.** A document says it where it gives the type what it gives it, under `satisfies`: a struct it declares beside its fields, `{ struct: { rank: Int }, satisfies: ["App.Describable"] }`, and any other type in an extension, keyed by the type, `extensions: { "Bank.Account": { satisfies: ["App.Describable"] } }`. Any document may make one, about a type it declared or about another document's, which is how a document that arrives later gives a type the procedures a contract asks.

**A type the language names is a type the way a declared one is**, and a claim may be about it: `extensions: { Int: { satisfies: ["App.Describable"], procedures: { describe: … } } }`, backed by its member `describe`.

**A claim written where a struct is declared, or under an extension keyed by a type's bare name, is about every value of the type.** A list and a dictionary are named bare `Array` and `Dictionary`: every list is an instance of `Array` whatever it holds, bytes among them under [what a value is](../WARP-2/SPEC.md), and every dictionary of `Dictionary` under whatever keys, so a claim about `Array` is about every list and one about `Dictionary` about every dictionary. What backs such a claim takes every value it is about, under [a claim holds to members](../WARP-56/SPEC.md).

**A struct taking type parameters named bare is the same**: a claim about it is about every value of it whatever it is applied to, each parameter one no call fills, held to the bounds the struct declares, so a claim about `App.Box` is about `App.Box<Int>` and `App.Box<String>` alike.

**A claim is about a type**, written as a head under *the grammar* in [heads](../WARP-55/SPEC.md#the-grammar), an Optional by its `?`, so a procedure conforms to no contract. A value of a declared type is an instance of the struct or [enum](../WARP-94/SPEC.md) it is, and of no other name, so a head naming a declared name is about a type only where that name is a struct or an enum. A claim's head, and an extension's whatever the extension gives, under [members](../WARP-58/SPEC.md), refuses by what it names:

| the head names | refuses |
|---|---|
| what the head grammar does not give | **at the load** |
| a name the link declares as a contract | **at the build**, under [what a document stands on](../WARP-57/SPEC.md) |
| an alias, a type member's spelling among them, or a case's spelling | **at the load** in the document declaring it, which gives it nothing at all, and **at the build** in another |
| a name no module declares | **at the build** |

**Note.** An alias's or a case's spelling splits its stage the way two declarers of one spelling do, under [the specification](../README.md): whether a name is an alias is a fact of the document that declares it, which that document decides alone at its load, and only the link sees a declaration in another document.

**Note.** No head is a procedure type, and a bare head is no `Any`, `Never`, `Procedure`, `Self` or `Hashable`: `Any` and `Never` are types no value is an instance of by name, `Procedure` and a procedure type name a structure and no type, `Self` names a type only inside a contract's procedures, and `Hashable` is a contract, which a value conforms to and is never an instance of.

## Interactions

- A claim is held to members under [a claim holds to members](../WARP-56/SPEC.md) and [members](../WARP-58/SPEC.md).
- Where a claim is judged and whom it holds for is under [what a document stands on](../WARP-57/SPEC.md), and a claim from a third document is imported under [the imports list](../WARP-10/SPEC.md).

## Alternatives considered

- A list of claims of its own at the top of a document, apart from where the type is given its procedures. A type is given what it gives in two places, its declaration and an extension, and a claim is written in the same shape in both, so a reader finds the claim beside the members that back it.

## Notes
