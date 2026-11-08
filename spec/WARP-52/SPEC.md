# WARP-52: Bounds

Status: accepted

## Summary

A type parameter is bounded where it is introduced. The rules decide where a bound is written, that the signature owns it and writes it once, and that it holds every occurrence of the name.

## Motivation

Were a bound allowed beside any `some T`, two slots of one signature could bound `T` differently, and two implementations would have to agree on which one wins or whether they meet.

## Rules

**A type parameter is bounded where it is introduced**: beside the first `some T` the signature's slots write, the parameters in order and then the return type, at any depth, a procedure-typed slot's own types included, `parameters: [{ name: of, type: "some T: Standard.Comparable" }, { name: value, type: "some T" }]`. A bound written inside a procedure-typed slot is the declaring signature's, because that procedure type's parameters are the declaring signature's own slots. A head writes its own beside the names it applies, under [heads](../WARP-55/SPEC.md), and a struct beside the names it lists.

**The signature owns the bound and writes it once.** The other slots name the parameter and never the bound, so one bound is one claim however many slots mention the name, and a bound beside a later `some T` **refuses at the load**. Only `some T` names `T`, and `some T.Item` names none. Inside one type the order is the spelling's: a struct's or a dictionary's arguments in order, a procedure type's parameters in order before its return type.

**A bound holds every occurrence of the name** to what conforms to the contract the bound names, under [contracts](../WARP-53/SPEC.md). A bound may name several, joined with `&`: `some T: Describable & Standard.Comparable` holds `T` to what conforms to every one of them. A bound names contracts and nothing else, and what conforms to one is whatever type a document claims does, so the set a bound holds a parameter to is open.

**The judgement is the build's.** A reading whose type does not conform to the bound refuses (two booleans meeting `lessThan` never run), and so does a reading whose type the build does not know, under [what a slot takes, exactly](../WARP-48/SPEC.md). A cast judges what actually arrived at the **run** by what it reads as: the type it is an instance of, applied to what its parts read as, which is what a head is held to under [heads](../WARP-55/SPEC.md).

**An associated type is bounded under `bounds`.** What a signature does not introduce, an associated type of one of its type parameters, it bounds under `bounds`, keyed by its label, `bounds: { "T.Item": Hashable }`, beside what `sameTypes` says of it, under [the associated types of a type parameter](../WARP-60/SPEC.md). A key of `bounds` naming a type parameter, one standing on a parameter no slot mentions, and a bound a slot writes beside an associated type, `some T.Item: Hashable`, each **refuse at the load**.

**Only the declaring procedure, beside its first `some T` and under `bounds`, a head, a struct, an enum and a contract's `types` write a bound**, under *where a type is written* below, and a closure writes none, under [expressions](../WARP-30/SPEC.md).

**A closure written in the body, and a name the body declares the type of, read the same names**: a `some T` there is the `T` the caller filled, held to the bounds the declaration wrote, so a closure may send what the body around it may. One writing a `some T` the procedure around it does not declare, or written where no procedure is, **refuses at the load**.

**A bound names a contract.** One naming what no module declares as a contract **refuses at the build**, and one naming a type the language names or a struct the language declares, `Failure`, neither of which is a contract, **refuses at the load**.

**A type parameter lives where something fills it**: in a signature, filled by what a call hands; in a struct or an [enum](../WARP-94/SPEC.md) that lists it, filled by a mention; or in a head, filled by what the claim or the member is asked about. A declared type writing `some` for a name it does not list, an alias's included, and a signature naming one in what it returns and at none of its parameters, at any depth of a procedure-typed one included, each **refuse at the load**, because nothing there fills it.

### Where a type is written

Each place a document writes a type may write what its row says, at any depth of the type, inside a procedure type it writes included:

| a type written as | a bound | `some T` | `some T.Item` | `Self`, `Self.Item` | `inout` | `var` |
|---|---|---|---|---|---|---|
| a procedure's parameter or return type, a member's included | beside the first `some T` its slots write | yes | yes | no | in front of a parameter's type | no |
| a closure's parameter or return type | no | of the procedure around it | of the procedure around it | no | in front of a parameter's type | no |
| a contract's procedure's parameter or return type | no | yes | no | yes | in front of a parameter's type | no |
| a struct's field | no | of a parameter the struct lists | no | no | no | in front of the field's type |
| a case's field | no | of a parameter the enum lists | no | no | no | no |
| a type member | no | of a parameter its head names, or in a struct's or an enum's declaration one it lists | yes | no | no | no |
| an alias | no | no | no | no | no | no |
| a module variable's type | no | no | no | no | no | no |
| a name's type, which a statement declares | no | of the procedure around it | yes | no | no | no |
| a cast | no | of the procedure around it | yes | no | no | no |
| a same type, a value of `sameTypes` | no | of a parameter a slot writes | yes | no | no | no |
| a [head](../WARP-55/SPEC.md) | where it first names `T` | yes | no | no | no | no |

`inout` in front of a parameter's type is in front of the type of a procedure type's parameter too, wherever that procedure type is written, `(inout Int) -> Int` in an alias among them. Writing what a slot may not write **refuses at the load**, except a `some T.Item` whose `T` is written where nothing can bound it, a contract's procedure's among them, which refuses at the build under [associated types](../WARP-60/SPEC.md). Which type parameter a `some T` or a `some T.Item` written there may name is under the rules above and under [associated types](../WARP-60/SPEC.md).

## Interactions

- Whether a type conforms to what a bound names is judged under [what a document stands on](../WARP-57/SPEC.md).

## Alternatives considered

- A bound held in a map beside the names, a struct listing `T` and a separate map putting `Hashable` on `T`. It writes each name twice for one fact, and the head already spelled a bound beside its name.
- One `where` list holding every requirement, bounds and same types together. A refusal names a spot by the steps through the document, and an element of such a list is a spot only if the model keeps the order it was written in, so the model and the object would change for a spelling.

## Notes
