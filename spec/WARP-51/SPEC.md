# WARP-51: Type parameters

Status: accepted

## Summary

A declaration may leave a type parameter for the call to fill. The rules decide what a body may do with a parameter it does not know, how a call reads its return value, and when a procedure handed to the call fills a parameter. They also decide that a parameter read twice must be read the same both ways, and that readings which do not fit refuse at the build.

## Motivation

A value's type is not always readable off the value. An `Int?` whose value is `5` is the value `5`, so a contract call inside a body that took it at `some T` picks the Optional's row only because the call handed `Int?` as what filled `T`.

## Rules

**A declaration may leave a type parameter and let the call fill it**: a procedure taking `Array<some T>` and a `some T` returns what it was given.

**Inside the declaration the parameter is one type its body does not know**, so every place there that reads it takes only a value of it: the return value, a write into a variable of it or into a part of one, a parameter handed in place, and an argument at a slot a call fills from it. A reading of `Any` or of a contract, and a value of a type the bounds hold, is no value of the parameter, and each **refuses at the build**. A call reads the return value as what filled the parameter.

**A procedure handed to the call fills a parameter only where nothing else does.** It is a value, and what it takes at a position is what it accepts there, not a value the call hands: where anything else handed fills a parameter, the procedure is judged against what filled it, by the rule a procedure-typed slot takes a value, and only where nothing else fills it does what the procedure takes fill it. So a closure whose parameter writes no type, handed to `filter` beside a list of `Int`, leaves `Element` `Int`. Two positions of procedures taking it as two types, one of which takes the other, fill it with the one both take: `(Int) -> Int` beside a closure whose parameter writes no type fills it with `Int`.

**A call hands what filled each type parameter of the declaration it calls**, as the build read it, and the run holds those types while the body runs: a call the body makes hands on what it read, a type parameter of the body read as what filled it there. A door fills them from what the values handed in read as. A closure the body wrote holds the types of the call that made it, so wherever it goes it is a value of the procedure type its signature writes, each type parameter read as that call filled it.

**A list or dictionary literal written inside the declaration at a parameter is judged part by part**, each element, key or value against what the slot asks at it, and an empty list holds no element wherever in the literal it stands: `[]` is a value of `Array<some T>`, `[[], [x]]` of `Array<Array<some T>>` where `x` is one of `some T`, and a list of two dictionary literals, one holding `[]` under `a` and one holding `[x]` under `b`, of `Array<Dictionary<String, Array<some T>>>`.

**A call reads a literal handed to it as one type** to fill a parameter, its parts joined part by part under [numbers and readings](../WARP-47/SPEC.md), and handed beside such a parameter it is then judged part by part as a write is. A dictionary literal handed where a dictionary of the parameter is declared fills it with what each of its keys and values reads it as where it stands at the parameter, joined part by part as a list's elements are, an empty one holding no entry, and each key and value is held where it stands. Where bounds hold the parameter, only what stands at the parameter in a literal handed there is held to them, what a name the literal holds reads as included, and a closure in the literal is judged as any closure handed to its procedure type is.

**A parameter read twice must be read the same both ways.** The readings that fill one parameter **unify**, which is no join: two readings where one accepts the other unify to the one that holds both, position by position through lists, dictionaries and Optionals: a reading of `Any` makes its position `Any`, as it does the whole parameter, and elsewhere the looser stands. Two readings that do not fit **refuse at the build**, and do not widen to `Any` as a join does: two declared types, structs or [enums](../WARP-94/SPEC.md), or one of them and a dictionary, are two types neither of which takes the other. Appending an `Int` to a list of `String`s is a parameter read as `String` and as `Int`, and no type is both. A variable handed in place fills the parameters its slot names exactly, since it is the parameter's type all the way in, and a position handed by value is then a place at that filling, promoted there as any place promotes: appending a `some T` to a list of `some T?` handed in place fills `Element` with `some T?`, and the value appended stands there as its some. Among positions handed by value, two readings that unify where a value at one position would change to stand at what they unify to, promoted to its some or its held type dropped at `Any`, **refuse at the build** too, the way ways that meet do: a slot `some T?` handed an `Int?` reads `T` as `Int`, and beside a reading of `Int?` unifying the two would make the none handed there the some of `Int??`; a slot `some T` handed a value read as `Hashable` and one read as `Any` reads `T` as `Any`, where the first would drop the type it holds. A name declared at the type the call means says which.

**A reading that leaves, or an empty list's element, holds no value**, and a parameter that no reading fills, or that only such readings fill, is filled with `Never`. So `[]` handed at `Array<some T>` reads as a list of any type, `null` alone handed at `some T?` is its none and leaves `T` `Never`, and a call returning that parameter alone reads `Never` and takes no name, the way a call of `Standard.Control.abort` does.

**A bounded parameter is one type.** Where bounds hold the parameter, what each argument hands there is held to them before its readings unify, so a reading among them that does not conform **refuses at the build**, and so does a parameter the readings fill with `Any`, though each conforms.

## Interactions

- A procedure-typed slot is under [what a slot takes, exactly](../WARP-48/SPEC.md), and how the readings at one place join, as a literal's parts do, is under [numbers and readings](../WARP-47/SPEC.md).
- An associated type of a parameter is filled under [the associated types of a type parameter](../WARP-60/SPEC.md).
- A contract call reads what filled its parameters to pick its row, under [calling a contract's procedure](../WARP-63/SPEC.md).

## Alternatives considered

- Handing a witness, the declarations backing a claim, as a hidden argument. A type conforms to a contract one way, so the type that filled a parameter already names the row.
- Copying a body for each type that fills it, at the link. The run would still read a value's own type at an entry and at a value of a contract, and the link would need a refusal for copies that never end.

## Notes

**Note.** An implementation may copy a generic body for the types that fill it, as an optimisation. The cases hold what a program answers and refuses, and a copy that answers the same is invisible to them. A copy keeps the promotions the generic body writes down: filled with `Null`, a body returning its `some T` at `some T?` puts `Some` on the `null` it returns, where a reading of `Null` written at `Null?` is the none, so a copy judged again at `Null` would answer otherwise.
