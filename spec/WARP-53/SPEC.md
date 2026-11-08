# WARP-53: Contracts

Status: accepted

## Summary

A contract says which procedures, and which types, a conforming type gives. The rules decide how a contract is declared, what Self is, and that a contract's procedure takes Self first. They also decide that a value read as a contract holds the type it was read as, and fills a bounded type parameter only where the parameter stands alone.

## Motivation

A program that arrives later gives a type that already runs new procedures, and a host hands a program values it did not build, so a slot often asks what a value can do rather than what it is. `App.log` taking whatever describes itself is no one type: a `Bank.Account` today, and a `Shop.Order` from a document that arrives next week. A contract says it in the document, `contracts: { "App.Describable": { procedures: { describe: { parameters: [Self], returns: String } } } }`, and `App.log` takes `App.Describable`. Without one, a front end could only bake a table of procedures into each call, which the build could not hold to the types and a door could not judge.

## Rules

**A contract says which procedures a type conforming to it gives**, and which types that type gives, under [associated types](../WARP-59/SPEC.md): the types that conform to it are open, and new ones arrive with new documents. A module declares one the way it declares a type: a name bound to the procedures it asks, under `procedures`, each written as a signature whose first parameter is `Self`, the type that conforms to the contract, since what fills `Self` there picks the procedure.

**`Self` is one type wherever it stands.** It may stand at any of the procedure's positions and in its return type, `Self?` included. A claim reads it as the type the claim is about, and `Self?` as the Optional of that type, for a claim about `Null` the Optional of `Null`. A call through the contract reads it as one type parameter the contract bounds, filled from the call the way any type parameter is.

**A contract's procedure takes `Self` first**, by value or in place: a variable handed there in place fills `Self` as a value does, so a contract may ask a procedure that changes the value it is called on, and a contract's variable written whole there holds on the type it held. Its first parameter's type is `Self` or `inout Self`, and one written otherwise **refuses at the load**. `Self` is written in a contract's procedures alone, under *where a type is written* in [bounds](../WARP-52/SPEC.md#where-a-type-is-written), and names no type parameter, under [names](../WARP-67/SPEC.md).

**Note.** A contract's own name at the first position is a value of whichever type conforms to the contract, so it is not the type that fills `Self` and picks no row.

**A contract may ask no procedures.** It is then a mark a claim gives a type, and a type conforms to it where a document claims it does, as for any contract.

**A contract's name stands where a type is written, and so does `A & B`**: the slot takes a value of whatever type conforms to every contract named. This is how the language says **A or B**: each type claims one contract and the slot names it. Either is a type parameter with no name, so nothing ties one slot's reading to another's, and a call fills nothing. A name that is not a contract's joined with `&` **refuses at the build**, and a type the language names or a struct the language declares joined with `&` **refuses at the load**.

**A value read as a contract is of a type the build does not know** and stands where [what a slot takes, exactly](../WARP-48/SPEC.md) says: a value read as `A` does not stand where `B` is asked, and one read as `A & B` stands where either is.

**A value read as a contract holds the type it was read as.** The run holds such a value beside a type, which the table gives by where the value comes to be read as a contract:

| where | what the value holds |
|---|---|
| a reading of a type that is no contract meets a contract: at an argument, a return, a write, a key a path reads or writes between brackets, or a part of a list, dictionary, struct or [case](../WARP-93/SPEC.md#a-cases-value) literal, and part by part where it meets a list, a dictionary or an Optional of a contract | that reading, which may name a type parameter, read as the call the body runs in filled it |
| a reading of a contract meets a contract there | the type its value holds, so a value read as `A & B` handed where `A` is asked holds what it held |
| a door, and a cast to a contract of a reading of `Any`, or of an Optional of `Any` whose value is its some | the type the value is an instance of |
| a cast to a contract of any other reading | the reading, read as the call the body runs in filled it, and where that is a contract, or an Optional of one and the value its some, the type the value holds |
| a native procedure is handed a value, as an argument or as what a closure it calls or a procedure it sends returns | the type the run holds it at |
| a native procedure hands a value back, or writes one through a parameter handed in place | the type the value holds |
| the build folds a value: a constant, a key a path reads or writes between brackets that a constant folds to, a module variable's start, and what a closure captured | the type the value holds |
| the value meets `Any`, in the value and in every list, dictionary and struct field holding one | none |
| the run hands the host its result, what an entry answers | none |

A cast to a contract judges the type the value holds at that reading and holds it on, so `maybe as? App.Described` of a `maybe` read as `Int?` is the none where `Int` conforms to `App.Described` and `Int?` does not. A cast to any other type judges the value. The type is the run's and no value's, so a value read as `Any` or handed to the host carries none. A native procedure is called by the run and what it returns comes back into the run, so a value keeps its type across one. A value the build folds keeps it too: the object writes the type beside the value, under [values, in an object](../WARP-90/SPEC.md), and the link holds the value beside it again. Sameness, `text` and a dictionary's keys read the value, so two keys that are one value are one key, holding what the entry the dictionary keeps holds.

**A value of a contract fills a bounded parameter only where the parameter stands alone.** A type parameter a contract bounds is one type wherever it stands, while a value of a contract is of whichever type conforms to it, so it fills one only where the parameter stands alone at one of the procedure's positions: `App.Described.describe` takes one, and a call handing one where the parameter stands twice, `Self` of `lhs` and `rhs` included, or inside a list, a dictionary or a struct, **refuses at the build**. A closure literal's parameter is such a slot too, and a call of the value holds what it hands to the contract by the rule a call to a declaration is held by. A value of a contract standing there fills the parameter with the type it holds, and the body takes the value. What the call returns is held at that type where the return type writes the parameter, and part by part through an Optional, a list and a dictionary of it, so a call whose return type writes the parameter inside a struct or a procedure type **refuses at the build** where a value of a contract fills it, `Self` included.

**Note.** A key a path writes into a dictionary keyed by a contract holds the type it was read as, and nothing a case writes reads that type back: `Standard.Collection.keys` bounds its `Key`, and a value of a contract fills a bounded parameter only where it stands alone, so it refuses such a dictionary at the build. So the hold is held only by tests inside the implementation.

**Note.** A native procedure that writes a value through a parameter handed in place keeps the type the value holds, and no case holds it: a procedure a case's `vocabulary` brings declares what it returns and writes through no parameter, under [conformance](../WARP-1/SPEC.md). So that row is held only by tests inside the implementation.

## Interactions

- A type conforms where a document claims it, under [claims](../WARP-54/SPEC.md) and [heads](../WARP-55/SPEC.md), and a claim is held to members under [a claim holds to members](../WARP-56/SPEC.md).
- A contract call and the table the build makes are under [calling a contract's procedure](../WARP-63/SPEC.md).

## Alternatives considered

- Memberships, a type that names its members, "`Int` or `Double`". Every type is a type in the same way, the language's and a document's, and a type says what it conforms to by a claim, so a membership would be a second way to say what a contract says.
- Contracts left out of the document, a front end baking a table of procedures for each type. The run could then not show that a value answers what a slot asks, and the table the link fills for a contract call would have nothing to read.

## Notes
