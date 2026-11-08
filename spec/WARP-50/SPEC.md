# WARP-50: A struct may take type parameters

Status: accepted

## Summary

A struct may list type parameters. The rules decide how they are listed and bounded under typeParameters, how a mention applies the struct to types, and when two mentions are one type.

## Motivation

A field written as `Any` cannot hand back the `T` it was given, since a cast onto a type parameter refuses. A front end that copied the struct out for each use would carry a second type checker and break the build of one document at a time.

## Rules

**A struct lists its type parameters** in order under `typeParameters`, `{ struct: { item: "some T" }, typeParameters: [T] }`, and may hold each to contracts beside its name there, `typeParameters: ["K: Hashable", V]`, an `entry` under *the grammar* below, the way a signature does beside the first `some T`. A field writes one as `some T`. A field naming one the struct does not list, a field writing a bound, a name listed twice and an empty list each **refuse at the load**.

**A mention applies the struct to one type per parameter**, `Box<Int>`, `Box<some T>` in a signature, and is the struct with each parameter read as the type at its position, so every judgement above asks that of its fields. A type standing at a bounded position conforms to the contracts its bound names, a type parameter by its own bounds, the way a dictionary's key conforms to `Hashable`, or **refuses at the build** where the mention is written. A value of one carries the struct's name and its fields, and nothing of what it was applied to, as a list carries no element type.

**Two mentions of one struct are one type only where they are applied to the same types.** What a reading says of one value and no declaration writes is read as what is declared: an integer literal as the number it names, and `Never` as any type. A procedure type is the same type only where it declares the same constness, isolation and failing. So `Box<Int>` does not stand where `Box<Int?>` is declared, though a list of `Int` stands where a list of `Int?` is, and `Box<isolated () -> Int>` does not stand where `Box<() -> Int>` is; two readings applied to different types join to `Any`; and a constant holding one is the struct its expression was judged as, or, judged at `Any`, what its value reads as, its fields' readings joined as the readings at one place join, under [numbers and readings](../WARP-47/SPEC.md).

**A call filling a type parameter walks into what the struct is applied to**, as into a list's element.

**A struct literal of one is read as applied to what its place applies the struct to.** Where the place leaves a position to a call, it is applied there to what the fields standing on that parameter read as, unified as a call's arguments filling a parameter are, under [type parameters](../WARP-51/SPEC.md), and to `Never` where no field reads one, as an empty list's element is.

**A door and a cast judge a value's fields against the struct applied to what the slot or the cast writes**, and an alias's name, `Pair: "Box<Int>"`, against the struct applied to what the alias writes. Where nothing does, at `Any`, a contract or a type parameter, a struct from outside reads as applied to its fields' readings joined, as a list value reads as its elements joined, and a bounded parameter is held to its bounds, which `Any`, what readings of several types join to, conforms to none: such a value **refuses at the run** at the door.

**An alias takes no type parameters**, and a mention applying one **refuses at the build**: what it stands for may be a struct applied to types, `Pair: "Box<Int>"`.

**A declared name that is no struct and no enum and comes back to itself** through what it stands for, at any depth of the type it writes, through names alone, a `?`, a structure's parts and the types a struct or an enum is applied to among them, spells no type and **refuses at the load**: a type that holds itself is a declared struct or enum.

**An enum takes type parameters as a struct does**: every rule of this WARP for a struct's holds for an enum's, a case's fields standing where a struct's fields do, and what an enum's declaration adds is under [enums](../WARP-94/SPEC.md).

### The grammar

Each string `typeParameters` lists is an `entry`, which reads `identifier` from [names](../WARP-67/SPEC.md) and `bound` from [types](../WARP-46/SPEC.md#the-grammar): the type parameter's name, and the contracts that hold it where it is held.

```
entry           = identifier [ ": " bound ]
```

An entry is written one way, its bound's names in name order and each once, as a type's are under [types](../WARP-46/SPEC.md#the-grammar). A string the grammar does not produce, and any other string for one entry, **refuses at the load**.

## Interactions

- A claim and a member under a head applying the struct are under [heads](../WARP-55/SPEC.md) and [members](../WARP-58/SPEC.md).

## Alternatives considered

- Arguments that vary with what they are applied to. Were `Holder<Int>` to stand where `Holder<Int?>` is declared, a field holding a procedure taking `some T` would be read as taking `Int?`, and a null would reach a closure that takes an `Int`. Arguments are invariant, and only `Array` and `Dictionary` keep their covariance.
- Type parameters on an alias. An alias is a spelling, and a spelling taking arguments is what a front end writes and expands in place.

## Notes
