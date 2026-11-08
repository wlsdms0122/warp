# WARP-46: How a type is written

Status: accepted

## Summary

A type is written as a string. The rules decide what each written type means, from the scalar types and Any and Never to arrays, dictionaries, optionals and procedure types, and what a type name may stand for.

## Motivation

A type is what every runtime reads off a host's signature and every front end writes, and a value is judged against it at a door, where what one implementation sent another receives. Two runtimes reading one string two ways take and refuse one value apart: were `Array<Int>?` read by one as an Optional list and by another as a list of Optionals, an entry declaring `{ name: xs, type: "Array<Int>?" }` would take `null` and refuse `[null]` in the first, and the reverse in the second. The string is what crosses between them, so no front end can settle it, and the spelling and what it means are the IR's.

## Rules

What a name may stand for, and what a slot takes. A type is judged at the build against the declarations the grammar read; what a type *admits* is asked of a value where it meets a slot, at the build where its reading is known and at the run at a door or a cast. Reads [the value model](../WARP-2/SPEC.md). Read by procedures, statements and expressions, each of which writes a slot.

A type is written as a string, a `type` under the grammar below, which reads `identifier`, `qualified-name` and `label` from [names](../WARP-67/SPEC.md).

### The grammar

```
type            = { mark } ( modified | procedure-type | bounded | joined | operand )
mark            = ( "inout" | "var" ) " "
modified        = modifier { modifier } ( procedure-type | "Procedure" )
modifier        = ( "const" | "isolated" ) " "
procedure-type  = "(" [ type { ", " type } ] ")" [ " throws" [ "(" [ failure { ", " failure } ] ")" ] ]
                  " -> " type
bounded         = "some " identifier ": " bound
bound           = qualified-name { " & " qualified-name }
joined          = qualified-name " & " qualified-name { " & " qualified-name } { "?" }
operand         = atom { "?" } | "(" ( procedure-type | modified | bounded ) ")" "?" { "?" }
atom            = name | applied | member | parameter | associated
name            = language-name | qualified-name
applied         = qualified-name "<" type { ", " type } ">"
member          = applied "." identifier
parameter       = "some " identifier
associated      = "some " label | "Self." identifier { "." identifier }
language-name   = "Any" | "Never" | "Null" | "Bool" | "Int" | "Double" | "String" | "Procedure"
                | "Self" | "Hashable" | "Failure" | "Round"
failure         = a failure's name, under names
```

| part | what it may be |
|---|---|
| a `name` | a `language-name`, or a type's name under [names](../WARP-67/SPEC.md); one beginning `Self.` is an `associated` |
| an `applied` | `Array` and one type, `Dictionary` and two, or a type's name and one type or more |
| a `member`'s `identifier` | a type member's name |
| the `identifier` after `some ` in a `bounded`, and a `parameter`'s `identifier` | a type parameter's name, an `identifier` that is not `reserved` under [names](../WARP-67/SPEC.md) |
| an `associated` | a type member's label |
| each `qualified-name` of a `bound` or a `joined` | a contract, under *what a name names* in [names](../WARP-67/SPEC.md) |
| the `modifier`s | `const`, `isolated`, or `const isolated` |
| the `mark`s | one, in a slot that takes it, under *where a type is written* in [bounds](../WARP-52/SPEC.md#where-a-type-is-written) |
| the failures `throws(…)` lists | one or more |

A `mark` and the `modifier`s stand in front of all of the type after them, and a `?` makes an Optional of all of the `atom`, the parenthesized type or the `joined` before it. What follows ` -> ` is all of a procedure type's return type, and what follows `: ` all of a bound, so each ends where the type it stands in ends: at the end of the string, or at the `, `, `>` or `)` of the list holding that type.

A string the grammar does not produce, and one with a part the table above does not let it be, **refuses at the load**. What a name stands for is the **build**'s, where the name resolves: a name no module declares, a type's name written with another count of types in brackets than its declaration lists type parameters, a name written bare counting none, and a `joined` naming a declaration that is no contract each **refuse at the build**, and what a `bound` may name is under *a bound names a contract* in [bounds](../WARP-52/SPEC.md).

### What a type means

| written | means |
|---|---|
| `Null` `Bool` `Int` `Double` `String` | the scalar types |
| `Any` | anything |
| `Never` | never returns. The type `Standard.Control.abort` declares, and what makes a leaving call checkable |
| `Array<T>` / `Dictionary<K, V>` | a list of `T` / a dictionary from keys of `K` to values of `V`, `K` a type that conforms to `Hashable`; `Array<Any>` is a list of anything |
| `Procedure` | some procedure, signature unsaid: a value of it stands where `Procedure` or `Any` is declared, and is called, or handed where a procedure type is written, only once a cast says what procedure it is |
| `const <procedure type>` | a const procedure, and `const Procedure` some const procedure, under *a const procedure* in [procedures](../WARP-15/SPEC.md) |
| `isolated <procedure type>` | a procedure that touches no name another body could touch at once, and `isolated Procedure` some such procedure; `const isolated <procedure type>` says both |
| `inout <type>` | a parameter handed a variable in place; written on a parameter's type, under *where a type is written* in [bounds](../WARP-52/SPEC.md#where-a-type-is-written) |
| `var <type>` | a field a path may write through; written on a field of a struct a type in `types` declares, under *where a type is written* in [bounds](../WARP-52/SPEC.md#where-a-type-is-written) |
| `Task` (any declared name) | the type a module declares under that name |
| `Box<Int>` (a declared struct or [enum](../WARP-93/SPEC.md) and the types it is applied to) | the struct a module declares under that name with its type parameters read as the types between the brackets, in the order it lists them. A struct or an enum is named with as many types in brackets as it lists type parameters, and without brackets where it lists none, and no other declaration is named with brackets: the build holds a name to this where it resolves |
| `App.Box.Item` / `App.Wrapper<String>.Item` (a type member's spelling, or a type applied to what its brackets hold followed by `.` and a type member's name) | the type the type member gives, read under the head it is given under, the head's type parameters read as what the brackets hold: an alias of it, under [associated types](../WARP-59/SPEC.md). The type before the dot is named as any mention names it, so `App.Wrapper.Item`, where `App.Wrapper` lists type parameters, **refuses at the build** |
| `some T` | a type parameter: worked out from the call, same reading everywhere it appears; bounded beside the first `some T` the signature's slots write, `some T: Standard.Comparable`. In a field of a struct listing it, the type a mention applies the struct to at its position |
| `Self` | the type conforming to a contract, written in that contract's procedures alone, under *where a type is written* in [bounds](../WARP-52/SPEC.md#where-a-type-is-written) |
| `Hashable` | the contract the language declares, which a dictionary's key conforms to, under [what the language declares](../WARP-61/SPEC.md): written as a contract is, and as a type a value of whatever type conforms to it |
| `Failure` / `Round` | the structs the language declares, what a catch binds and what a loop binds, under [what the language declares](../WARP-61/SPEC.md) |
| `some T.Item`, `Self.Item` | an associated type: the type the type filling `T` gives under a name a contract bounding `T` asks, and in a contract's procedures the one the type conforming to the contract gives, under [the associated types of a type parameter](../WARP-60/SPEC.md) |
| `Describable` (a declared contract's name) | a value of whatever type conforms to the contract. Nothing ties one slot's to another's |
| `Describable & Standard.Comparable` | a value of whatever type conforms to every contract named |
| `Int?` (any string spelling and `?`) | the Optional of the declared type, a sum of `Null` and the declared type: its none, and a some of each of the declared type's values. The Optional of an Optional is a type of its own, `Int??`, and so are `Null?`, `Any?` and `Never?` |
| `(Int, String) -> Bool` | a procedure type: the types it is called with, in position order, and after `->` what it returns, so `(Int) -> Int?` returns an Optional. No names, since a name is a declaration's and a value is called by position; `inout` in front of a parameter's type, `(inout Int) -> Int`, hands that parameter a variable in place |
| `(Int) throws -> Bool` / `(Int) throws(aborted, cast_refused) -> Bool` | what a procedure type may fail with: `throws` alone says anything, and `throws(…)` the failures it lists. Written without `throws`, it fails with nothing |
| `((Int) -> Int)?` / `(const Procedure)?` / `(some W: P)?` | the Optional of a procedure type, of a type the modifiers stand in front of, or of a type parameter written with its bound. A `?` written straight after one would stand inside it, in its return type or its bound, so parentheses group it and the `?` after them is the whole type's |

**A type is written one way**, the spelling the grammar gives it, with no white space but the grammar's, so `Dictionary<String,Int>` and `Array< Int>` are no string it gives. A procedure type's failures, a composition's names and a bound's names stand in name order, each once, so `App.B & App.A` is a second spelling of `App.A & App.B`. Any other string for one type **refuses at the load**, as a document saying a thing another way does under [the document format](../WARP-11/SPEC.md).

## Interactions

- What a slot of each type takes, the Optional included: [what a slot takes](../WARP-48/SPEC.md).
- A struct applied to types: [a struct may take type parameters](../WARP-50/SPEC.md); `some T` and its bound: [type parameters](../WARP-51/SPEC.md) and [bounds](../WARP-52/SPEC.md).
- The node that writes each string: [types, in the text](../WARP-39/SPEC.md).

## Alternatives considered

- Parameter names in a procedure type. A value's type would be tied to the names a receiving declaration chose, so a closure could not be handed to two slots whose parameters are named differently.

## Notes
