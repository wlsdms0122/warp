# WARP-94: Where an enum stands

Status: accepted

## Summary

An [enum](../WARP-93/SPEC.md) is a declared type, nominal as a declared struct is, and stands where a declared struct stands, rule for rule: in a slot and at the door, in a join and a cast, under a claim, with members and with type parameters. A case is not a type, a dot reads nothing on an enum, and the door holds a value from outside to its case. Reads *a declared struct is nominal* in [types](../WARP-49/SPEC.md).

## Motivation

The document under [enums](../WARP-93/SPEC.md#motivation) names `App.Target` in its entry's signature and in a native procedure's, and hands a value of it across the door. For a signature to say the enum, the enum has to stand wherever a type is written, and for a value to have one shape at the door, the door has to hold a struct under a case's spelling to that case. Neither is a front end's to write, since where a type stands and what a door judges are the IR's. Standing where a declared struct stands, rule for rule, gives an enum every place a type has with no second set of rules, and leaves the IR what is an enum's alone to say: a case is no type, a dot reads nothing on one, and a value under a case's spelling is held to its case.

## Rules

**An enum is a declared type, nominal as a declared struct is.** Its name stands wherever a type is written: a slot, a return type, a name saying what it holds, a cast, a field of a struct or of a case, a list's element, a dictionary's key or value, an Optional, a type argument, a claim, an extension's head, and an alias, which is a second spelling of it. A slot of an enum takes a value under one of its cases' spellings and no other: a struct, a dictionary, and a value of another enum each **refuse** at the build where the build sees it and at the run at the door, as a struct under another name does under [types](../WARP-49/SPEC.md). An enum, a declared struct and a dictionary are types none of which takes another.

**A case is not a type.** A case's spelling names no type, so written as a type, the type of a claim a document imports under [the imports list](../WARP-10/SPEC.md) included, it **refuses at the load** where the document declaring the enum writes it, since the document shows it alone, and **at the build** where another document does, where the name resolves. What one case carries is read in the arm of a `switch` that names it, under [a switch](../WARP-95/SPEC.md).

**An enum declares no field of its own**, since which fields a value carries is its case's. A dot on a reading of one is a dot on a type that has no fields, under [expressions](../WARP-33/SPEC.md), and an index on one, or a `set` through one, **refuses at the build** too.

**Two readings of one enum join to it where they apply it alike**, and to `Any` where they apply it to different types, as two of one struct do under [types](../WARP-50/SPEC.md); an enum beside any other reading but `Null`, a declared struct or another enum among them, joins to `Any`, and beside `Null` to its Optional, under [types](../WARP-47/SPEC.md). Two mentions of one enum are one type only where they apply it to the same types, by the rule two mentions of one struct are, `Never` read as any type.

**The door holds a value to its case.** At every door, whatever the slot declares, `Any` included, a struct under a case's spelling is held to that case: fitted to it as [what a slot takes, exactly](../WARP-48/SPEC.md) fits a value at a door, and judged against the fields it carries, as a struct under a declared struct's name is under [a declared struct is nominal](../WARP-49/SPEC.md). A case's spelling is the enum's declared name, then the case's name, under [names](../WARP-67/SPEC.md#the-grammar), and a struct under a spelling no enum declares a case under **refuses at the run**, as one under a name that declares nothing does: `App.Target.ftp` where `App.Target` declares `local` and `remote`, the enum's own name, `(struct App.Target)`, and `App.Place.remote` where `App.Place` is an alias of `App.Target`. So does one whose fields do not fit. The enum's type parameters read as the slot applies the enum, and at `Any`, a contract or a type parameter as applied to what the value's fields read as, joined, `Never` at a parameter no field reads, as a struct from outside is under [types](../WARP-50/SPEC.md).

**A cast to an enum** reads a value read as `Any` or as a contract: it holds where the value is under one of the enum's cases' spellings and its fields fit the enum as the cast applies it, and otherwise fails with `cast_refused`, which `as?` reads as the none, under [expressions](../WARP-32/SPEC.md). What `cast_refused`'s `actual` names for a value of an enum is under [`try`](../WARP-25/SPEC.md). Which casts between a reading of an enum and one of a declared struct, a dictionary, another enum or the enum applied to other types the build refuses, and which between their Optionals stand, is under [expressions](../WARP-32/SPEC.md), which reads an enum there as it reads a declared struct.

**`Hashable`.** An enum conforms to `Hashable` where a document claims it does, `{ enum: { … }, satisfies: [Hashable] }`, as a declared struct does under [types](../WARP-62/SPEC.md), and a dictionary type keyed by an enum no claim within what the document stands on puts under it **refuses at the build**. Which keys are one key is sameness, under [values](../WARP-4/SPEC.md), so two values of one case carrying the same values are one key, and a value carrying a procedure is no key, under [values](../WARP-3/SPEC.md).

**Claims and members** are a struct's, under [types](../WARP-54/SPEC.md) to [types](../WARP-58/SPEC.md). A claim beside the cases, or in an extension another document writes, is about every value of the enum, of every case and whatever the enum is applied to, and is backed by the enum's members, each taking a value of the enum first, `App.Target.describe` taking an `App.Target`. Under a head applying the enum, `App.Result<Int, some E>`, what is given holds for the values the head takes. So an enum gives a contract's procedure, a `describe` a front end spells it with among them, as a struct does. A claim about a case refuses as a claim about no type, at the stage *a case is not a type* says.

**Type parameters** are a struct's, under [a struct may take type parameters](../WARP-50/SPEC.md), which holds each of its rules for an enum's, a case's fields standing where a struct's fields do.

## Interactions

- An enum stands where a declared struct stands: [WARP-49](../WARP-49/SPEC.md).
- A cast to an enum: [WARP-32](../WARP-32/SPEC.md).
- Claims, members and `Hashable`: [WARP-54](../WARP-54/SPEC.md) to [WARP-58](../WARP-58/SPEC.md), and [WARP-62](../WARP-62/SPEC.md) for a dictionary's key.
- Type parameters in a mention and at the door: [WARP-50](../WARP-50/SPEC.md) to [WARP-52](../WARP-52/SPEC.md).

## Alternatives considered

- **A case as a type**, as Kotlin's sealed subclass is, with a slot that takes one case. Swift has no such slot, and a slot taking one case has nothing to ask of it. A front end writes a sealed subclass as a struct and a case carrying it, `remote(Remote)`, which is how Swift writes the same thing, so the core needs no relation of a case's type standing in its enum's place.
- **A door that also takes a case's name as a string**, `"local"` beside `(struct App.Target.local)`. One value has one spelling, so sameness, `text` and both encodings read one shape. Turning a string into a case is the host's, by the signature, at its own door.

## Notes
