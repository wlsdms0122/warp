# WARP-48: What a slot takes, exactly

Status: accepted

## Summary

A slot is where a value meets a declaration, and the judgement is one rule per type. The rules decide what Any, a type unknown to the build, an empty list, a declared struct, an Optional and a procedure type accept at a slot.

## Motivation

A slot is where one implementation's value meets another's declaration, at a door above all, and a value one runtime takes and another refuses is a program that runs in one and not the other. Were one runtime to take `2` handed where an entry declares `{ name: n, type: Double }` and another to refuse it, or one to read `null` handed at `Int??` as the outer none and another as a some holding the inner one, a host would get two answers for one document. A front end writes no value a host hands, so each judgement is the IR's.

## Rules

Where a value meets a declaration (an argument, a return value, and a write into a box that said what it holds), the judgement is one rule per type.

**`Any` accepts everything.** It passes the value through untouched, null and procedures included. Nothing is judged, because nothing was declared, beyond what every door holds of a struct's name, under [a declared struct is nominal](../WARP-49/SPEC.md).

**A value of a type the build does not know** is a value read as `Any` or as a contract. It stands where `Any` is declared and where a call fills a type parameter no bound holds, and a value read as a contract stands where a contract it is read as is asked, a bound among them; anywhere else it **refuses at the build**, and a cast says what it is.

**An empty list or dictionary reads as holding `Never`.** It holds no element, so it is a value of a list or a dictionary of any type.

**A declared struct says which fields there are**, and a struct under its name fits only with exactly them: one short and one over both **refuse**, each field is judged against its type, and the value is held as it came. A case of an enum says which fields a value under its spelling has, the same way. To hand on fewer fields, write a struct literal of another declared struct; to keep keys a declaration does not name, declare `Dictionary<String, T>`, where the keys are the value's own.

**The door a value from outside comes through is the one place a value is fitted**: a field the declaration never named is left out of a struct under its name there, and a field the case never named out of one under a case's spelling, at whatever depth a struct, a list, a dictionary's key or value or an Optional holds it. A `Some` is not fitted: it is held to what [the value model](../WARP-2/SPEC.md) says a `Some` is, under [a declared struct is nominal](../WARP-49/SPEC.md).

**A declared name whose structure is neither a struct nor an enum is an alias**, a second spelling of what it stands for: the build reads every mention of it as that type, so it takes, joins and conforms to contracts wherever that type does. One whose structure is a struct is nominal, under [a declared struct is nominal](../WARP-49/SPEC.md), and so is one whose structure is an enum, under [enums](../WARP-94/SPEC.md).

**An Optional (`T?`) takes three readings, in this order.** A reading of an Optional `U?` stands as it is where `T` takes `U` and `U` is as many Optional levels deep as `T` or more. A reading of `Null`, and the literal `null`, is its none, the outermost one whatever `T` is. A reading `T` takes is its some, so a reading of `Int?` where `Int??` is asked is a some of `Int?`. A `T?` reading does not fit a plain `T` slot, and the same holds a level down: a reading of `Int??` does not fit `Int?`.

**A some is the value itself**, except where the value is `null` or a `Some`: then it is the struct `Some` holding the value. Where a reading that may hold one of those, `Null`, `Any`, an Optional, a type parameter, an associated type, a contract or a composition, or an alias of one, meets an Optional as its some, the build writes the promotion down and the run puts `Some` on exactly the `null`s and `Some`s; everywhere else a some is the value as it came. A value of `T?` is `null`, a `Some` holding a value of `T` that is `null` or a `Some`, or a value of `T` that is neither, so the run judges a `Some` by what it holds. Taking one level off is the `unwrap` construct's, under [statements](../WARP-27/SPEC.md): `null` is the none, a `Some` gives what it holds, and any other value gives itself. A variable handed in place is promoted nowhere, since it is the parameter's type all the way in, under [procedures](../WARP-18/SPEC.md).

**A list or a dictionary is promoted part by part.** A list whose elements read a type that may hold a none, where a list of their Optional is asked, is walked, and each element is its some, by value; a dictionary whose keys or values do is walked through them the same way, at any depth of lists and dictionaries. A procedure value is not walked, so it stands at another procedure type only where no value it is handed or returns would be promoted there: `() -> some T` where `() -> some T?` is asked **refuses at the build**.

**Ways that meet are no place.** A variable's ways meet at their readings joined, and where a value one way leaves would be promoted or have its type dropped to stand there, the build refuses and the variable declares its type, under *what a variable reads as* in [checking](../WARP-68/SPEC.md).

**A modifier stands in front of a procedure type**, under *the grammar* in [types](../WARP-46/SPEC.md#the-grammar).

**The numeric edge is value-independent.** `Int` refuses every `Double`, `2.0` included, and `Double` every `Int`, at the **build** where the value's reading is known and at the **run** at a door, where a value from outside comes with none. A literal read as a `Double` names the binary64 value nearest it, so digits past 2^53 round as binary64 rounds.

**`Never` fits every slot**, by never arriving. It is a real type: an expression typed `Never` may be written where any value is expected, such as an argument that calls `Standard.Control.abort`, and evaluating it ends the evaluation it is inside. The statement rules (no name, nothing follows) are statement rules.

**`inout` and `var` say something about the slot and nothing about the value.** What fits the slot is judged by the type after the mark, all of the type, under *the grammar* in [types](../WARP-46/SPEC.md#the-grammar), and where either is written is under *where a type is written* in [bounds](../WARP-52/SPEC.md#where-a-type-is-written).

**A slot asking `isolated` takes what is declared isolated.** Being const is a separate claim and does not stand in for it.

**A procedure-typed slot** takes a value that takes exactly the positions the slot's type hands, each accepting what the slot may hand at that position, returns what the slot's return type accepts, and fails with no more than the slot's type says it may fail with. What a closure may fail with is what its signature declares, as its constness is. The names the value's declaration wrote are its own and take no part: one closure fits two slots that name their parameter differently. That is held at the **build** where the value's type is known, and at the **run** where a cast reads a value read as `Any` or as a contract, under *one calling convention* in [procedures](../WARP-17/SPEC.md).

## Interactions

- Where a value of a contract stands, and what type it holds, is under [contracts](../WARP-53/SPEC.md).
- How a literal reads its place is under [numbers and readings](../WARP-47/SPEC.md).

## Alternatives considered

- An Optional as a union, `Null` or `T`. A union of a type with itself is that type, so `Int??` would collapse into `Int?`, and a generic body could not put a none into `some T?` and get it back apart.
- Every some written out by the document. A front end would then have to know each slot's type to write a value into it, which is not writing in place.
- An alias kept as a name in the type the build judges. Every judgement would have to remember to see through it, and each one that forgot would be a defect of its own.
- A value read as `Any` standing at a bounded type parameter without a cast, judged by the run. A contract slot already takes `Any` only through a cast, and a list of slots the run judges grows a missing slot whenever a slot is added.

## Notes

**Note.** A generic body does not know what fills its parameter, so the build can only write down where the promotion may happen, and the run does it on the values that need it.
