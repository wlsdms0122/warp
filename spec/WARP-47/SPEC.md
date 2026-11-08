# WARP-47: Numbers and readings

Status: accepted

## Summary

Int and Double are two types and neither takes the other. The rules decide how a literal is read as the place it is written into reads it, when an integer literal is a Double, and how readings join.

## Motivation

A literal is the one value that has no type until something reads it. `1` written where a `Double` is declared, or beside `2.5` in a list, could be either number, and two implementations that read it differently would hand back `1` and `1.0` for one document, or one would refuse what the other runs.

## Rules

**`Int` and `Double` are two types.** Neither takes the other, whatever the value, under *the numeric edge* in [what a slot takes, exactly](../WARP-48/SPEC.md). A slot that takes either kind of number is bounded by the contract `Standard.Numeric`, under [the standard vocabulary](../WARP-77/SPEC.md).

**A literal is read as the place it is written into reads it.** A place is a slot, a procedure's declared return type, a name that says what it holds, a write, a list's, a dictionary's, a struct's or a case literal's part there, what stands between a path's brackets (an `Int` on a list and the key type on a dictionary), the type a cast, `as` or `as?`, names, and a type parameter a call fills. A type parameter a call fills reads as what the call's arguments fill it with, under [type parameters](../WARP-51/SPEC.md); a struct literal there fills nothing, and reads as the declared struct the others fill it with, and a [case literal](../WARP-93/SPEC.md#a-cases-value) as the enum the others fill it with.

**An integer literal is a `Double` where its place reads a `Double`, and where it stands beside a `Double`**, the `Double` it names, whatever type the place declares: `[1, 2.5]` written where `Array<Any>` is declared holds `1.0`. A literal stands beside each reading that stands at its position among the readings it is joined or unified with, whether a literal or a name writes that reading: the other elements of its list literal, the other keys or the other values of its dictionary literal, and the same field of the other struct and case literals among them, each at the same depth, so `[[1], [2.5]]` holds `[1.0]` and `[1, "a", 2.5]` holds `1.0`; and the other readings filling the type parameter it stands at, a call's arguments and a struct literal's fields among them. Anywhere else an integer literal is an `Int`, and a name it is bound to holds an `Int`.

**Readings that stand at one place join part by part**: the elements of one list, the keys and the values of one dictionary, and the ways that meet at one variable. A reading beside itself reads itself, so `Null` beside `Null` reads `Null`. Null beside another reading reads that reading where it is an Optional and its Optional otherwise, and an Optional beside a reading other than `Null` reads the Optional of what its payload joins with that reading, or with that reading's payload where it is an Optional. Two lists join by their elements and two dictionaries by their keys and their values; two dictionaries whose keys join to `Any` read `Any` whole, since a dictionary's key conforms to `Hashable`. Two procedures join to a procedure that keeps the parameters both write alike, returns the return type both write, or `Any` where they write two, and carries the constness and isolation both carry and what either may fail with, and two whose parameters differ, in count or in a type, join to `Procedure` with the modifiers both carry in front of it, since no procedure type takes at each position what each of the two takes there. `Never`, as a whole or as a part, joins to what stands beside it, so two mentions of one declared struct or enum, one applying it to `Never` at a position where the other applies it to a type, join to the other: `App.Result<Never, String>` beside `App.Result<Int, String>` reads `App.Result<Int, String>`. Two parts that still differ read `Any`. A join fills no type parameter: the readings that fill one unify under [type parameters](../WARP-51/SPEC.md), where two that do not fit refuse.

**Ways that each write a name are places of their own.** A write lands as what the name holds it as, so where two ways meet, one writing an integer literal beside another writing a `Double` reads `Any`, which a slot of a type takes only through a cast.

## Interactions

- That `Int` refuses `2.0` and `Double` refuses `1` whatever the value is, and how a `Double` literal rounds, are under [what a slot takes, exactly](../WARP-48/SPEC.md).
- What a type parameter a call fills reads as is the readings filling it unified, under [type parameters](../WARP-51/SPEC.md), and what ways that meet read as is their join, under [what a variable reads as](../WARP-68/SPEC.md).

## Alternatives considered

- A membership of `Int` and `Double`, a type that is either number. The language says A or B one way, with a contract each type conforms to, under [contracts](../WARP-53/SPEC.md), and `Int` and `Double` are types as a declared struct is, so a slot taking either is bounded by `Standard.Numeric`.
- Fixed-width integers, `Int8` and the like. The value model is a transport model, and a fixed width is no kind of value a transport carries, so a range is a declared struct and a procedure that makes one, which is the vocabulary's.
- Two procedures whose parameters differ joining to a procedure taking `Any` at each position where they differ. A list of a closure taking `Int` and one taking `String` would then hand a string to the first, against *a procedure-typed slot* in [what a slot takes, exactly](../WARP-48/SPEC.md).
- A 32-bit `Double`. It is a precision of the same number, and every binary32 value is a binary64 value, so nothing crossing a door is lost without it.

## Notes
