# WARP-60: The associated types of a type parameter

Status: accepted

## Summary

An associated type of a type parameter is written some T.Item. The rules decide how a call fills it once it fills T, that a value of a contract or Any gives none, and how the body treats it as one unknown type.

## Motivation

A generic procedure over a container has to name what the container holds. `Lib.firstOf`, taking `some C: Lib.Container` where `Lib.Container` asks `Item`, returns what `C` gives as `Item`. With `C` alone it could return only `Any`, every caller would cast, and a call handing a box of `Int` beside a `String` it means to compare with what the box holds would build and fail at the run. `returns: "some C.Item"` names that type in the document, and a call fills it from the claim that says what fills `C`, so the build holds every call to it.

## Rules

**`some T.Item` is a type** where a contract bounding a type parameter `T` asks `Item`: the associated type `Item` of `T`, written where *where a type is written* in [bounds](../WARP-52/SPEC.md#where-a-type-is-written) says.

**A call fills it once it fills `T`**, from what fills `T`: the type member of a type a claim within reach says conforms to the contract, filled by what the type puts in the head the member was given under, or, where a type parameter of the caller fills `T`, the caller's own associated type, `some U.Item`. What the call's arguments read at `some T.Item` is that type, so a declaration taking `some T` and `some T.Item` handed a box of `Int` and a string **refuses at the build**.

**A value of a contract or of `Any` gives no associated type**, being of no one type, so a call filling `T` with one where the signature names `T.Item`, `Self.Item` of a call through the contract included, **refuses at the build**, and `Never` filling `T`, the type of what holds no value, gives `Never` at every associated type of `T`, so a slot written there takes no value.

**Inside the declaration an associated type is one type the body does not know**, under [type parameters](../WARP-51/SPEC.md), held to what each contract bounding `T` holds `Item` to and to what the signature's `bounds` say of it under `T.Item`, a slot writing `some T: Lib.Container` beside `bounds: { "T.Item": App.Describable }`. One a call fills from a parameter of the declaration around it is that declaration's own.

**A signature may say an associated type is a type under `sameTypes`**, `sameTypes: { "T.Item": Int }`: a call fills `T` only with what gives that type there, and inside the declaration it is that type. The type may name a type parameter a slot writes or another associated type, `"some U.Item"`, `"Array<some U>"`, which the call reads as it fills the slots, and what fills `T` gives there is held to that type exactly.

**What `sameTypes` may say.** A type parameter no slot writes, and an associated type `sameTypes` names itself or one standing on such, `some T.Item.Key` where it says what `T.Item` is, **refuse at the load**, and so do a key naming a type parameter rather than an associated type, one whose parameter no slot writes, and `sameTypes` written in a closure or a contract's procedure. A type that does not conform to what bounds the associated type **refuses at the build**, where it is written.

**An associated type may stand on another**: where a contract holding `Item` asks `Key`, `some T.Item.Key` is the associated type `Key` of `T.Item`, filled from what fills `T.Item` as that is filled from what fills `T`. An associated type no contract bounding what it stands on asks **refuses at the build** where it is written, and one whose type parameter no parameter of the signature writes, so no call fills it, **refuses at the load**.

**A struct's field, a case's field and a head write no associated type**, under *where a type is written* in [bounds](../WARP-52/SPEC.md#where-a-type-is-written).

**At a door an associated type is what the type of the value at its parameter gives**, held to what bounds the associated type and to what `sameTypes` says it is, so a value standing at one is held to that type, and one of another, or a type that does not conform to those bounds or is not the type `sameTypes` says, **refuses at the run**.

## Interactions

- A contract's `types` and a type member are under [associated types](../WARP-59/SPEC.md); which claims are within reach is under [what a document stands on](../WARP-57/SPEC.md).

## Alternatives considered

- An associated type joined with what the arguments at it read. Joining let an `Int?` through where the claim gave `Int`.

## Notes

**Note.** A same type is held exactly, so some programs that would run safely refuse: where `T.Item` is `Int` and a signature says it is `some U`, a call whose `U` the other arguments read as `Int?` refuses though every value would fit.

**Note.** A struct's field, a case's field and a head write no associated type because a value carries no type's arguments and what fills a struct's or an enum's parameters is read off its fields, which an associated type says nothing of, and a head is a type.
