# WARP-32: A cast

Status: accepted

## Summary

A cast names the type a value is read as. The rules decide that the build trusts the cast and the run judges the value against the type, how as and as? differ on a mismatch, and which needless casts refuse at the build.

## Motivation

Without a cast, a value read as `Any` could reach a slot of a type only if the run judged it at that slot, so every slot that takes a type would be a place the run must judge, and a place left off that list would take a value of the wrong type unjudged.

## Rules

A **cast** names the type a value is read as. The type is written the way any type is, as a string. From the cast on, the reading *is* that type, so every dot after it is judged against it; the run is left the one question the build cannot decide, which is what actually arrived, and it decides it by judging the value against the type, leaving nothing out. A cast is how a value read as `Any` or as a contract reaches a slot of a type, since the build does not know which type it is. A plain `as` **fails at the run** with `cast_refused` when the value is not that type. It is a failure like any other, so a `try` catches it, and `as?` reads that mismatch as the none, which is the author saying they expected it. A cast takes no level off an Optional: a `Some` holding `null` is no value of `Int?`, so cast to `Int?` it fails.

A cast whose operand, read on its own, already **is** the type it names refuses at the build, the way a needless `?.` does: the claim says nothing. So does a cast to a type that takes what its operand reads and takes the reading, or any part of it, an Optional's payload, a list's element or a dictionary's key or value at any depth, as an Optional's some: the reading stands there by promotion, and a name declared at that type says it, so `x as Int??` of an `x` read as `Int?` refuses, and so does `xs as Array<Int??>` of an `xs` read as `Array<Int?>`. The test is sameness, not admission: a reading of `Int?` cast to `Int` names something the types leave open, and only the run can say whether it holds. The type a cast names is a place a literal in its operand is written into, as a slot is, under [types](../WARP-48/SPEC.md): a struct literal there is read as the declared struct the type names, and an integer literal as the `Double` it names where the type declares a `Double`, at every depth, so `[1] as Array<Double>` is `[1.0]`. On its own a literal is read as written, and a struct literal as no struct at all, so a cast that is a literal's place is needless only where the literal, read as written, already is the type or stands there by promotion, as `1 as Int` and `[1] as Array<Int?>` do.

A type parameter of the procedure the cast stands in, and an associated type of one (`some T.Item`), written anywhere inside its type (`Array<some T>`), reads as the call filled it, as it does on a name saying what it holds, so the run judges what arrives against the type the call filled; a type parameter the procedure does not declare **refuses at the load**.

**A cast names a type that shares a value with its operand's reading.** A cast writes no name onto a value and never takes one away, so a cast to a type that shares no value with what its operand reads names a type no value it reads is, and **refuses at the build**. Two types, each with its aliases read as what they stand for, share a value by the first row either of them meets:

| one of the two | shares a value with the other |
|---|---|
| `Any`, a contract or a composition of contracts, a type parameter, an associated type | always |
| `Null`, an Optional | where the other is `Null` or an Optional, at the none, and where an Optional's payload shares a value with the other |
| `Procedure`, a procedure type | where the other is `Procedure` or a procedure type |
| `Bool`, `Int`, `Double`, `String` | where the other is the same type |
| `Array<T>` | where the other is an `Array`, at the empty list |
| `Dictionary<K, V>` | where the other is a `Dictionary`, at the empty dictionary |
| a declared struct or [enum](../WARP-94/SPEC.md) | where the other is the same declaration applied to the same types, `Never` reading as any type there, since its type arguments are invariant under [a struct may take type parameters](../WARP-50/SPEC.md): `App.Result<Int, String>` cast to `App.Result<String, String>` refuses, though a `failure` carrying a `String` fits both |

Between two Optionals the none is a value of both, so such a cast stands, and `as?` reads a value of the other as the none. A dictionary arriving where a cast reads a declared struct from a reading of `Any` or of a contract is no value of it, so the cast fails with `cast_refused` and `as?` reads it as the none. A cast onto `Any` or `Never` refuses at the build for the other half of the same reason: those name no type to read.

**Note.** A contract and a type parameter share a value with every type because what they hold is settled by what arrives: which types claim a contract is the link's to say, so the build leaves those casts to the run, which judges the value against the claims the link holds.

A cast that names a type nothing declares **refuses at the build**, wherever it is written, by the rule every type spelling is held to. `as?` reads a value that is not the named type as null; it does not read a name that names nothing as null, because that is the declaration being wrong rather than the value.

## Interactions

- `cast_refused` and what a catch reads from it: [`try`](../WARP-25/SPEC.md); what it adds to a body: [what a body may fail with](../WARP-26/SPEC.md).
- A dot on `Any` or on a contract: [a dot reads a name](../WARP-33/SPEC.md).

## Alternatives considered

- A value read as `Any` standing in a bounded type parameter's slot, judged by the run there. A contract's slot takes such a value only through a cast, and one rule covers both: a value the build could not type reaches a slot that asks for a type through a cast.

## Notes
