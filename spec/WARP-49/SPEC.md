# WARP-49: A declared struct is nominal

Status: accepted

## Summary

A declared struct is nominal. The rules decide that a struct type is written once and is exact, that a value of it carries its name, how a struct literal is read as the declared struct its place reads, and what happens at a door or a cast when the name differs.

## Motivation

A contract call picks its row by the type that fills `Self`, and a door holds a struct to the declaration its name names. Were a struct only its fields, `{ title: "a", done: false }` would be a value of every struct with those fields and of `Dictionary<String, Any>` at once, and which row a contract call reached would depend on the value's shape rather than on what a document declared.

## Rules

**A struct type is written once**, as the structure of a type declared in `types`, `{ struct: { title: String, done: Bool } }` under the type's name, its fields under `struct`, each called by a value's name under [names](../WARP-67/SPEC.md); everywhere else a type names it. It is a name as well as a structure, and a value of it carries the name.

**A struct type is exact.** A declared struct fits a value under its own name and no other, so two declared structs of one structure under two names are two types, and a declared struct and `Dictionary<String, T>` of its fields take nothing of each other. A slot judges a value and hands it on as it came; it does not rebuild one. A struct under another name **refuses** at the **build** where the build can see the name and at the **run** at the door it comes through, and where a cast reads a value read as `Any` or as a contract, the cast fails with `cast_refused` and `as?` reads it as null. An alias, under [what a slot takes, exactly](../WARP-48/SPEC.md), attaches no name.

**A struct literal is read as the declared struct its place reads**, as every literal is read as its place reads it. The build judges it there field by field against the declaration, exactly the declared fields, and it takes the struct's name. A struct literal written where no declared struct is read, at `Any`, at a contract, at a type parameter no call fills with a declared struct or at a name that declares nothing, **refuses at the build**.

**A value from outside holds a name only as a struct's or as a case's.** At every door, whatever the slot declares, `Any` included, a struct under a name is held to the struct the name declares, or to the case it spells under [enums](../WARP-94/SPEC.md), fitted to it as [what a slot takes, exactly](../WARP-48/SPEC.md) fits a value at a door and judged against it, an alias's name becoming its struct's. One under a name that declares neither **refuses at the run**, and so does a dictionary at a declared struct, which takes no dictionary. A struct under `Some` is held to [the value model](../WARP-2/SPEC.md) and not fitted: one that is not exactly `wrapped` holding `null` or a `Some` **refuses at the run**, whatever the slot declares. So every struct under a name is a value of that struct, of that case's enum, or a `Some` the value model admits.

**Note.** A case hands a door only what a case's text writes, and a text refuses a `Some` the value model does not admit, so the door refusing one is held only by tests inside the implementation.

**A dictionary's key from outside is a value**, held there as its value is. Two keys of one dictionary that this makes one key, a struct under an alias's name beside one under its struct's or two structs apart only in a field left out, **refuse at the run**: a dictionary value holds its keys in the key order, so neither of the two is the later one.

**A declared struct may name itself** in a field at any depth of the field's type, directly included, so a tree is one declaration, and an enum may name itself in a case's field the same way.

## Interactions

- A struct applied to types is under [a struct may take type parameters](../WARP-50/SPEC.md).
- A claim is about the struct a value is an instance of, under [claims](../WARP-54/SPEC.md), and a contract call picks its row by that name, under [calling a contract's procedure](../WARP-63/SPEC.md).
- A dictionary's keys and their sameness are under [a dictionary's keys](../WARP-3/SPEC.md) and [a dictionary's key](../WARP-62/SPEC.md).

## Alternatives considered

- An unnamed record type, a struct known only by its fields. One construct then played three parts, a struct, a tuple and a dictionary, and a contract call through `Self` could not tell which; patching that at the contract slot would add a rule for one shape.

## Notes
