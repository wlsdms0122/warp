# WARP-67: Names and their grammar

Status: accepted

## Summary

Every name a program writes is in normal form C and holds the grammar of where it is written. The rules decide the grammar of type names, type parameter names, procedure names and member names, and which refuse at the load.

## Motivation

A declaration and a mention meet only by being the same name, and no scope or lookup stands between them, so a name has one byte spelling and one grammar for each place it is written. Compared as bytes in normal form C, two implementations find the same declaration for every mention, a path cuts into the same steps in each, and no dot makes one spelling two declarations' names.

## Rules

- every name the program writes is **written**, and is **normal form C**, compared as bytes: one name has one byte spelling, so a declaration and a reference can only meet by being the same bytes, `é` written two ways is a refusal, not two names, and nothing written is no name, since a declaration is called something and a reference writes something. A struct's field names hold this line at the encodings, and the names a program writes hold it here;
- every name holds the grammar of where it is written, and one that does not **refuses at the load** where it is written.

### The grammar

```
letter          = "A" … "Z" | "a" … "z"
digit           = "0" … "9"
identifier      = ( letter | "_" ) { letter | digit | "_" }
qualified-name  = identifier { "." identifier }
label           = identifier "." identifier { "." identifier }
spelling        = qualified-name "." identifier
reserved        = "Any" | "Never" | "Null" | "Bool" | "Int" | "Double" | "String" | "Array"
                | "Dictionary" | "Optional" | "Procedure" | "Self"
                | "Hashable" | "Failure" | "Round" | "Some"
                | "some" | "const" | "isolated" | "inout" | "var" | "throws"
                | "null" | "true" | "false"
```

| name | what it is | grammar |
|---|---|---|
| a **type's name** | what a type or a contract a module declares is called | a `qualified-name` that is not `reserved` and does not begin with `Self.` |
| a **procedure's name** | what a document declares under `procedures` | a `qualified-name` |
| a **type parameter's name** | the `T` of `some T`, a name a struct's or an enum's `typeParameters` lists, the part of a key of `bounds` before its first dot | an `identifier` that is not `reserved` |
| a **contract's procedure's name** | what a contract's procedure is called | an `identifier` |
| a **member's name** | what a procedure a type declares or extends with is called, after its type's name | an `identifier` |
| a **type member's name** | the type a contract asks under `types` and a type gives under its own | an `identifier` |
| a **case's name** | what an enum's case is called | an `identifier` |
| a **failure's name** | what `failing` and a procedure type's `throws(…)` call a failure, under [a procedure](../WARP-12/SPEC.md) | an `identifier` that is not `anything`, which `failing` writes for any failure |
| a **type member's label** | a type member written after what it stands on: `some T.Item`, `Self.Item` in a contract's procedures, a key of `bounds` or `sameTypes` naming an associated type | a `label` whose first `identifier` is a type parameter's name or `Self` and whose others are type members' names |
| a **member's spelling** | what a call writes for a member, and the name the member stands under among the procedures | a `spelling`: the name of the type its head is about, under [heads](../WARP-55/SPEC.md#the-grammar), then the member's name |
| a **contract's procedure's spelling** | what a call writes for a contract's procedure, and the name it stands under among the procedures | a `spelling`: the contract's name, then the contract's procedure's name |
| a **type member's spelling** | what a slot writes for a type member, and the name it stands under among the types | a `spelling`: the name of the type its head is about, under [heads](../WARP-55/SPEC.md#the-grammar), then the type member's name |
| a **case's spelling** | the name a value of a case carries, and the name the case stands under among the types | a `spelling`: the enum's name, then the case's name |
| a **value's name** | what a constant, a module variable, a statement, a loop's round, a try's failure, a parameter, a contract's procedure's parameter and a field of a struct type or of a case are called, and the name a switch's arm binds a field to | an `identifier` |

### What a name names

A **mention** of a type or a contract in a slot or a cast is a `name` under *the grammar* in [types](../WARP-46/SPEC.md#the-grammar), and a `language-name` there is the language's and no document's. A **struct's name**, which a struct value carries, is a type's name, a case's spelling under [enums](../WARP-93/SPEC.md), which is a type's name too, or `Failure`, `Round` or `Some`, the structs the language declares under [what the language declares](../WARP-61/SPEC.md). A **contract** a bound, a part joined with `&` or a claim names is a type's name or `Hashable`, so a type the language names or a struct it declares written there refuses at the load. The **type an extension or a claim is about** is written as a head, under *the grammar* in [heads](../WARP-55/SPEC.md#the-grammar).

## Interactions

- A name is its declared spelling and two namespaces hold them, under [names](../WARP-64/SPEC.md).
- A struct's field names are held at the encodings, under [encodings](../WARP-5/SPEC.md); a path's steps are under [a path](../WARP-31/SPEC.md#the-grammar).

## Alternatives considered

- A value's name of any scalars but the four a path's steps are written with, reached through a quoted spelling of a step, as some IRs quote a name that is no identifier. A field could then carry a key from outside, such as `content-type`, under its own spelling, and a path would have two spellings of a step to tell apart. A key that is no identifier is a dictionary's key, read with `["content-type"]`.

## Notes

**Note.** A dot is a character of a type's name and of a procedure's name, so both are `qualified-name`s. A call writes a contract's or a type's name, a dot and the procedure's name, so a contract's procedure, a member, a type member and a case are one `identifier`: a dot in one would make one spelling two declarations' names. A value's name is one `identifier`, so a path, which writes its steps with `.`, `[`, `]` and `?` under [a path](../WARP-31/SPEC.md), reads each name it holds as one step. A type's name beginning with `Self.` would read as an associated type of `Self`.
