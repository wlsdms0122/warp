# WARP-58: Members

Status: accepted

## Summary

Members are what a document gives a type under procedures. The rules decide how a member is spelled, how a type satisfies a contract's procedure by its member, and which documents' members a claim may stand on.

## Motivation

A claim needs a procedure behind each one its contract asks, and the build finds it by the type and the procedure's name. Were any declaration spelled `Int.describe` taken as that procedure, a document declaring `Int.describe` for its own use would back, or break, a claim another document makes about `Int`, so whether one document builds would turn on what an unrelated one calls its procedures. A member is given where the type is given what it gives, `extensions: { Int: { satisfies: ["App.Describable"], procedures: { describe: … } } }`, so a claim finds it there and nowhere else.

## Rules

**What a document gives a type under `procedures` are the type's members**, in the struct's declaration or in an extension. A member is a procedure under its spelling, which a call writes, under [names](../WARP-67/SPEC.md#the-grammar): `Bank.Account.describe`, and an Optional's `Optional.describe`. It stands among the procedures as any declaration does: a procedure declared under that spelling, or a second member under it, is one name with two declarers, and **refuses at the load** in one document and **at the build** across documents.

**A type satisfies a contract's procedure by its member of that name**, given in the claim's document or in one that document stands on. So a claim written in an extension stands on the members a struct's declaration gives, and a claim written in a struct's declaration takes no member from an extension, which stands on the declaration and not the other way round.

**A document gives a struct or an [enum](../WARP-94/SPEC.md) it declares what it gives every value of it in the declaration**, so an extension of a struct or an enum the document declares under its bare name **refuses at the load**, and so does an extension giving nothing, which is a second way to write a document.

**A member takes a value of its type first**, by value or in place, as the table below writes it. A member is there for the values its head takes, and a call says which by what it hands first, so the member takes that value first. Under a head applying its type it takes what the head takes, and under the type's bare name every value of the type.

| a member given under | takes first |
|---|---|
| a head applying its type, an Optional's included | the head as written, each type parameter under the head's name for it and each alias as the head writes it. A bound beside a type parameter's first naming may be left out, and one written holds beside the head's: under `App.Box<some T: Hashable>`, `App.Box<some T>` |
| the bare name of a type listing no type parameters | the type's name: `Bank.Account`, `Int` |
| `Array` | `Array<Any>`, or `Array` applied to a type parameter of its own with no bound |
| `Dictionary` | `Dictionary` applied to a type parameter of its own bounded by `Hashable` alone, then to `Any` or a type parameter of its own with no bound: `Dictionary<some K: Hashable, Any>` |
| the bare name of a struct or an enum listing type parameters | the type applied to a type parameter of its own at each position, each bounded as the declaration bounds that position: `App.Box<some T>` |

Under a head, a first parameter written otherwise **refuses at the load**. Under the bare name, a first parameter writing the type's own name, the one the head writes, that takes only some of the type's values, `Array<Int>` or `App.Box<Any>`, **refuses at the build**, since it is given under a head applying the type. A first parameter writing any other name, an alias of the type among them, and a member that takes nothing, **refuse at the load**: a procedure that takes no value of a type, `Array.make` taking a `String`, is declared under `procedures` with that spelling.

**A member's type parameters the head names are held to the head's bounds** beside its own, so a call handing `App.Box.describe` a box of what does not conform to `Hashable` **refuses at the build**.

**An extension's head is held the way the type a claim is about is held**, whatever the extension gives, under [claims](../WARP-54/SPEC.md), and one that refuses there refuses at the extension.

**A procedure spelled like a member and declared among a document's `procedures` is that document's procedure** and nothing more: it is no member, and satisfies no contract's procedure. So what a link declares never decides what an unrelated document may call things, and a document that names no contract builds the same whichever documents stand beside it.

## Interactions

- A claim is held to members under [a claim holds to members](../WARP-56/SPEC.md), and a member is called through its contract under [calling a contract's procedure](../WARP-63/SPEC.md).
- What a document stands on is under [what a document stands on](../WARP-57/SPEC.md).

## Alternatives considered

- Any declaration spelled `<type>.<procedure>` answering, members or not. It reserved spellings across the link.

## Notes
